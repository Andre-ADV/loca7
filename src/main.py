from src.auth.router import auth_router
from src.users.router import users_router

from src.database import get_db
from typing import Annotated, AsyncGenerator

from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
async def main(db: Annotated[AsyncGenerator, Depends(get_db)]) -> None:
    return JSONResponse(content={"message": "OK"}, status_code=200)

app.include_router(auth_router)
app.include_router(users_router)
