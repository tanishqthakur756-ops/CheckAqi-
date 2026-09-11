"""
FastAPI application — India AQI–Weather Tracker backend.

Run with:
    uvicorn app.main:app --reload

All endpoints return JSON conforming to the contracts defined in schemas.py.
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .api.districts import router as districts_router
from .api.sources import router as sources_router
from .db import init_db

app = FastAPI(
    title="India AQI–Weather Tracker API",
    description="Real-time and historical AQI + weather data for Indian districts.",
    version="1.0.0",
)

# CORS — allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(districts_router)
app.include_router(sources_router)


@app.on_event("startup")
def on_startup():
    """Initialize the database on startup."""
    init_db()


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "aqi-tracker-api"}


@app.get("/api")
def api_info():
    """API info (moved off "/" so the dashboard can be served there instead)."""
    return {
        "name": "India AQI–Weather Tracker API",
        "version": "1.0.0",
        "endpoints": {
            "districts": "/api/districts",
            "district_detail": "/api/districts/{district_id}",
            "district_history": "/api/districts/{district_id}/history?range=1y",
            "district_correlation": "/api/districts/{district_id}/correlation",
            "sources": "/api/sources",
            "health": "/health",
        },
    }


# Serve the dashboard frontend at "/". Mounted last so it doesn't shadow the
# /api/* and /health routes above.
_static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/", StaticFiles(directory=_static_dir, html=True), name="static")
