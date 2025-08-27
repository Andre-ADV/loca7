from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

class UserAuthScheme(BaseModel):
    email: EmailStr
    senha: str

class TokenScheme(BaseModel):
    sub: str
    iat: datetime
    exp: datetime
    model_config = ConfigDict(from_attributes=True)

class TokenResponseScheme(BaseModel):
    access_token: str
