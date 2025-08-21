from pydantic import BaseModel

class Users(BaseModel):
    name: str
    email: str
    password: str 
    document: str 
    doc_type: str 