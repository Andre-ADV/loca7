from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Olá, mundo! Esta é sua API FastAPI."}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}