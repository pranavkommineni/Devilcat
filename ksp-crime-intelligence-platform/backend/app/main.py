"""
KSP Crime Intelligence Platform - FastAPI Backend
Main application entry point
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.catalyst_client import catalyst_client

# Import routers
from app.api.v1 import endpoints


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown event handlers"""
    # Startup
    print(f"Starting {settings.APP_NAME}...")
    await catalyst_client.initialize()
    yield
    # Shutdown
    print("Shutting down...")
    await catalyst_client.close()


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="Crime Intelligence Platform API",
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": settings.APP_NAME}


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "KSP Crime Intelligence Platform API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
    }


# Include API routers
app.include_router(endpoints.fir.router, prefix="/api/v1/fir", tags=["FIR Management"])
app.include_router(
    endpoints.suspects.router, prefix="/api/v1/suspects", tags=["Suspect Management"]
)
app.include_router(
    endpoints.victims.router, prefix="/api/v1/victims", tags=["Victim Management"]
)
app.include_router(
    endpoints.crimes.router, prefix="/api/v1/crimes", tags=["Crime Data"]
)
app.include_router(
    endpoints.auth.router, prefix="/api/v1/auth", tags=["Authentication"]
)
app.include_router(
    endpoints.network_analysis.router,
    prefix="/api/v1/network",
    tags=["Network Analysis"],
)
app.include_router(
    endpoints.predictive.router,
    prefix="/api/v1/predictive",
    tags=["Predictive Analytics"],
)
app.include_router(
    endpoints.conversational_ai.router,
    prefix="/api/v1/ai",
    tags=["Conversational AI"],
)
app.include_router(endpoints.admin.router, prefix="/api/v1/admin", tags=["Admin"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
