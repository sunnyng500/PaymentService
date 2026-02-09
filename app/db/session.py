import os
from collections.abc import AsyncGenerator
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker

load_dotenv()

ORACLE_USER = os.getenv("DB_USER")
ORACLE_PASSWORD = os.getenv("DB_PASSWORD")
ORACLE_HOST = os.getenv("DB_HOST")
ORACLE_PORT = os.getenv("DB_PORT")
ORACLE_SERVICE = os.getenv("DB_SERVICE_NAME")

DB_URL = f"oracle+oracledb://{ORACLE_USER}:{ORACLE_PASSWORD}@{ORACLE_HOST}:{ORACLE_PORT}/?service_name={ORACLE_SERVICE}"

#for sync session
local_engine = create_engine(DB_URL,echo=True)
local_session = sessionmaker(bind=local_engine)
def get_db():
    db = local_session()
    try:
        yield db
    finally:
        db.close()

#
async_engine = create_async_engine(DB_URL,echo=True)
async_session = async_sessionmaker(bind=async_engine,autoflush=False,expire_on_commit=False)

async def get_async_db() -> AsyncGenerator[AsyncSession,None]:
    async with async_session.begin() as session:
            yield session

