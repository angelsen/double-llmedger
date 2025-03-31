import logging

from api import dashboard, health
from core.config import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Create FastAPI app
app = FastAPI(title="DoubleLLMedger API", version="0.1.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,  # Critical for cookie auth
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization", "Cookie"],
    expose_headers=["Set-Cookie"],
)

# Include routers
app.include_router(health.router, prefix=settings.API_V1_PREFIX)
app.include_router(dashboard.router, prefix=settings.API_V1_PREFIX)

# Note: We do NOT create tables here as the frontend (SvelteKit with Drizzle ORM)
# is responsible for managing the database schema.

# Main entry point
if __name__ == "__main__":
    # Silence watchfiles noise
    import logging
    import os

    import uvicorn

    watch_logger = logging.getLogger("watchfiles")
    watch_logger.setLevel(logging.ERROR)

    # Only watch the backend directory for changes
    BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=[BACKEND_DIR],
        log_level="info",
    )
