from pydantic import BaseModel

class AuthLogin(BaseModel):
    email: str
    password: str

class CreateUserRequest(BaseModel):
    username: str
    password: str

