from src.config import DATABASE_URL
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

# Connections
# Creating engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Binding engine to session
SessionLocal = async_sessionmaker(bind=engine)

# Models Base
Base = declarative_base()

# Create tables and get session
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
