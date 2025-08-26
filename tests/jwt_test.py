import time
import jwt
import re


from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Dict, Annotated, Optional
from fastapi import Request, HTTPException, Depends, FastAPI, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

secret = "secret"
algorithm = "HS256"

_JWT_RE = re.compile(r"^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$")

class User(BaseModel):
    user_id: int

def token_response(token: str):
    return {
        "access_token": token,
    }

class TokenData(BaseModel):
    sub: str
    iat: datetime
    exp: datetime
    model_config = ConfigDict(from_attributes=True)

def sanitize_bearer(header: str) -> str:
    """
    Aceita:
      - "Bearer <token>"
      - "<token>" (já limpo)
    Rejeita:
      - vazio, None, "Bearer" sem token, strings com espaços a mais
      - tokens que não parecem JWT (3 partes)
    """
    if not isinstance(header, str) or not header.strip():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token ausente")

    parts = header.strip().split()

    if len(parts) == 1:
        # já é o token (sem prefixo)
        token = parts[0]
    elif len(parts) == 2 and parts[0].lower() == "bearer":
        token = parts[1]
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization malformado")

    # remove aspas acidentais
    token = token.strip().strip('"').strip("'")

    if token.count(".") != 2 or not _JWT_RE.fullmatch(token):
        # evita erros como "Invalid header padding" no decoder
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token malformado")

    return token
    

def decode_jwt(token: str) -> User:

    try:
        claims = jwt.decode(
            token, 
            secret, 
            algorithms=[algorithm],
            options={"require": ["exp", "iat", "sub"]},
        )



        return TokenData(**claims)
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError as e:
        print(e)
        raise HTTPException(status_code=401, detail="Token inválido")
    
def encode_jwt(user_id: int):
    payload = {
        "sub": str(user_id),
        "iat": time.time(),
        "exp": time.time() + 1200
    }

    token = jwt.encode(payload, secret, algorithm=algorithm)

    return token_response(token) 


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = False):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        creds: Optional[HTTPAuthorizationCredentials] = await super().__call__(request)
        if not creds or not creds.scheme == "Bearer":
            raise HTTPException(status_code=403, detail="Invalid token")

        print(creds.credentials)

        token = sanitize_bearer(creds.credentials)    
    
        return decode_jwt(token)


def get_current_user(token: Annotated[TokenData, Depends(JWTBearer())]):
    return User(user_id = int(token.sub))

app = FastAPI()

@app.post("/auth")
async def authenticate(user_id: int):
    return encode_jwt(user_id=user_id)

@app.get("/")
async def add_post(current_user: Annotated[str, Depends(get_current_user)]) -> dict:
    return {
        "user": current_user
    }


