from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from database.config import settings
import asyncio
import logging

logger = logging.getLogger(__name__)

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
# Initialize database models with retry logic
# -------------------------
async def init_models(max_retries=5, retry_delay=2):
    """Initialize database with retry logic for Kubernetes startup"""
    for attempt in range(max_retries):
        try:
            logger.info(f"Attempting to connect to database (attempt {attempt + 1}/{max_retries})...")
            async with engine.begin() as conn:
                # Drop all tables (optional, only for dev)
                # await conn.run_sync(Base.metadata.drop_all)
                await conn.run_sync(Base.metadata.create_all)
            logger.info("Database connection successful and tables created!")
            return
        except Exception as e:
            logger.warning(f"Database connection attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
            else:
                logger.error("Max retries reached. Could not connect to database.")
                raise

# -------------------------
# Dependency for FastAPI
# -------------------------
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session