from typing import Generator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

import settings

# create async engine for interaction with database
engine = create_async_engine(settings.REAL_DATABASE_URL, future=True, echo=True)

# create session for the interaction with database
async_session= sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_db() -> Generator:
    """Dependency for getting async session"""
    try:
        session: AsyncSession = async_session()
        print("session open") # Отладочный print!
        yield session
    except Exception as e:
        print(f"{e=}")
    finally:
        await session.close()
        print("session close") # Отладочный print!