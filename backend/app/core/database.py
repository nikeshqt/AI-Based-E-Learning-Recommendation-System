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


def _sync_schema_updates(sync_conn):
    Base.metadata.create_all(sync_conn)
    from sqlalchemy import text
    # Check for sqlite pragma support to ensure backwards-compatible schema sync
    try:
        rows = sync_conn.execute(text("PRAGMA table_info(users)")).fetchall()
        user_cols = {r[1] for r in rows}
        if user_cols:
            if "role" not in user_cols:
                sync_conn.execute(text("ALTER TABLE users ADD COLUMN role VARCHAR DEFAULT 'student' NOT NULL"))
            if "is_active" not in user_cols:
                sync_conn.execute(text("ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT 1 NOT NULL"))
            if "last_login" not in user_cols:
                sync_conn.execute(text("ALTER TABLE users ADD COLUMN last_login TIMESTAMP"))
    except Exception:
        pass

    try:
        rows = sync_conn.execute(text("PRAGMA table_info(courses)")).fetchall()
        course_cols = {r[1] for r in rows}
        if course_cols:
            if "is_active" not in course_cols:
                sync_conn.execute(text("ALTER TABLE courses ADD COLUMN is_active BOOLEAN DEFAULT 1 NOT NULL"))
    except Exception:
        pass


async def init_db():
    """Create database tables and sync schema if they do not exist on startup."""
    async with engine.begin() as conn:
        await conn.run_sync(_sync_schema_updates)
