"""
Unit tests for the AQI calculator (Part 3).

These tests verify the CPCB breakpoint logic with known concentrations
and expected AQI values. They run standalone — no database needed.
"""

import pytest
from app.analytics.aqi_calculator import (
    calculate_sub_index,
    compute_station_aqi,
    get_aqi_category,
    aqi_to_color,
    BREAKPOINTS,
)


# =====================================================================
# calculate_sub_index tests
# =====================================================================
class TestCalculateSubIndex:
    """Tests for single-pollutant AQI sub-index calculation."""

    def test_pm25_good(self):
        """PM2.5 at 15 μg/m³ should be in the 'Good' range (AQI ~25)."""
        result = calculate_sub_index("pm2_5", 15.0)
        assert result is not None
        assert 0 <= result <= 50

    def test_pm25_satisfactory(self):
        """PM2.5 at 45 μg/m³ should be in the 'Satisfactory' range (AQI ~75)."""
        result = calculate_sub_index("pm2_5", 45.0)
        assert result is not None
        assert 51 <= result <= 100

    def test_pm25_moderate(self):
        """PM2.5 at 75 μg/m³ should be in the 'Moderate' range (AQI ~150)."""
        result = calculate_sub_index("pm2_5", 75.0)
        assert result is not None
        assert 101 <= result <= 200

    def test_pm25_poor(self):
        """PM2.5 at 105 μg/m³ should be in the 'Poor' range (AQI ~205)."""
        result = calculate_sub_index("pm2_5", 105.0)
        assert result is not None
        assert 201 <= result <= 300

    def test_pm25_very_poor(self):
        """PM2.5 at 150 μg/m³ should be in the 'Very Poor' range (AQI ~325)."""
        result = calculate_sub_index("pm2_5", 150.0)
        assert result is not None
        assert 301 <= result <= 400

    def test_pm25_severe(self):
        """PM2.5 at 300 μg/m³ should be in the 'Severe' range (AQI ~450)."""
        result = calculate_sub_index("pm2_5", 300.0)
        assert result is not None
        assert 401 <= result <= 500

    def test_pm25_at_breakpoint_boundary(self):
        """At exactly 30 μg/m³, AQI should be exactly 50."""
        result = calculate_sub_index("pm2_5", 30.0)
        assert result == 50.0

    def test_pm25_at_60_boundary(self):
        """At exactly 60 μg/m³, AQI should be exactly 100."""
        result = calculate_sub_index("pm2_5", 60.0)
        assert result == 100.0

    def test_pm25_zero(self):
        """At 0 μg/m³, AQI should be 0."""
        result = calculate_sub_index("pm2_5", 0.0)
        assert result == 0.0

    def test_pm25_none(self):
        """None concentration should return None."""
        result = calculate_sub_index("pm2_5", None)
        assert result is None

    def test_pm25_exceeds_max(self):
        """Concentration above 500 should cap at 500."""
        result = calculate_sub_index("pm2_5", 600.0)
        assert result == 500.0

    def test_pm10_good(self):
        """PM10 at 30 μg/m³ should be in the 'Good' range."""
        result = calculate_sub_index("pm10", 30.0)
        assert result is not None
        assert 0 <= result <= 50

    def test_pm10_moderate(self):
        """PM10 at 150 μg/m³ should be in the 'Moderate' range."""
        result = calculate_sub_index("pm10", 150.0)
        assert result is not None
        assert 101 <= result <= 200

    def test_no2_good(self):
        """NO2 at 20 μg/m³ should be in the 'Good' range."""
        result = calculate_sub_index("no2", 20.0)
        assert result is not None
        assert 0 <= result <= 50

    def test_no2_poor(self):
        """NO2 at 200 μg/m³ should be in the 'Poor' range."""
        result = calculate_sub_index("no2", 200.0)
        assert result is not None
        assert 201 <= result <= 300

    def test_so2_good(self):
        """SO2 at 20 μg/m³ should be in the 'Good' range."""
        result = calculate_sub_index("so2", 20.0)
        assert result is not None
        assert 0 <= result <= 50

    def test_co_good(self):
        """CO at 0.5 mg/m³ should be in the 'Good' range."""
        result = calculate_sub_index("co", 0.5)
        assert result is not None
        assert 0 <= result <= 50

    def test_co_severe(self):
        """CO at 40 mg/m³ should be in the 'Severe' range."""
        result = calculate_sub_index("co", 40.0)
        assert result is not None
        assert 401 <= result <= 500

    def test_o3_8h_good(self):
        """O3 (8h) at 30 μg/m³ should be in the 'Good' range."""
        result = calculate_sub_index("o3", 30.0, o3_period="8h")
        assert result is not None
        assert 0 <= result <= 50

    def test_o3_1h_good(self):
        """O3 (1h) at 50 μg/m³ should be in the 'Good' range."""
        result = calculate_sub_index("o3", 50.0, o3_period="1h")
        assert result is not None
        assert 0 <= result <= 50

    def test_o3_1h_below_severe_threshold_has_no_breakpoint(self):
        """FIX: CPCB only defines 1-hr O3 breakpoints for Very Poor/Severe
        (>208 ug/m3) -- a "moderate" 1-hr reading has no official mapping,
        since low-severity O3 is meant to be read via the 8-hr average
        instead. This replaces the old test, which assumed a full 0-500
        1-hr table that didn't match the real CPCB spec."""
        result = calculate_sub_index("o3", 120.0, o3_period="1h")
        assert result is None

    def test_o3_1h_very_poor(self):
        """O3 (1h) at 400 ug/m3 should fall in the Very Poor range."""
        result = calculate_sub_index("o3", 400.0, o3_period="1h")
        assert result is not None
        assert 301 <= result <= 400

    def test_o3_8h_caps_at_poor_above_208(self):
        """FIX: an 8-hr O3 reading above 208 has no defined 8-hr breakpoint;
        it must cap at 'Poor' (300) rather than extrapolate into Very
        Poor/Severe, since that requires a 1-hr reading instead."""
        result = calculate_sub_index("o3", 300.0, o3_period="8h")
        assert result == 300.0
        assert 101 <= result <= 200

    def test_o3_default_period_is_8h(self):
        """Without specifying period, O3 should use 8h breakpoints."""
        result_8h = calculate_sub_index("o3", 60.0)
        result_explicit = calculate_sub_index("o3", 60.0, o3_period="8h")
        assert result_8h == result_explicit

    def test_unknown_pollutant(self):
        """Unknown pollutant should return None."""
        result = calculate_sub_index("xyz", 50.0)
        assert result is None


