"""
Main application entry point.

This module initializes the FastAPI application, sets up middleware,
configures CORS, and registers all API routes.
"""
import logging
import os
import time
from contextlib import asynccontextmanager

import uvicorn

# Import routers
from api import dashboard, health

# Import configuration
from core.config import settings
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# Application lifespan context manager for startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager.

    Handles startup and shutdown events for the application.
    Use this to initialize and cleanup resources.
    """
    # Startup: Run before the application starts accepting requests
    logger.info("Starting application...")

    # This line separates startup from shutdown logic
    yield

    # Shutdown: Run when the application is shutting down
    logger.info("Shutting down application...")


# Custom middleware for request logging and timing
class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging requests and measuring response time."""

    async def dispatch(self, request: Request, call_next):
        """Process the request and log details."""
        start_time = time.time()
        request_id = request.headers.get("X-Request-ID", "unknown")

        # Log the incoming request
        logger.debug(
            f"Request: {request_id} - {request.method} {request.url.path}"
        )

        try:
            # Process the request
            response = await call_next(request)

            # Calculate and add processing time to the response headers
            process_time = time.time() - start_time
            response.headers["X-Process-Time"] = f"{process_time:.4f}"

            # Log the response
            logger.debug(
                f"Response: {request_id} - {response.status_code} - {process_time:.4f}s"
            )

            return response
        except Exception as e:
            # Log exceptions
            logger.exception(f"Error processing request {request_id}: {str(e)}")

            # Return a JSON error response
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "Internal server error"},
            )


# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
    lifespan=lifespan,
)

# Add custom middleware
app.add_middleware(LoggingMiddleware)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["Content-Type", "Authorization", "Cookie"],
    expose_headers=["Set-Cookie"],
)

# Include routers with version prefix
app.include_router(health.router, prefix=settings.API_V1_PREFIX)
app.include_router(dashboard.router, prefix=settings.API_V1_PREFIX)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs": "/docs",
    }


# Main entry point for development server
if __name__ == "__main__":
    # Silence watchfiles noise in development
    watch_logger = logging.getLogger("watchfiles")
    watch_logger.setLevel(logging.ERROR)

    # Only watch the backend directory for changes
    BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))

    # Run the development server
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        reload_dirs=[BACKEND_DIR],
        log_level=settings.LOG_LEVEL.lower(),
    )
