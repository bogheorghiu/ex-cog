"""Tests for parse_content.py - adaptive detail levels and parsing."""
import pytest
from pathlib import Path
from scripts.parse_content import (
    get_adaptive_detail_level,
    ParseConfig,
    ParseResult,
    DetailLevel,
    parse_articles,
)


class TestAdaptiveDetailLevel:
    """Tests for get_adaptive_detail_level() function."""

    def test_bulk_corpus_forces_level_2_with_clustering(self):
        """100+ articles force level 2 with clustering."""
        level, clustering, reason = get_adaptive_detail_level(150, 7)
        assert level == 2
        assert clustering is True
        assert "auto-reduced" in reason.lower() or "bulk" in reason.lower()

    def test_bulk_corpus_at_boundary(self):
        """Exactly 101 articles triggers bulk mode."""
        level, clustering, reason = get_adaptive_detail_level(101, 10)
        assert level == 2
        assert clustering is True

    def test_large_corpus_caps_at_level_3(self):
        """50-100 articles cap at level 3 with clustering."""
        level, clustering, reason = get_adaptive_detail_level(75, 8)
        assert level == 3
        assert clustering is True

    def test_large_corpus_at_lower_boundary(self):
        """Exactly 51 articles triggers large corpus mode."""
        level, clustering, reason = get_adaptive_detail_level(51, 9)
        assert level == 3
        assert clustering is True

    def test_medium_corpus_caps_at_level_5(self):
        """20-50 articles cap at level 5, no clustering."""
        level, clustering, reason = get_adaptive_detail_level(30, 9)
        assert level == 5
        assert clustering is False

    def test_medium_corpus_at_lower_boundary(self):
        """Exactly 21 articles triggers medium corpus mode."""
        level, clustering, reason = get_adaptive_detail_level(21, 10)
        assert level == 5
        assert clustering is False

    def test_small_corpus_uses_requested_level(self):
        """<20 articles use requested level without clustering."""
        level, clustering, reason = get_adaptive_detail_level(10, 9)
        assert level == 9
        assert clustering is False
        assert reason == ""  # No adjustment message

    def test_small_corpus_at_boundary(self):
        """Exactly 20 articles still counts as small."""
        level, clustering, reason = get_adaptive_detail_level(20, 8)
        assert level == 8
        assert clustering is False

    def test_requested_level_below_cap_unchanged(self):
        """If requested level is already below cap, use it."""
        # Bulk corpus but requesting level 1 (below cap of 2)
        level, clustering, reason = get_adaptive_detail_level(150, 1)
        assert level == 1
        assert clustering is True

    def test_zero_articles(self):
        """Zero articles uses requested level."""
        level, clustering, reason = get_adaptive_detail_level(0, 5)
        assert level == 5
        assert clustering is False

    def test_single_article(self):
        """Single article uses requested level."""
        level, clustering, reason = get_adaptive_detail_level(1, 10)
        assert level == 10
        assert clustering is False


class TestParseConfig:
    """Tests for ParseConfig dataclass."""

    def test_valid_detail_level(self):
        """Valid detail levels 0-10 are accepted."""
        for level in range(11):
            config = ParseConfig(detail_level=level)
            assert config.detail_level == level

    def test_invalid_detail_level_raises(self):
        """Detail level outside 0-10 raises ValueError."""
        with pytest.raises(ValueError, match="must be 0-10"):
            ParseConfig(detail_level=11)
        with pytest.raises(ValueError, match="must be 0-10"):
            ParseConfig(detail_level=-1)

    def test_category_quick(self):
        """Levels 0-3 return 'quick' category."""
        for level in range(4):
            config = ParseConfig(detail_level=level)
            assert config.category == "quick"

    def test_category_balanced(self):
        """Levels 4-6 return 'balanced' category."""
        for level in range(4, 7):
            config = ParseConfig(detail_level=level)
            assert config.category == "balanced"

    def test_category_comprehensive(self):
        """Levels 7-10 return 'comprehensive' category."""
        for level in range(7, 11):
            config = ParseConfig(detail_level=level)
            assert config.category == "comprehensive"

    def test_clustering_default_false(self):
        """use_clustering defaults to False."""
        config = ParseConfig()
        assert config.use_clustering is False

    def test_adaptive_reason_default_empty(self):
        """adaptive_reason defaults to empty string."""
        config = ParseConfig()
        assert config.adaptive_reason == ""


class TestParseResult:
    """Tests for ParseResult dataclass."""

    def test_result_includes_clustering_fields(self):
        """ParseResult has use_clustering and adaptive_reason fields."""
        result = ParseResult(
            overview="test",
            articles=[],
            themes=[],
            connections=[],
            detail_level=5,
            use_clustering=True,
            adaptive_reason="Test reason",
        )
        assert result.use_clustering is True
        assert result.adaptive_reason == "Test reason"

    def test_result_defaults(self):
        """ParseResult has sensible defaults for new fields."""
        result = ParseResult(
            overview="test",
            articles=[],
            themes=[],
            connections=[],
            detail_level=5,
        )
        assert result.use_clustering is False
        assert result.adaptive_reason == ""


class TestParseArticlesIntegration:
    """Integration tests for parse_articles with adaptive detail."""

    def test_force_level_bypasses_adaptive(self, tmp_path):
        """force_level=True uses exact detail level without adaptation."""
        # Create minimal article structure
        json_dir = tmp_path / "json"
        json_dir.mkdir()

        # Create 150 fake article metadata files
        for i in range(150):
            (json_dir / f"article_{i}.json").write_text(
                f'{{"title": "Article {i}", "url": "http://example.com/{i}"}}'
            )

        # Without force_level, should adapt to level 2
        result_adapted = parse_articles(str(tmp_path), detail_level=7)
        assert result_adapted.detail_level == 2
        assert result_adapted.use_clustering is True

        # With force_level, should use exact level
        result_forced = parse_articles(str(tmp_path), detail_level=7, force_level=True)
        assert result_forced.detail_level == 7
        assert result_forced.use_clustering is False

    def test_empty_directory_returns_no_articles(self, tmp_path):
        """Empty directory returns appropriate result."""
        result = parse_articles(str(tmp_path), detail_level=5)
        assert "No articles found" in result.overview
        assert len(result.articles) == 0
