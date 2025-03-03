from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from .core.database import engine
import logging
from contextlib import asynccontextmanager
import asyncio
# Import all models to ensure they are registered with SQLModel
from .models import user, news, asset, analysis

# Configure logging
logger = logging.getLogger(__name__)


# Create tables
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Creating database tables...")
    await asyncio.to_thread(SQLModel.metadata.create_all, engine)
    logger.info("Database tables created successfully")
    yield  # Shutdown logic (optional) goes after yield

app = FastAPI(title="Financial News Analysis API", lifespan=lifespan)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

# Version endpoint
@app.get("/api/version")
async def version():
    return {
        "version": "0.1.0",
        "environment": "development"
    }

# This code will only run if this file is executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 