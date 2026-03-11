"""
Tests for TickerValidator - format validation and error handling.

Tests validate_format() and _handle_yfinance_errors() which are pure functions.
validate_with_yfinance() requires mocking external API.
"""

import pytest
import sys
import os

# Add parent directory to path for imports
parent_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, parent_dir)
sys.path.insert(0, os.path.join(parent_dir, 'implementations', 'validation'))

# Import directly to avoid ticker_cache's cache.manager dependency
from ticker_validator import TickerValidator


class TestValidateFormat:
    """Tests for TickerValidator.validate_format() - pure function, no mocking needed."""

    def test_empty_symbol_returns_false(self):
        """Empty string should fail validation."""
        is_valid, cleaned, error = TickerValidator.validate_format("")
        assert is_valid is False
        assert cleaned is None
        assert "empty" in error.lower()

    def test_none_symbol_returns_false(self):
        """None should fail validation."""
        is_valid, cleaned, error = TickerValidator.validate_format(None)
        assert is_valid is False
        assert cleaned is None
        assert "empty" in error.lower()

    def test_valid_simple_symbol(self):
        """Standard stock symbols should pass."""
        is_valid, cleaned, error = TickerValidator.validate_format("AAPL")
        assert is_valid is True
        assert cleaned == "AAPL"
        assert error is None

    def test_valid_symbol_with_dot(self):
        """Symbols with dots (BRK.A, BRK.B) should pass."""
        is_valid, cleaned, error = TickerValidator.validate_format("BRK.A")
        assert is_valid is True
        assert cleaned == "BRK.A"
        assert error is None

    def test_valid_symbol_with_hyphen(self):
        """Symbols with hyphens should pass."""
        is_valid, cleaned, error = TickerValidator.validate_format("BF-B")
        assert is_valid is True
        assert cleaned == "BF-B"
        assert error is None

    def test_lowercase_gets_uppercased(self):
        """Lowercase input should be normalized to uppercase."""
        is_valid, cleaned, error = TickerValidator.validate_format("aapl")
        assert is_valid is True
        assert cleaned == "AAPL"
        assert error is None

    def test_whitespace_gets_trimmed(self):
        """Leading/trailing whitespace should be removed."""
        is_valid, cleaned, error = TickerValidator.validate_format("  MSFT  ")
        assert is_valid is True
        assert cleaned == "MSFT"
        assert error is None

    def test_symbol_too_long_fails(self):
        """Symbols over 10 characters should fail (caught by regex length limit)."""
        is_valid, cleaned, error = TickerValidator.validate_format("VERYLONGSYMBOL")
        assert is_valid is False
        assert cleaned is None
        assert "invalid" in error.lower()  # Regex {1,10} catches length before explicit check

    def test_symbol_exactly_10_chars_passes(self):
        """10 character symbols should pass (edge case)."""
        is_valid, cleaned, error = TickerValidator.validate_format("ABCDEFGHIJ")
        assert is_valid is True
        assert cleaned == "ABCDEFGHIJ"
        assert error is None

    def test_special_characters_fail(self):
        """Symbols with special characters (except . and -) should fail."""
        invalid_symbols = ["AAPL!", "MS$FT", "GOOG@", "META#", "AMZN%"]
        for symbol in invalid_symbols:
            is_valid, cleaned, error = TickerValidator.validate_format(symbol)
            assert is_valid is False, f"Expected {symbol} to fail"
            assert "invalid" in error.lower()

    def test_numbers_allowed(self):
        """Symbols with numbers should pass."""
        is_valid, cleaned, error = TickerValidator.validate_format("3M")
        assert is_valid is True
        assert cleaned == "3M"


class TestHandleYfinanceErrors:
    """Tests for TickerValidator._handle_yfinance_errors() - error message mapping."""

    def test_no_data_found_error(self):
        """'No data found' errors should give specific message."""
        error = Exception("No data found for symbol XYZ")
        result = TickerValidator._handle_yfinance_errors("XYZ", error)
        assert "delisted" in result.lower() or "invalid" in result.lower()
        assert "XYZ" in result

    def test_delisted_error(self):
        """Delisted errors should be handled."""
        error = Exception("Symbol OLDCO is delisted")
        result = TickerValidator._handle_yfinance_errors("OLDCO", error)
        assert "delisted" in result.lower()

    def test_connection_error(self):
        """Connection errors should suggest retry."""
        error = Exception("Connection timeout")
        result = TickerValidator._handle_yfinance_errors("AAPL", error)
        assert "network" in result.lower() or "try again" in result.lower()

    def test_timeout_error(self):
        """Timeout errors should be handled like connection errors."""
        error = Exception("Request timeout after 30s")
        result = TickerValidator._handle_yfinance_errors("MSFT", error)
        assert "network" in result.lower() or "try again" in result.lower()

    def test_rate_limit_error(self):
        """Rate limit errors should give specific message."""
        error = Exception("Rate limit exceeded")
        result = TickerValidator._handle_yfinance_errors("GOOG", error)
        assert "rate limit" in result.lower()

    def test_too_many_requests_error(self):
        """'Too many requests' should be treated as rate limit."""
        error = Exception("Too many requests, please slow down")
        result = TickerValidator._handle_yfinance_errors("META", error)
        assert "rate limit" in result.lower()

    def test_unknown_error_includes_original(self):
        """Unknown errors should include the original error text."""
        error = Exception("Something completely unexpected happened")
        result = TickerValidator._handle_yfinance_errors("AMZN", error)
        assert "AMZN" in result
        assert "unexpected" in result.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
