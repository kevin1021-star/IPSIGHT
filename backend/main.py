"""
CIPHER-SENTINEL: FastAPI Application Entry Point
SIH26160 | NTRO | AI-Powered IPsec VPN Protocol Analyzer
"""

import sys
import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Ensure the core engine is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.database import engine, Base
from backend.routers import auth, assessments, reports, dashboard

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create DB tables on startup."""
    logger.info("CIPHER-SENTINEL API starting — creating tables if needed...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database ready.")
    yield
    logger.info("CIPHER-SENTINEL API shutting down.")


app = FastAPI(
    title="CIPHER-SENTINEL API",
    description=(
        "AI-Powered IPsec VPN Protocol Analyzer & Security Assessment Framework. "
        "SIH26160 | National Technical Research Organisation (NTRO)"
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# ---------------------------------------------------------------------------
# CORS — allow all for development; tighten for production
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(auth.router)
app.include_router(assessments.router)
app.include_router(reports.router)
app.include_router(dashboard.router)


# ---------------------------------------------------------------------------
# Global exception handler
# ---------------------------------------------------------------------------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"},
    )


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------
@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "service": "CIPHER-SENTINEL", "version": "1.0.0"}


@app.get("/", tags=["Root"])
async def root():
    return {
        "service": "CIPHER-SENTINEL API",
        "docs": "/docs",
        "health": "/health",
    }
