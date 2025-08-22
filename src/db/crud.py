from sqlalchemy import select, text
from src.db.database import SessionLocal, get_db

class Crud:

    def __init__(self, model):
        self.db = get_db()
        self.model = model

    async def getAll(self):
        result = await self.db.execute(select(self.model))
        return result.scalars().all()
    
    

