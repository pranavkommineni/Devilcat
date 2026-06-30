"""
main.py
-------
FastAPI application entrypoint, deployed via AppSail (see appsail.config.json).
Performance notes:
  - orjson response class for faster JSON serialization on large dashboard payloads.
  - GZip middleware for map/graph payloads which can be large.
  - CORS restricted to configured portal origins, not wildcard.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import ORJSONResponse

from app.api.v1.router import api_router
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    default_response_class=ORJSONResponse,
    docs_url="/docs" if not settings.is_production else None,
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1024)

app.include_router(api_router, prefix=settings.api_v1_prefix)
