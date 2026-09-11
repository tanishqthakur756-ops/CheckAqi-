"""
AQI Calculator — converts pollutant concentrations to AQI values
following the CPCB (Central Pollution Control Board, India) specification.

The AQI is computed using the standard formula:

    AQI = ((I_high - I_low) / (C_high - C_low)) * (C - C_low) + I_low

where:
    C       = pollutant concentration
    C_low   = breakpoint concentration lower bound
    C_high  = breakpoint concentration upper bound
    I_low   = AQI value at C_low
    I_high  = AQI value at C_high

The overall station AQI is the maximum sub-index across all pollutants
present (per CPCB guidelines).

Reference: CPCB "National Air Quality Standards" and AQI methodology.
"""

from __future__ import annotations
from typing import Optional


# =====================================================================
# CPCB AQI Breakpoints
# =====================================================================
# Each entry: (C_low, C_high, I_low, I_high)
# Concentrations are in μg/m³ (except CO which is mg/m³).

BREAKPOINTS = {
    "pm2_5": [
        (0, 30, 0, 50),
        (31, 60, 51, 100),
        (61, 90, 101, 200),
        (91, 120, 201, 300),
        (121, 250, 301, 400),
        (251, 500, 401, 500),
    ],
    "pm10": [
        (0, 50, 0, 50),
        (51, 100, 51, 100),
        (101, 250, 101, 200),
        (251, 350, 201, 300),
        (351, 430, 301, 400),   # FIX: was 420, official CPCB breakpoint is 430
        (431, 600, 401, 500),
    ],
    # FIX: NO2 and SO2 were previously identical (copy-paste bug) -- they are
    # NOT the same pollutant and CPCB gives SO2 a much higher tolerance range.
    "no2": [
        (0, 40, 0, 50),
        (41, 80, 51, 100),
        (81, 180, 101, 200),
        (181, 280, 201, 300),
        (281, 400, 301, 400),
        (401, 600, 401, 500),   # 600 = our closure of CPCB's open-ended "400+"
    ],
    "so2": [
        (0, 40, 0, 50),
        (41, 80, 51, 100),
        (81, 380, 101, 200),
        (381, 800, 201, 300),
        (801, 1600, 301, 400),
        (1601, 2000, 401, 500),  # 2000 = our closure of CPCB's "1600+"
    ],
    "co": [
        (0, 1, 0, 50),
        (1.1, 2, 51, 100),
        (2.1, 10, 101, 200),
        (10.1, 17, 201, 300),
        (17.1, 34, 301, 400),
        (34.1, 50, 401, 500),
    ],
    # O3 FIX: CPCB only defines 8-hr breakpoints through "Poor" (AQI <= 300);
    # Very Poor/Severe legitimately require a 1-hr reading instead of
    # extrapolating the 8-hr scale. Values verified against the official
    # CPCB breakpoint table (µg/m³).
    "o3_8h": [
        (0, 50, 0, 50),
        (51, 100, 51, 100),
        (101, 168, 101, 200),
        (169, 208, 201, 300),
        # No official 8-hr breakpoint beyond 208 -- see calculate_sub_index,
        # which caps an over-208 8-hr reading at "Poor" (300) instead of
        # guessing at Very Poor/Severe from the wrong averaging period.
    ],
    "o3_1h": [
        (209, 748, 301, 400),
        (749, 1000, 401, 500),   # 1000 = our closure of CPCB's "748+"
    ],
}

# AQI category labels and colors
AQI_CATEGORIES = [
    (0, 50, "Good", "green"),
    (51, 100, "Satisfactory", "yellow"),
    (101, 200, "Moderate", "orange"),
    (201, 300, "Poor", "red"),
    (301, 400, "Very Poor", "purple"),
    (401, 500, "Severe", "maroon"),
]


def calculate_sub_index(
    pollutant: str,
    concentration: float,
    o3_period: Optional[str] = None,
) -> Optional[float]:
    """
    Calculate the AQI sub-index for a single pollutant.

    Args:
        pollutant: One of 'pm2_5', 'pm10', 'no2', 'so2', 'co', 'o3'.
        concentration: Pollutant concentration in μg/m³ (or mg/m³ for CO).
        o3_period: For ozone, either '8h' (default) or '1h'.

    Returns:
        AQI sub-index as a float, or None if concentration is None.
    """
    if concentration is None:
        return None

    # Resolve the breakpoint key
    if pollutant == "o3":
        period = o3_period or "8h"
        key = f"o3_{period}"
    else:
        key = pollutant

    if key not in BREAKPOINTS:
        return None

    # FIX: an 8-hr O3 reading above 208 has no defined 8-hr breakpoint --
    # CPCB switches to a 1-hr reading for Very Poor/Severe. Cap at "Poor"
    # (300) rather than silently extrapolating past what the 8-hr standard
    # actually covers.
    if key == "o3_8h" and concentration > 208:
        return 300.0

    breakpoints = BREAKPOINTS[key]

    # Find the matching breakpoint range
    for c_low, c_high, i_low, i_high in breakpoints:
        if c_low <= concentration <= c_high:
            # Linear interpolation
            aqi = ((i_high - i_low) / (c_high - c_low)) * (concentration - c_low) + i_low
            return round(aqi, 1)

    # Concentration exceeds the highest breakpoint
    if concentration > breakpoints[-1][1]:
        return float(breakpoints[-1][3])  # cap at 500

    # FIX: previously fell through to `return 0.0` here unconditionally, which
    # silently reported "Good" (AQI 0) for any concentration below a table's
    # lowest breakpoint. That's harmless for tables starting at 0, but wrong
    # for o3_1h, which intentionally starts at 209 (CPCB doesn't define a
    # low-severity 1-hr O3 breakpoint -- that range is meant to be read via
    # the 8-hr average instead). Only return 0.0 for tables that genuinely
    # start at concentration 0; otherwise there's no defined breakpoint.
    if breakpoints[0][0] == 0:
        return 0.0
    return None


