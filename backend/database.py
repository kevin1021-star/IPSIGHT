"""
CIPHER-SENTINEL: Async SQLAlchemy database layer (Neon PostgreSQL via asyncpg).

Exports
-------
engine            – AsyncEngine instance
AsyncSessionLocal – async_sessionmaker factory
Base              – declarative base for ORM models
get_db            – FastAPI dependency that yields an AsyncSession
"""

from __future__ import annotations

import logging
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Settings (reads from environment / .env)
# ---------------------------------------------------------------------------

class _DBSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    DATABASE_URL: str = "sqlite+aiosqlite:///./cipher_sentinel_dev.db"


_settings = _DBSettings()


# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------

_connect_args: dict = {}

# Neon / asyncpg requires ssl; aiosqlite needs check_same_thread disabled
if "sqlite" in _settings.DATABASE_URL:
    _connect_args = {"check_same_thread": False}
else:
    _connect_args = {"ssl": "require"}

engine: AsyncEngine = create_async_engine(
    _settings.DATABASE_URL,
    echo=False,          # set True for SQL debug logging
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    connect_args=_connect_args,
)

AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


# ---------------------------------------------------------------------------
# Declarative base (imported by models.py)
# ---------------------------------------------------------------------------

class Base(DeclarativeBase):
    pass


# ---------------------------------------------------------------------------
# FastAPI dependency
# ---------------------------------------------------------------------------

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Yield an async database session, rolling back on error."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
