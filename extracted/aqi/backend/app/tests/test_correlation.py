"""
Unit tests for the correlation module (Part 3).

Tests the `pearson_r` function with known data — no database required.
"""

import pytest
import math
from app.analytics.correlation import pearson_r


class TestPearsonR:
    """Tests for the Pearson correlation coefficient calculation."""

    def test_perfect_positive(self):
        """Perfect positive correlation should return 1.0."""
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]
        result = pearson_r(x, y)
        assert result == 1.0

    def test_perfect_negative(self):
        """Perfect negative correlation should return -1.0."""
        x = [1, 2, 3, 4, 5]
        y = [10, 8, 6, 4, 2]
        result = pearson_r(x, y)
        assert result == -1.0

    def test_no_correlation(self):
        """Uncorrelated data should return a value near 0."""
        x = [1, 2, 3, 4, 5]
        y = [3, 1, 5, 2, 4]
        result = pearson_r(x, y)
        assert result is not None
        assert -0.5 < result < 0.5

    def test_single_pair(self):
        """Only 2 data points should return None (need at least 2 for variance)."""
        result = pearson_r([1], [2])
        assert result is None

    def test_mismatched_lengths(self):
        """Mismatched list lengths should return None."""
        result = pearson_r([1, 2, 3], [1, 2])
        assert result is None

    def test_zero_variance(self):
        """Zero variance in one variable should return None."""
        x = [5, 5, 5, 5, 5]
        y = [1, 2, 3, 4, 5]
        result = pearson_r(x, y)
        assert result is None

    def test_empty_lists(self):
        """Empty lists should return None."""
        result = pearson_r([], [])
        assert result is None

    def test_known_value(self):
        """Test with a known correlation value."""
        # x and y have a known correlation
        x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        y = [2, 1, 4, 3, 6, 5, 8, 7, 10, 9]
        result = pearson_r(x, y)
        assert result is not None
        # This should be a strong positive correlation
        assert result > 0.5

    def test_rounding(self):
        """Result should be rounded to 4 decimal places."""
        x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        y = [1, 3, 2, 5, 4, 7, 6, 9, 8, 10]
        result = pearson_r(x, y)
        assert result is not None
        # Check it's rounded (no more than 4 decimal places)
        assert result == round(result, 4)
