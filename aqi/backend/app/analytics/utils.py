"""
Shared analytics utilities: IST date handling, IMD season classification,
safe statistics, and district/station lookups.
"""

from __future__ import annotations
from datetime import datetime, date, timedelta
from typing import Optional
import math

from ..db import get_db
from ..models import District, Station, DailyReading, DistrictRollup


# =====================================================================
# IST date helpers
# =====================================================================
def today_ist() -> str:
    """Return today's date in IST as 'YYYY-MM-DD'."""
    from datetime import timezone, timedelta
    ist = timezone(timedelta(hours=5, minutes=30))
    return datetime.now(ist).strftime("%Y-%m-%d")


def parse_date(date_str: str) -> date:
    """Parse a 'YYYY-MM-DD' string into a date object."""
    return datetime.strptime(date_str, "%Y-%m-%d").date()


# =====================================================================
# IMD season classification
# =====================================================================
def get_imd_season(date_str: str) -> str:
    """
    Classify a date into an IMD season.

    IMD seasons:
      - winter:      December, January, February
      - summer:      March, April, May
      - monsoon:     June, July, August, September
      - post_monsoon: October, November
    """
    d = parse_date(date_str)
    month = d.month

    if month in (12, 1, 2):
        return "winter"
    elif month in (3, 4, 5):
        return "summer"
    elif month in (6, 7, 8, 9):
        return "monsoon"
    else:  # 10, 11
        return "post_monsoon"


# =====================================================================
# Safe statistics
# =====================================================================
def safe_mean(values: list[float]) -> Optional[float]:
    """Return the mean of a list, or None if empty."""
    if not values:
        return None
    return round(sum(values) / len(values), 2)


def safe_max(values: list[float]) -> Optional[float]:
    """Return the max of a list, or None if empty."""
    if not values:
        return None
    return max(values)


# =====================================================================
# DB lookup helpers
# =====================================================================
def all_district_ids() -> list[str]:
    """Return all district_id values from the database."""
    with get_db() as db:
        rows = db.query(District.district_id).all()
        return [r[0] for r in rows]


def all_district_centroids() -> list[dict]:
    """Return all districts with their centroid coordinates."""
    with get_db() as db:
        rows = db.query(District.district_id, District.latitude, District.longitude).all()
        return [
            {"district_id": r[0], "lat": r[1], "lon": r[2]}
            for r in rows
            if r[1] is not None and r[2] is not None
        ]


def get_readings(district_id: str, date_str: str) -> list:
    """
    Get all daily_readings for a district on a given date.
    Joins through stations to filter by district.
    """
    d = parse_date(date_str)
    with get_db() as db:
        readings = (
            db.query(DailyReading)
            .join(Station, DailyReading.station_id == Station.station_id)
            .filter(Station.district_id == district_id)
            .filter(DailyReading.date == d)
            .all()
        )
        return readings


def upsert_rollup(district_id: str, date_str: str, **kwargs) -> None:
    """Insert or update a district_rollups row (Contract B)."""
    d = parse_date(date_str)
    with get_db() as db:
        existing = (
            db.query(DistrictRollup)
            .filter(DistrictRollup.district_id == district_id)
            .filter(DistrictRollup.date == d)
            .first()
        )
        if existing:
            for key, value in kwargs.items():
                setattr(existing, key, value)
        else:
            rollup = DistrictRollup(
                district_id=district_id,
                date=d,
                **kwargs,
            )
            db.add(rollup)
        db.commit()


def get_district_history(district_id: str, range_years: int = 3) -> list:
    """
    Get district rollup history for the past `range_years` years.
    Returns list of DistrictRollup objects ordered by date.
    """
    today = date.today()
    start_date = today - timedelta(days=range_years * 365)
    with get_db() as db:
        history = (
            db.query(DistrictRollup)
            .filter(DistrictRollup.district_id == district_id)
            .filter(DistrictRollup.date >= start_date)
            .filter(DistrictRollup.date <= today)
            .order_by(DistrictRollup.date)
            .all()
        )
        return history


def get_district_history_range(district_id: str, range_str: str) -> list:
    """
    Get district rollup history for a specific range string.
    range_str: '30d', '90d', or '1y'
    """
    today = date.today()
    if range_str == "30d":
        start_date = today - timedelta(days=30)
    elif range_str == "90d":
        start_date = today - timedelta(days=90)
    elif range_str == "1y":
        start_date = today - timedelta(days=365)
    else:
        start_date = today - timedelta(days=365)

    with get_db() as db:
        history = (
            db.query(DistrictRollup)
            .filter(DistrictRollup.district_id == district_id)
            .filter(DistrictRollup.date >= start_date)
            .filter(DistrictRollup.date <= today)
            .order_by(DistrictRollup.date)
            .all()
        )
        return history
