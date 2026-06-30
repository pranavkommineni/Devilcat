from fastapi import APIRouter

from app.api.v1.endpoints import auth, fir, health

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(fir.router)

# Phase 3+ endpoints (victims, crime, cdr, finance, gis, network_analysis,
# predictive, conversational_ai, admin) register here as they're built —
# keeps main.py untouched as the surface area grows.
