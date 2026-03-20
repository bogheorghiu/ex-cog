"""Tests for saturation_detector.py - Ralph-Plus saturation detection."""
import pytest
from scripts.saturation_detector import (
    SaturationTracker,
    PassQuality,
    PassResult,
    should_continue_simple,
    assess_pass_quality_simple,
)


class TestPassQuality:
    """Tests for PassQuality enum."""

    def test_quality_values(self):
        """PassQuality has HIGH and LOW values."""
        assert PassQuality.HIGH.value == "HIGH"
        assert PassQuality.LOW.value == "LOW"


class TestSaturationTracker:
    """Tests for SaturationTracker class."""

    def test_initial_state(self):
        """New tracker starts with empty state."""
        tracker = SaturationTracker()
        assert len(tracker.history) == 0
        assert tracker.is_saturated is False
        assert tracker.stop_reason == ""

    def test_assess_quality_high(self):
        """2+ patterns returns HIGH quality."""
        tracker = SaturationTracker()
        assert tracker.assess_quality(2, 0) == PassQuality.HIGH
        assert tracker.assess_quality(1, 1) == PassQuality.HIGH
        assert tracker.assess_quality(0, 2) == PassQuality.HIGH
        assert tracker.assess_quality(5, 3) == PassQuality.HIGH

    def test_assess_quality_low(self):
        """<2 patterns returns LOW quality."""
        tracker = SaturationTracker()
        assert tracker.assess_quality(0, 0) == PassQuality.LOW
        assert tracker.assess_quality(1, 0) == PassQuality.LOW
        assert tracker.assess_quality(0, 1) == PassQuality.LOW

    def test_record_pass_adds_to_history(self):
        """record_pass adds PassResult to history."""
        tracker = SaturationTracker()
        result = tracker.record_pass(5, 2, "First pass")

        assert len(tracker.history) == 1
        assert result.new_patterns == 5
        assert result.reinforced_patterns == 2
        assert result.quality == PassQuality.HIGH
        assert result.notes == "First pass"

    def test_should_continue_after_one_low(self):
        """Should continue after single LOW pass."""
        tracker = SaturationTracker()
        tracker.record_pass(0, 1)  # LOW

        assert tracker.should_continue() is True
        assert tracker.is_saturated is False

    def test_saturation_after_two_consecutive_low(self):
        """Saturation detected after 2 consecutive LOW passes."""
        tracker = SaturationTracker()
        tracker.record_pass(5, 2)  # HIGH
        tracker.record_pass(0, 1)  # LOW
        tracker.record_pass(0, 0)  # LOW

        assert tracker.should_continue() is False
        assert tracker.is_saturated is True
        assert "2" in tracker.stop_reason
        assert "consecutive" in tracker.stop_reason.lower()

    def test_high_pass_resets_consecutive_count(self):
        """HIGH pass between LOWs resets consecutive count."""
        tracker = SaturationTracker()
        tracker.record_pass(0, 1)  # LOW
        tracker.record_pass(3, 2)  # HIGH - resets
        tracker.record_pass(0, 0)  # LOW

        assert tracker.should_continue() is True
        assert tracker.is_saturated is False

    def test_preview_mode_checks_without_recording(self):
        """Preview counts affect should_continue without mutating history."""
        tracker = SaturationTracker()
        tracker.record_pass(0, 1)  # LOW

        # Preview another LOW - should trigger saturation check
        result = tracker.should_continue(preview_new=0, preview_reinforced=0)

        # History not mutated
        assert len(tracker.history) == 1
        # Preview detected potential saturation
        assert result is False
        # State not mutated by preview
        assert tracker.is_saturated is False

    def test_preview_high_continues(self):
        """Preview with HIGH quality allows continuation."""
        tracker = SaturationTracker()
        tracker.record_pass(0, 1)  # LOW

        # Preview a HIGH pass
        result = tracker.should_continue(preview_new=3, preview_reinforced=2)

        assert result is True

    def test_get_summary(self):
        """get_summary returns correct statistics."""
        tracker = SaturationTracker()
        tracker.record_pass(5, 2)  # HIGH
        tracker.record_pass(3, 1)  # HIGH
        tracker.record_pass(0, 1)  # LOW
        tracker.record_pass(0, 0)  # LOW

        summary = tracker.get_summary()

        assert summary["total_passes"] == 4
        assert summary["high_value_passes"] == 2
        assert summary["low_value_passes"] == 2
        assert summary["total_new_patterns"] == 8
        assert summary["total_reinforced"] == 4

    def test_custom_threshold(self):
        """Custom consecutive_low_threshold is respected."""
        tracker = SaturationTracker(consecutive_low_threshold=3)
        tracker.record_pass(0, 1)  # LOW
        tracker.record_pass(0, 0)  # LOW

        # 2 consecutive LOW, but threshold is 3
        assert tracker.should_continue() is True

        tracker.record_pass(0, 0)  # LOW - now 3 consecutive
        assert tracker.should_continue() is False

    def test_custom_high_pattern_threshold(self):
        """Custom high_pattern_threshold is respected."""
        tracker = SaturationTracker(high_pattern_threshold=3)

        # 2 patterns is now LOW with threshold=3
        assert tracker.assess_quality(1, 1) == PassQuality.LOW
        assert tracker.assess_quality(2, 1) == PassQuality.HIGH


class TestSimpleFunctions:
    """Tests for simple function variants."""

    def test_should_continue_simple_continues(self):
        """should_continue_simple returns True with <2 consecutive LOW."""
        result, reason = should_continue_simple(["HIGH", "LOW", "HIGH", "LOW"])
        assert result is True
        assert reason == ""

    def test_should_continue_simple_stops(self):
        """should_continue_simple returns False with 2+ consecutive LOW."""
        result, reason = should_continue_simple(["HIGH", "LOW", "LOW"])
        assert result is False
        assert "exhausted" in reason.lower() or "consecutive" in reason.lower()

    def test_should_continue_simple_case_insensitive(self):
        """should_continue_simple handles case variations."""
        result, _ = should_continue_simple(["high", "low", "low"])
        assert result is False

    def test_assess_pass_quality_simple_high(self):
        """assess_pass_quality_simple returns HIGH for 2+ patterns."""
        assert assess_pass_quality_simple(2, 0) == "HIGH"
        assert assess_pass_quality_simple(1, 1) == "HIGH"
        assert assess_pass_quality_simple(0, 2) == "HIGH"

    def test_assess_pass_quality_simple_low(self):
        """assess_pass_quality_simple returns LOW for <2 patterns."""
        assert assess_pass_quality_simple(0, 0) == "LOW"
        assert assess_pass_quality_simple(1, 0) == "LOW"
        assert assess_pass_quality_simple(0, 1) == "LOW"
