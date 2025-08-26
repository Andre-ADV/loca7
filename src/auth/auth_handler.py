import datetime
from fastapi import HTTPException
import jwt
import re

from src.config import SECRET_KEY, ALGORITHM
from time import time
from src.auth.schemas import TokenResponseScheme

from fastapi import status

def token_response(token: str) -> TokenResponseScheme:
    return TokenResponseScheme(access_token=token)

def generate_token(user_id: int):

    payload = {
        "sub": str(user_id),
        "iat": time(),
        "exp": time() + 60 * 15 # 15 minutos para expiração do token 
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token

def decode_token(token: str):
    print(token)
    
    try:
        decoded_token = jwt.decode(
            token, 
            SECRET_KEY, 
            algorithms=[ALGORITHM],
            options={"require": ["sub", "iat", "exp"]}  
        )

        return decoded_token
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

def sanitize_bearer(header: str) -> str:
    """
    Aceita:
      - "Bearer <token>"
      - "<token>" (já limpo)
    Rejeita:
      - vazio, None, "Bearer" sem token, strings com espaços a mais
      - tokens que não parecem JWT (3 partes)
    """
    _JWT_RE = re.compile(r"^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$")

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
