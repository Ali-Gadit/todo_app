"""
Middleware configuration for the FastAPI application.
"""

import logging
import time
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from .config import settings

# Configure logging
logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging HTTP requests and responses."""

    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> Response:
        """Process request and log timing."""
        start_time = time.time()

        # Process request
        response = await call_next(request)

        # Calculate duration
        duration = time.time() - start_time

        # Log request details
        logger.info(
            f"{request.method} {request.url.path} - "
            f"Status: {response.status_code} - "
            f"Duration: {duration:.2f}s"
        )

        return response


class RequestValidationMiddleware(BaseHTTPMiddleware):
    """Middleware for handling request validation errors."""

    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> Response:
        """Process request with validation error handling."""
        try:
            return await call_next(request)
        except Exception as exc:
            logger.error(f"Unhandled exception: {exc}")
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal server error"},
            )


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Simple rate limiting middleware.
    In production, use Redis for distributed rate limiting.
    """

    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self._request_counts: dict[str, list[float]] = {}

    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> Response:
        """Check rate limit before processing request."""
        # Skip rate limiting for health check
        if request.url.path in ["/health", "/docs", "/openapi.json"]:
            return await call_next(request)

        client_ip = request.client.host if request.client else "unknown"
        current_time = time.time()

        # Clean old entries (older than 1 minute)
        if client_ip in self._request_counts:
            self._request_counts[client_ip] = [
                t for t in self._request_counts[client_ip]
                if current_time - t < 60
            ]
        else:
            self._request_counts[client_ip] = []

        # Check rate limit
        if len(self._request_counts[client_ip]) >= self.requests_per_minute:
            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Too many requests. Please try again later."
                },
            )

        # Record request
        self._request_counts[client_ip].append(current_time)

        return await call_next(request)


def get_cors_origins() -> list[str]:
    """Get CORS origins from settings, supporting both string and list formats."""
    if isinstance(settings.CORS_ORIGINS, str):
        # Handle comma-separated string
        return [origin.strip() for origin in settings.CORS_ORIGINS.split(",")]
    return settings.CORS_ORIGINS


def setup_middleware(app) -> None:
    """
    Apply all middleware to the FastAPI application.

    Args:
        app: FastAPI application instance
    """
    # Add CORS middleware (configured in main.py as well)
    from fastapi.middleware.cors import CORSMiddleware

    app.add_middleware(
        CORSMiddleware,
        allow_origins=get_cors_origins(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add custom middleware
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(RequestValidationMiddleware)

    if not settings.DEBUG:
        app.add_middleware(
            RateLimitMiddleware,
            requests_per_minute=100,
        )
