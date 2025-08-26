from typing import Optional

from fastapi import Request, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .auth_handler import decode_token, sanitize_bearer

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        # Parsing das credenciais de autorizacao
        creds: Optional[HTTPAuthorizationCredentials] = await super().__call__(request)
        
        # Verifica se as credenciais existe e se é do tipo Bearer
        if not creds or not creds.scheme == "Bearer":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        
        # Trata o token
        token = sanitize_bearer(creds.credentials)    
    
        # Retorna o token decodificado
        return decode_token(token)
