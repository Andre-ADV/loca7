from typing import List
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from src.users.schemas import CreateUser, DeleteUser, ReadUser, UpdateUser, User

users_router = APIRouter(
    tags=['users'],
    prefix='/users'
)

fake_users = [
    User(id_=1, name="Aliffer", email="blz@gmail.com", document="52248676816"),
    User(id_=2, name="Maria", email="maria@gmail.com", document="12345678901"),
]

@users_router.get('/', response_model=List[User])
async def getUsers():
    return fake_users

@users_router.get("/{id}", response_model=User)
async def getUser(id: int):
    for user in fake_users:
        if user.id_ == id:
            return user
    raise HTTPException(status_code=404, detail="Usuário não encontrado")

@users_router.post('/')
async def createUser(user: CreateUser):
    return user
    return JSONResponse(content={"message": "Users route"}, status_code=200)

@users_router.patch('/')
async def updateUser(user: UpdateUser):
    return user
    return JSONResponse(content={"message": "Users route"}, status_code=200)

@users_router.delete('/')
async def deleteUser(user: DeleteUser):
    return user
    return JSONResponse(content={"message": "Users route"}, status_code=200)


