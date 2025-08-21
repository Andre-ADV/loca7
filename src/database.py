from config import DATABASE_URL
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

# Connections
# Creating engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Binding engine to session
SessionLocal = async_sessionmaker(engine)

# Models Base
Base = declarative_base()

# Create tables and get session
async def get_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
