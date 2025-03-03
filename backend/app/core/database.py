from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel
from .config import settings
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Create SQLAlchemy engine
try:
    engine = create_engine(settings.DATABASE_URL)
    logger.info(f"Database connection established: {settings.DATABASE_URL}")
except Exception as e:
    logger.error(f"Database connection failed: {str(e)}")
    raise

# Create session factory
SessionLocal = Session(bind=engine)

# Dependency to get DB session
def get_session():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close() 