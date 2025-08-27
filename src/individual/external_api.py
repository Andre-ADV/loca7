from __future__ import annotations
import httpx
import time

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.individual.config import BASES
from src.individual.infoqualy.parser_infoqualy import flatten_infoqualy 
from src.individual.infoqualy.repository import upsert_individual_from_infoqualy_async 

class ExternalAPI:
    def __init__(self, base_name: str = "infoqualy", token_ttl_seconds: int = 50 * 60):
        self.bases = BASES
        self.base_name = base_name
        self._token_value: Optional[str] = None
        self._token_exp: int = 0
        self._token_ttl = token_ttl_seconds

    async def get_token(self) -> str:
        """Gera token (sem cache)."""
        cfg = self.bases['infoqualy']
        async with httpx.AsyncClient(timeout=60) as client:
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
    
    async def get_data_individual(self, cpf: str, db: AsyncSession) -> dict | None:
        cfg = self.bases['infoqualy']
        token = await self._get_token_cached()
        payload = {"doc": cpf}

        async with httpx.AsyncClient(timeout=150) as client:
            resp = await client.post(
                cfg["url_consulta_pf"],
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
                    cfg["url_consulta_pf"],
                    headers={
                        "Authorization": f"Bearer {token}",
                        "Content-Type": "application/json",
                    },
                    json=payload,
                )

            resp.raise_for_status()
            data_api = resp.json()

        # Validação mínima para decidir se persiste
        flat = flatten_infoqualy(data_api)
        if flat.get("cpf") and flat.get("nome"):
            ind = await upsert_individual_from_infoqualy_async(db, data_api)
            print(ind)

        return flat
