from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
async def main() -> None:
    return JSONResponse(content={"message": "OK"}, status_code=200)


