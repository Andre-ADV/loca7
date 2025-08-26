from __future__ import annotations
import httpx
import time

from sqlalchemy.ext.asyncio import AsyncSession
from src.individual.config import BASES
from individual.infoqualy.parser_infoqualy import flatten_infoqualy 
from individual.infoqualy.repository import upsert_individual_from_infoqualy_async 

class ExternalAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.bases = BASES

    async def get_token(self) -> str:
        """Gera token (sem cache)."""
        cfg = self.bases[self.base_name]
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(
                cfg["url_token"],
                headers={"Authorization": f"Bearer {cfg['api_key']}"},
            )
            resp.raise_for_status()
            token = resp.json().get("token")
            if not token:
                raise RuntimeError("Token ausente na resposta de gerar_token.")
            return token

    async def _get_token_cached(self) -> str:
        now = int(time.time())
        if self._token_value and self._token_exp > now:
            return self._token_value
        token = await self.get_token()
        self._token_value = token
        self._token_exp = now + self._token_ttl
        return token

    def _invalidate_token(self) -> None:
        self._token_value = None
        self._token_exp = 0
        
    async def get_token(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.bases['infoqualy']['url_token'],
                headers={
                    "Authorization": f"Bearer {self.bases['infoqualy']['api_key']}"
                }
            )
            response.raise_for_status()  # levanta erro se a resposta for inválida
            data = response.json()
            return data.get("token")
    
    async def get_individual(self, cpf: str, db: AsyncSession) -> dict | None:
        """
        Consulta Infoqualy com CPF, faz parse e faz upsert assíncrono.
        Retorna o JSON bruto da API.
        """
        cfg = self.bases[self.base_name]
        token = await self._get_token_cached()
        payload = {"doc": cpf}

        async with httpx.AsyncClient(timeout=60) as client:
            # 1ª tentativa
            resp = await client.post(
                cfg["url_consulta"],
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                },
                json=payload,
            )

            # Se token expirou
            if resp.status_code == 401:
                self._invalidate_token()
                token = await self._get_token_cached()
                resp = await client.post(
                    cfg["url_consulta"],
                    headers={
                        "Authorization": f"Bearer {token}",
                        "Content-Type": "application/json",
                    },
                    json=payload,
                )

            resp.raise_for_status()
            data_api = resp.json()
            print(data_api)

        # Validação mínima para decidir se persiste
        flat = flatten_infoqualy(data_api)
        if flat.get("cpf") and flat.get("nome"):
            await upsert_individual_from_infoqualy_async(db, data_api)

        return data_api