# =====================================================================
# compute_station_aqi tests
# =====================================================================
class TestComputeStationAQI:
    """Tests for overall station AQI computation."""

    def test_single_pollutant(self):
        """With one pollutant, AQI should equal that pollutant's sub-index."""
        result = compute_station_aqi({"pm2_5": 75.0})
        assert result["aqi"] is not None
        assert 101 <= result["aqi"] <= 200
        assert result["dominant_pollutant"] == "pm2_5"

    def test_multiple_pollutants_takes_max(self):
        """Station AQI should be the max sub-index across pollutants."""
        result = compute_station_aqi({"pm2_5": 30.0, "pm10": 150.0})
        # pm2_5 at 30 → AQI 50, pm10 at 150 → AQI ~150
        assert result["aqi"] is not None
        assert result["aqi"] >= 100  # pm10 should dominate
        assert result["dominant_pollutant"] == "pm10"

    def test_all_none(self):
        """All None concentrations should return None AQI."""
        result = compute_station_aqi({"pm2_5": None, "pm10": None})
        assert result["aqi"] is None
        assert result["dominant_pollutant"] is None

    def test_empty_dict(self):
        """Empty pollutants dict should return None AQI."""
        result = compute_station_aqi({})
        assert result["aqi"] is None

    def test_with_o3_readings(self):
        """O3 readings with explicit periods should be handled."""
        result = compute_station_aqi(
            {"pm2_5": 30.0},
            # FIX: 180 has no defined 1-hr breakpoint (real CPCB range starts
            # at 209) so it's correctly dropped; the 8-hr reading dominates.
            o3_readings={"8h": 120.0, "1h": 180.0},
        )
        assert result["aqi"] is not None
        # pm2_5 at 30 -> 50, o3_8h at 120 -> ~129 (o3_1h at 180 has no breakpoint, excluded)
        assert result["aqi"] >= 100
        assert "o3_1h" not in result["sub_indices"]

    def test_sub_indices_populated(self):
        """Sub-indices dict should contain all non-None pollutants."""
        result = compute_station_aqi({"pm2_5": 45.0, "pm10": 80.0, "no2": None})
        assert "pm2_5" in result["sub_indices"]
        assert "pm10" in result["sub_indices"]
        assert "no2" not in result["sub_indices"]