def compute_station_aqi(
    pollutants: dict,
    o3_readings: Optional[dict] = None,
) -> dict:
    """
    Compute the overall station AQI from a set of pollutant concentrations.

    The station AQI is the maximum sub-index across all pollutants present,
    per CPCB guidelines.

    Args:
        pollutants: Dict like {"pm2_5": 45.2, "pm10": 80.0, "no2": 35.0, ...}
        o3_readings: Optional dict with '8h' and/or '1h' O3 concentrations.

    Returns:
        Dict with keys:
            - "aqi": overall AQI (float or None)
            - "dominant_pollutant": the pollutant with the highest sub-index
            - "sub_indices": dict of pollutant -> sub-index
    """
    sub_indices = {}

    # Process O3 readings first (they may come via o3_readings dict
    # even if "o3" is not in the pollutants dict)
    if o3_readings:
        for period, conc in o3_readings.items():
            if conc is not None:
                idx = calculate_sub_index("o3", conc, o3_period=period)
                if idx is not None:
                    sub_indices[f"o3_{period}"] = idx

    for pollutant, concentration in pollutants.items():
        if concentration is None:
            continue
        if pollutant == "o3":
            # O3 with explicit o3_readings already processed above;
            # only use the plain concentration if no o3_readings were given
            if not o3_readings:
                idx = calculate_sub_index("o3", concentration)
                if idx is not None:
                    sub_indices["o3_8h"] = idx
        else:
            idx = calculate_sub_index(pollutant, concentration)
            if idx is not None:
                sub_indices[pollutant] = idx

    if not sub_indices:
        return {
            "aqi": None, "dominant_pollutant": None, "sub_indices": {},
            "category": "Unknown", "color": "#808080", "is_cpcb_compliant": False,
        }

    # Station AQI = max sub-index
    dominant = max(sub_indices, key=sub_indices.get)
    overall_aqi = sub_indices[dominant]
    category, _ = get_aqi_category(overall_aqi)
    color = aqi_to_color(overall_aqi)

    # FIX: this compliance flag was dropped in an earlier revision. CPCB
    # requires >=3 pollutants, including at least one particulate (PM2.5/PM10),
    # before an AQI reading counts as fully compliant rather than a partial
    # single-sensor estimate. The frontend uses this to badge "Verified" vs
    # "Estimated" readings -- without it, a 1-pollutant station's guess looks
    # identical to a fully-instrumented station's reading.
    pm_keys = {"pm2_5", "pm10"}
    has_pm = bool(pm_keys.intersection(sub_indices.keys()))
    is_compliant = len(sub_indices) >= 3 and has_pm

    return {
        "aqi": overall_aqi,
        "dominant_pollutant": dominant,
        "sub_indices": sub_indices,
        "category": category,
        "color": color,
        "is_cpcb_compliant": is_compliant,
    }


def get_aqi_category(aqi: float) -> tuple[str, str]:
    """
    Return the (label, color) for a given AQI value.

    Args:
        aqi: AQI value (0–500).

    Returns:
        Tuple of (category_name, color_name).
    """
    if aqi is None:
        return ("Unknown", "gray")

    for low, high, label, color in AQI_CATEGORIES:
        if low <= aqi <= high:
            return (label, color)

    # AQI above 500
    return ("Severe", "maroon")


def aqi_to_color(aqi: Optional[float]) -> str:
    """Map an AQI value to a hex color for frontend use."""
    if aqi is None:
        return "#808080"  # gray for no data

    _, color_name = get_aqi_category(aqi)
    color_map = {
        "green": "#2ECC71",
        "yellow": "#F1C40F",
        "orange": "#E67E22",
        "red": "#E74C3C",
        "purple": "#8E44AD",
        "maroon": "#C0392B",
        "gray": "#808080",
    }
    return color_map.get(color_name, "#808080")
