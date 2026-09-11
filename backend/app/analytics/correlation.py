"""
Correlation analysis — Pearson r between AQI and weather variables,
plus seasonal pattern computation.

This module operates on Contract B (district_rollups) data.
"""

from __future__ import annotations
from typing import Optional
import math

from .utils import get_district_history


def pearson_r(x: list[float], y: list[float]) -> Optional[float]:
    """
    Compute the Pearson correlation coefficient between two lists.

    Args:
        x: First variable values.
        y: Second variable values (same length as x).

    Returns:
        Pearson r in [-1, 1], or None if not enough data or zero variance.
    """
    n = len(x)
    if n != len(y) or n < 2:
        return None

    mean_x = sum(x) / n
    mean_y = sum(y) / n

    numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    sum_sq_x = sum((xi - mean_x) ** 2 for xi in x)
    sum_sq_y = sum((yi - mean_y) ** 2 for yi in y)

    denominator = math.sqrt(sum_sq_x * sum_sq_y)
    if denominator == 0:
        return None

    return round(numerator / denominator, 4)


def compute_correlation(district_id: str, variable: str) -> Optional[float]:
    """
    Compute Pearson r between avg_aqi and a weather variable for a district.

    Args:
        district_id: The district to analyze.
        variable: One of 'avg_temp', 'avg_rainfall', 'avg_wind_speed'.

    Returns:
        Pearson r, or None if fewer than 10 data points or insufficient variance.
    """
    history = get_district_history(district_id, range_years=3)

    pairs = []
    for h in history:
        aqi_val = h.avg_aqi
        weather_val = getattr(h, variable, None)
        if aqi_val is not None and weather_val is not None:
            pairs.append((aqi_val, weather_val))

    if len(pairs) < 10:
        return None

    x_vals, y_vals = zip(*pairs)
    return pearson_r(list(x_vals), list(y_vals))


def compute_seasonal_pattern(district_id: str) -> Optional[dict]:
    """
    Compute the average AQI per season for a district over the past 3 years.

    Returns:
        Dict like {"winter": 120.5, "summer": 180.3, "monsoon": 95.0,
                   "post_monsoon": 110.2} or None if no data.
    """
    history = get_district_history(district_id, range_years=3)

    season_aqis: dict[str, list[float]] = {
        "winter": [],
        "summer": [],
        "monsoon": [],
        "post_monsoon": [],
    }

    for h in history:
        if h.avg_aqi is not None and h.season in season_aqis:
            season_aqis[h.season].append(h.avg_aqi)

    result = {}
    for season, aqis in season_aqis.items():
        if aqis:
            result[season] = round(sum(aqis) / len(aqis), 2)
        else:
            result[season] = None

    # Return None if all seasons are None
    if all(v is None for v in result.values()):
        return None

    return result
