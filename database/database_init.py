from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from database.config import settings

# -------------------------
# Database configuration
# -------------------------
DATABASE_URL = settings.DATABASE_URL

# Base class for models
Base = declarative_base()

# Create engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

# -------------------------
# Initialize database models
# -------------------------
async def init_models():
    async with engine.begin() as conn:
        # Drop all tables (optional, only for dev)
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

# -------------------------
# Dependency for FastAPI
# -------------------------
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session