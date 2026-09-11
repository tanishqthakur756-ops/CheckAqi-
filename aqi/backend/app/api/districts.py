"""
District API endpoints.

All responses conform to the contracts defined in schemas.py:
  - Contract B: DistrictRollup
  - Contract C: HistoryResponse
"""

from datetime import date, timedelta
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from ..db import get_db_session
from ..models import District, Station, DailyReading, DistrictRollup
from ..schemas import (
    DistrictMeta,
    DistrictWithLatestAQI,
    DistrictDetailResponse,
    HistoryResponse,
    DistrictRollup as DistrictRollupSchema,
    CorrelationResponse,
)
from ..analytics.correlation import compute_correlation, compute_seasonal_pattern
from ..analytics.utils import get_district_history_range, get_imd_season

router = APIRouter(prefix="/api/districts", tags=["districts"])


@router.get("/", response_model=list[DistrictWithLatestAQI])
def list_districts(db: Session = Depends(get_db_session)):
    """
    List all districts with their latest AQI reading.

    Returns Contract B-like data (latest rollup per district).
    """
    districts = db.query(District).all()
    results = []

    for d in districts:
        # Get the latest rollup for this district
        latest_rollup = (
            db.query(DistrictRollup)
            .filter(DistrictRollup.district_id == d.district_id)
            .order_by(DistrictRollup.date.desc())
            .first()
        )

        # Get the latest daily reading for this district
        latest_reading = (
            db.query(DailyReading)
            .join(Station, DailyReading.station_id == Station.station_id)
            .filter(Station.district_id == d.district_id)
            .order_by(DailyReading.date.desc())
            .first()
        )

        latest_aqi = None
        latest_date = None
        coverage_type = None

        if latest_rollup:
            latest_aqi = latest_rollup.avg_aqi
            latest_date = latest_rollup.date.strftime("%Y-%m-%d") if latest_rollup.date else None
            coverage_type = latest_rollup.coverage_type
        elif latest_reading:
            latest_aqi = latest_reading.aqi
            latest_date = latest_reading.date.strftime("%Y-%m-%d") if latest_reading.date else None
            coverage_type = "station"

        results.append(DistrictWithLatestAQI(
            district_id=d.district_id,
            name=d.name,
            state=d.state,
            latitude=d.latitude,
            longitude=d.longitude,
            latest_aqi=latest_aqi,
            latest_date=latest_date,
            coverage_type=coverage_type,
        ))

    return results


@router.get("/{district_id}", response_model=DistrictDetailResponse)
def district_detail(district_id: str, db: Session = Depends(get_db_session)):
    """
    Get district metadata and active station count.
    """
    district = db.query(District).filter(District.district_id == district_id).first()
    if not district:
        raise HTTPException(status_code=404, detail=f"District '{district_id}' not found")

    active_count = (
        db.query(Station)
        .filter(Station.district_id == district_id)
        .filter(Station.is_active == True)
        .count()
    )

    return DistrictDetailResponse(
        meta=DistrictMeta(
            district_id=district.district_id,
            lgd_code=district.lgd_code,
            name=district.name,
            state=district.state,
            latitude=district.latitude,
            longitude=district.longitude,
        ),
        active_station_count=active_count,
    )


@router.get("/{district_id}/history", response_model=HistoryResponse)
def district_history(
    district_id: str,
    range: str = "1y",
    db: Session = Depends(get_db_session),
):
    """
    Get district history (Contract C).

    Returns rollup rows for the specified date range.
    """
    # Validate range — don't trust raw input
    if range not in ("30d", "90d", "1y"):
        range = "1y"

    # Verify district exists
    district = db.query(District).filter(District.district_id == district_id).first()
    if not district:
        raise HTTPException(status_code=404, detail=f"District '{district_id}' not found")

    # Fetch rollups for the range
    rollups = get_district_history_range(district_id, range)

    data = [
        DistrictRollupSchema(
            district_id=r.district_id,
            date=r.date.strftime("%Y-%m-%d") if r.date else "",
            avg_aqi=r.avg_aqi,
            max_aqi=r.max_aqi,
            avg_temp=r.avg_temp,
            avg_rainfall=r.avg_rainfall,
            avg_wind=r.avg_wind,
            season=r.season,
            station_count=r.station_count,
            coverage_type=r.coverage_type,
        )
        for r in rollups
    ]

    return HistoryResponse(
        district_id=district_id,
        range=range,
        data=data,
    )


@router.get("/{district_id}/correlation", response_model=CorrelationResponse)
def district_correlation(
    district_id: str,
    db: Session = Depends(get_db_session),
):
    """
    Get correlation data for a district.

    Returns seasonal pattern and Pearson r correlations between
    AQI and weather variables.
    """
    district = db.query(District).filter(District.district_id == district_id).first()
    if not district:
        raise HTTPException(status_code=404, detail=f"District '{district_id}' not found")

    seasonal = compute_seasonal_pattern(district_id)
    # FIX: this previously read "avg_temp" and mislabeled it wind_correlation --
    # avg_wind didn't exist in district_rollups at all, so wind_correlation
    # was silently reporting a temperature correlation instead.
    wind_corr = compute_correlation(district_id, "avg_wind")
    rain_corr = compute_correlation(district_id, "avg_rainfall")

    return CorrelationResponse(
        seasonal_pattern=seasonal,
        wind_correlation=wind_corr,
        rainfall_correlation=rain_corr,
    )