# =====================================================================
# get_aqi_category tests
# =====================================================================
class TestGetAqiCategory:
    """Tests for AQI category classification."""

    def test_good(self):
        label, color = get_aqi_category(25)
        assert label == "Good"
        assert color == "green"

    def test_satisfactory(self):
        label, color = get_aqi_category(75)
        assert label == "Satisfactory"
        assert color == "yellow"

    def test_moderate(self):
        label, color = get_aqi_category(150)
        assert label == "Moderate"
        assert color == "orange"

    def test_poor(self):
        label, color = get_aqi_category(250)
        assert label == "Poor"
        assert color == "red"

    def test_very_poor(self):
        label, color = get_aqi_category(350)
        assert label == "Very Poor"
        assert color == "purple"

    def test_severe(self):
        label, color = get_aqi_category(450)
        assert label == "Severe"
        assert color == "maroon"

    def test_none(self):
        label, color = get_aqi_category(None)
        assert label == "Unknown"
        assert color == "gray"

    def test_boundary_50(self):
        label, _ = get_aqi_category(50)
        assert label == "Good"

    def test_boundary_51(self):
        label, _ = get_aqi_category(51)
        assert label == "Satisfactory"

    def test_boundary_100(self):
        label, _ = get_aqi_category(100)
        assert label == "Satisfactory"

    def test_boundary_101(self):
        label, _ = get_aqi_category(101)
        assert label == "Moderate"

    def test_above_500(self):
        label, color = get_aqi_category(600)
        assert label == "Severe"
        assert color == "maroon"


# =====================================================================
# aqi_to_color tests
# =====================================================================
class TestAqiToColor:
    """Tests for AQI to hex color mapping."""

    def test_good_color(self):
        assert aqi_to_color(25) == "#2ECC71"

    def test_satisfactory_color(self):
        assert aqi_to_color(75) == "#F1C40F"

    def test_moderate_color(self):
        assert aqi_to_color(150) == "#E67E22"

    def test_poor_color(self):
        assert aqi_to_color(250) == "#E74C3C"

    def test_very_poor_color(self):
        assert aqi_to_color(350) == "#8E44AD"

    def test_severe_color(self):
        assert aqi_to_color(450) == "#C0392B"

    def test_none_color(self):
        assert aqi_to_color(None) == "#808080"


# =====================================================================
# Breakpoint integrity tests
# =====================================================================
class TestBreakpointIntegrity:
    """Verify that breakpoints are well-formed."""

    def test_all_pollutants_present(self):
        expected = {"pm2_5", "pm10", "no2", "so2", "co", "o3_8h", "o3_1h"}
        assert expected.issubset(set(BREAKPOINTS.keys()))

    def test_each_has_six_breakpoints(self):
        # FIX: o3_8h and o3_1h are deliberately NOT full 0-500 tables -- CPCB
        # only defines 8-hr O3 breakpoints through "Poor" (4 bands) and 1-hr
        # O3 breakpoints only for Very Poor/Severe (2 bands). Splitting them
        # this way is the actual fix for the O3 averaging-period bug.
        for pollutant, bps in BREAKPOINTS.items():
            if pollutant in ("o3_8h", "o3_1h"):
                continue
            assert len(bps) == 6, f"{pollutant} should have 6 breakpoints"
        assert len(BREAKPOINTS["o3_8h"]) == 4
        assert len(BREAKPOINTS["o3_1h"]) == 2

    def test_aqi_ranges_are_0_to_500(self):
        for pollutant, bps in BREAKPOINTS.items():
            if pollutant in ("o3_8h", "o3_1h"):
                continue
            assert bps[0][2] == 0, f"{pollutant} first I_low should be 0"
            assert bps[-1][3] == 500, f"{pollutant} last I_high should be 500"
        # o3_8h intentionally stops at "Poor" (300); o3_1h intentionally
        # starts at "Very Poor" (301) -- see comment above.
        assert BREAKPOINTS["o3_8h"][0][2] == 0
        assert BREAKPOINTS["o3_8h"][-1][3] == 300
        assert BREAKPOINTS["o3_1h"][0][2] == 301
        assert BREAKPOINTS["o3_1h"][-1][3] == 500

    def test_breakpoints_no_overlap(self):
        """Each breakpoint's C_high should be < next breakpoint's C_low (no overlap)."""
        for pollutant, bps in BREAKPOINTS.items():
            for i in range(len(bps) - 1):
                assert bps[i][1] < bps[i + 1][0], (
                    f"{pollutant} breakpoints overlap at index {i}: "
                    f"high={bps[i][1]} >= next_low={bps[i + 1][0]}"
                )
