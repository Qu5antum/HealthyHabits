from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from backend.src.config.config import config

# database işlemleri
engine = create_async_engine(config.URL_DATABASE)
Base = declarative_base()
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# veritabanda tabloları oluşturmak
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_session()-> AsyncSession:
    async with async_session() as session:
        yield session



