from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

Base = declarative_base()

db_url = settings.ASYNC_DATABASE_URL

# Fallback for standalone environment if postgresql port is not listening
try:
    import socket
    s = socket.socket()
    s.settimeout(1)
    if s.connect_ex((settings.POSTGRES_SERVER, settings.POSTGRES_PORT)) != 0:
        db_url = "sqlite+aiosqlite:///./elearning_recsys.db"
    s.close()
except Exception:
    pass

engine = create_async_engine(
    db_url,
    echo=False,
    future=True,
)

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
)


async def get_db():
    """Dependency for obtaining async SQL database sessions."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    """Create database tables if they do not exist on startup."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
