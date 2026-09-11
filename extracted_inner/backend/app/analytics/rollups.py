"""
District rollups — turns many station readings into one Contract B row
per district/day.

This module is the bridge between Contract A (daily_readings) and
Contract B (district_rollups).
"""

from __future__ import annotations
from typing import Optional
from dataclasses import dataclass

from .utils import (
    all_district_ids,
    get_readings,
    upsert_rollup,
    get_imd_season,
    safe_mean,
    safe_max,
)


@dataclass
class RollupSummary:
    """Container for the fields that make up a Contract B row."""
    avg_aqi: Optional[float]
    max_aqi: Optional[float]
    avg_temp: Optional[float]
    avg_rainfall: Optional[float]
    season: str
    station_count: int
    coverage_type: str


def summarize(readings: list) -> dict:
    """
    Summarize a list of DailyReading objects into a Contract B dict.

    Args:
        readings: List of DailyReading ORM objects for one district on one date.

    Returns:
        Dict matching Contract B (minus district_id and date, which are
        added by the caller).
    """
    if not readings:
        return {
            "avg_aqi": None,
            "max_aqi": None,
            "avg_temp": None,
            "avg_rainfall": None,
            "avg_wind": None,
            "season": get_imd_season(_today_str()),
            "station_count": 0,
            "coverage_type": "no_data",
        }

    valid_aqi = [r.aqi for r in readings if r.aqi is not None]
    valid_temp = [r.temperature for r in readings if r.temperature is not None]
    valid_rain = [r.rainfall_mm for r in readings if r.rainfall_mm is not None]
    # FIX: wind_speed_kmh was captured in daily_readings (Contract A) but
    # never rolled up, so district_rollups had no wind field at all -- the
    # "wind_correlation" API endpoint was silently correlating against
    # avg_temp instead. See analytics/correlation.py and api/districts.py.
    valid_wind = [r.wind_speed_kmh for r in readings if r.wind_speed_kmh is not None]

    # Determine coverage type:
    #   "station"     — at least one observed reading
    #   "interpolated" — all readings are estimated (no observed data)
    #   "no_data"     — no readings at all (handled above)
    has_observed = any(r.data_type == "observed" for r in readings)
    coverage_type = "station" if has_observed else "interpolated"

    return {
        "avg_aqi": safe_mean(valid_aqi),
        "max_aqi": safe_max(valid_aqi),
        "avg_temp": safe_mean(valid_temp),
        "avg_rainfall": safe_mean(valid_rain),
        "avg_wind": safe_mean(valid_wind),
        "season": get_imd_season(_reading_date_str(readings[0])),
        "station_count": len(readings),
        "coverage_type": coverage_type,
    }


def _today_str() -> str:
    """Return today's date as YYYY-MM-DD (fallback for no_data case)."""
    from datetime import datetime, timezone, timedelta
    ist = timezone(timedelta(hours=5, minutes=30))
    return datetime.now(ist).strftime("%Y-%m-%d")


def _reading_date_str(reading) -> str:
    """Extract date string from a DailyReading object."""
    if hasattr(reading, "date") and reading.date is not None:
        if isinstance(reading.date, str):
            return reading.date
        return reading.date.strftime("%Y-%m-%d")
    return _today_str()


def recompute_district_rollups(date_str: str) -> int:
    """
    Recompute district rollups for a given date.

    Iterates over all districts, fetches their station readings for the date,
    summarizes them, and upserts a Contract B row.

    Args:
        date_str: Date in 'YYYY-MM-DD' format.

    Returns:
        Number of districts processed.
    """
    district_ids = all_district_ids()
    count = 0

    for district_id in district_ids:
        readings = get_readings(district_id, date_str)
        summary = summarize(readings)
        upsert_rollup(district_id, date_str, **summary)
        count += 1

    return count


def recompute_district_rollups_range(start_date: str, end_date: str) -> int:
    """
    Recompute district rollups for a date range (inclusive).

    Args:
        start_date: Start date in 'YYYY-MM-DD' format.
        end_date: End date in 'YYYY-MM-DD' format.

    Returns:
        Number of district-days processed.
    """
    from datetime import datetime, timedelta

    start = datetime.strptime(start_date, "%Y-%m-%d").date()
    end = datetime.strptime(end_date, "%Y-%m-%d").date()

    total = 0
    current = start
    while current <= end:
        total += recompute_district_rollups(current.strftime("%Y-%m-%d"))
        current += timedelta(days=1)

    return total
