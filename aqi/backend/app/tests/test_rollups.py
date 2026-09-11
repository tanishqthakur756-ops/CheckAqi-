"""
Unit tests for the rollups module (Part 3).

Tests the `summarize` function with mock DailyReading objects —
no database required.
"""

import pytest
from types import SimpleNamespace
from app.analytics.rollups import summarize


def make_reading(aqi=None, temperature=None, rainfall_mm=None, data_type="observed"):
    """Create a mock DailyReading-like object."""
    return SimpleNamespace(
        aqi=aqi,
        temperature=temperature,
        rainfall_mm=rainfall_mm,
        data_type=data_type,
        date="2024-06-15",
    )


class TestSummarize:
    """Tests for the summarize function (Contract B producer)."""

    def test_empty_readings(self):
        """No readings should produce a no_data rollup."""
        result = summarize([])
        assert result["avg_aqi"] is None
        assert result["max_aqi"] is None
        assert result["avg_temp"] is None
        assert result["avg_rainfall"] is None
        assert result["station_count"] == 0
        assert result["coverage_type"] == "no_data"

    def test_single_reading(self):
        """A single reading should produce correct averages."""
        readings = [make_reading(aqi=120.0, temperature=28.5, rainfall_mm=0.0)]
        result = summarize(readings)
        assert result["avg_aqi"] == 120.0
        assert result["max_aqi"] == 120.0
        assert result["avg_temp"] == 28.5
        assert result["avg_rainfall"] == 0.0
        assert result["station_count"] == 1
        assert result["coverage_type"] == "station"

    def test_multiple_readings(self):
        """Multiple readings should average correctly."""
        readings = [
            make_reading(aqi=100.0, temperature=25.0, rainfall_mm=5.0),
            make_reading(aqi=150.0, temperature=30.0, rainfall_mm=10.0),
            make_reading(aqi=200.0, temperature=35.0, rainfall_mm=0.0),
        ]
        result = summarize(readings)
        assert result["avg_aqi"] == 150.0
        assert result["max_aqi"] == 200.0
        assert result["avg_temp"] == 30.0
        assert result["avg_rainfall"] == 5.0
        assert result["station_count"] == 3
        assert result["coverage_type"] == "station"

    def test_none_values_filtered(self):
        """None values should be excluded from averages."""
        readings = [
            make_reading(aqi=100.0, temperature=None, rainfall_mm=5.0),
            make_reading(aqi=None, temperature=30.0, rainfall_mm=10.0),
        ]
        result = summarize(readings)
        assert result["avg_aqi"] == 100.0  # only one non-None
        assert result["max_aqi"] == 100.0
        assert result["avg_temp"] == 30.0  # only one non-None
        assert result["avg_rainfall"] == 7.5  # average of 5 and 10
        assert result["station_count"] == 2

    def test_all_none_aqi(self):
        """All None AQI values should produce None avg/max."""
        readings = [
            make_reading(aqi=None, temperature=25.0),
            make_reading(aqi=None, temperature=30.0),
        ]
        result = summarize(readings)
        assert result["avg_aqi"] is None
        assert result["max_aqi"] is None
        assert result["avg_temp"] == 27.5
        assert result["station_count"] == 2

    def test_interpolated_coverage(self):
        """All estimated readings should produce 'interpolated' coverage."""
        readings = [
            make_reading(aqi=100.0, data_type="estimated"),
            make_reading(aqi=150.0, data_type="estimated"),
        ]
        result = summarize(readings)
        assert result["coverage_type"] == "interpolated"

    def test_mixed_coverage(self):
        """Mix of observed and estimated should be 'station'."""
        readings = [
            make_reading(aqi=100.0, data_type="observed"),
            make_reading(aqi=150.0, data_type="estimated"),
        ]
        result = summarize(readings)
        assert result["coverage_type"] == "station"

    def test_season_is_set(self):
        """The season field should always be populated."""
        readings = [make_reading(aqi=100.0)]
        result = summarize(readings)
        assert result["season"] in ("winter", "summer", "monsoon", "post_monsoon")

    def test_contract_b_shape(self):
        """Result should have all Contract B fields."""
        readings = [make_reading(aqi=100.0, temperature=25.0, rainfall_mm=5.0)]
        result = summarize(readings)
        expected_keys = {
            "avg_aqi", "max_aqi", "avg_temp", "avg_rainfall",
            "season", "station_count", "coverage_type",
        }
        assert set(result.keys()) == expected_keys
