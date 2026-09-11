"""
Pydantic schemas — the data contracts (A, B, C) that every part of the system
produces or consumes.

Contract A: DailyReadingIn   — output of ingestion, input to DB
Contract B: DistrictRollup   — output of processing, input to API
Contract C: HistoryResponse  — API response for GET /api/districts/{id}/history
"""

from __future__ import annotations
from datetime import date
from typing import Optional, Literal

from pydantic import BaseModel, Field


# =====================================================================
# Contract A: one merged daily reading (output of ingestion, input to DB)
# =====================================================================
class DailyReadingIn(BaseModel):
    station_id: str
    district_id: str
    date: str  # "YYYY-MM-DD"
    aqi: Optional[float] = None
    pm2_5: Optional[float] = None
    pm10: Optional[float] = None
    no2: Optional[float] = None
    temperature: Optional[float] = None
    rainfall_mm: Optional[float] = None
    wind_speed_kmh: Optional[float] = None
    data_type: Literal["observed", "estimated"] = "observed"
    source: str


class DailyReadingOut(DailyReadingIn):
    fetched_at: Optional[str] = None


# =====================================================================
# Contract B: one district rollup row (output of processing, input to API)
# =====================================================================
class DistrictRollup(BaseModel):
    district_id: str
    date: str  # "YYYY-MM-DD"
    avg_aqi: Optional[float] = None
    max_aqi: Optional[float] = None
    avg_temp: Optional[float] = None
    avg_rainfall: Optional[float] = None
    avg_wind: Optional[float] = None
    season: Literal["winter", "summer", "monsoon", "post_monsoon"]
    station_count: int = 0
    coverage_type: Literal["station", "interpolated", "no_data"]


# =====================================================================
# Contract C: API response shape for GET /api/districts/{id}/history
# =====================================================================
class HistoryResponse(BaseModel):
    district_id: str
    range: Literal["30d", "90d", "1y"]
    data: list[DistrictRollup]


# =====================================================================
# Supporting schemas for other endpoints
# =====================================================================
class DistrictMeta(BaseModel):
    district_id: str
    lgd_code: Optional[str] = None
    name: str
    state: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class DistrictWithLatestAQI(BaseModel):
    district_id: str
    name: str
    state: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    latest_aqi: Optional[float] = None
    latest_date: Optional[str] = None
    coverage_type: Optional[str] = None


class DistrictDetailResponse(BaseModel):
    meta: DistrictMeta
    active_station_count: int


class SourceInfo(BaseModel):
    source_name: str
    source_url: Optional[str] = None
    license_note: Optional[str] = None
    last_synced_at: Optional[str] = None


class CorrelationResponse(BaseModel):
    seasonal_pattern: Optional[dict] = None
    wind_correlation: Optional[float] = None
    rainfall_correlation: Optional[float] = None
