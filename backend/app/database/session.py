import sqlite3
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from app.config import settings

# Async Engine for FastAPI async handlers
async_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    future=True,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

# Sync Engine for LangGraph node worker background operations
sync_engine = create_engine(
    settings.SYNC_DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False} if "sqlite" in settings.SYNC_DATABASE_URL else {}
)

SyncSessionLocal = sessionmaker(
    bind=sync_engine,
    autocommit=False,
    autoflush=False
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

def init_db():
    Base.metadata.create_all(bind=sync_engine)
    
    # Auto-migrate SQLite columns if table already exists
    if "sqlite" in settings.SYNC_DATABASE_URL:
        try:
            db_file = settings.SYNC_DATABASE_URL.replace("sqlite:///", "")
            if os.path.exists(db_file):
                conn = sqlite3.connect(db_file)
                cur = conn.cursor()
                cur.execute("PRAGMA table_info(research_jobs);")
                existing_cols = {row[1] for row in cur.fetchall()}
                
                columns_to_add = [
                    ("language", "TEXT DEFAULT 'en'"),
                    ("skill_level", "TEXT DEFAULT 'beginner'"),
                    ("study_time_hours_per_week", "TEXT DEFAULT '10-15'"),
                    ("learning_resources_json", "TEXT NULL")
                ]
                for col_name, col_def in columns_to_add:
                    if col_name not in existing_cols:
                        cur.execute(f"ALTER TABLE research_jobs ADD COLUMN {col_name} {col_def};")
                conn.commit()
                conn.close()
        except Exception as e:
            print(f"Database migration notice: {e}")
