"""
ETEx - FastAPI Application Entry Point

This is the main FastAPI application file for the ETEx backend.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="ETEx API",
    description="Engineering Terminology Explorer - Multi-language terminology search and translation system",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
# TODO: Load from environment variables
origins = [
    "http://localhost:5173",  # Vite dev server
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify the API is running.

    Returns:
        dict: Status and version information
    """
    return {
        "status": "healthy",
        "service": "ETEx API",
        "version": "0.1.0"
    }

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint with API information.

    Returns:
        dict: Welcome message and links
    """
    return {
        "message": "Welcome to ETEx API",
        "docs": "/docs",
        "health": "/health",
        "version": "0.1.0"
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    """
    Application startup tasks.
    """
    logger.info("Starting ETEx API...")
    logger.info("FastAPI application initialized")

    # Database is available via dependency injection (get_db)
    # No need to create tables here - use Alembic migrations instead
    logger.info("Database connection configured")

    # TODO: Load configuration from environment
    # TODO: Initialize external API clients

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """
    Application shutdown tasks.
    """
    logger.info("Shutting down ETEx API...")

    # TODO: Close database connections
    # TODO: Cleanup resources

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
