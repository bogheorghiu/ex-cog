"""Tests for article discovery module - TDD RED phase."""
import json
from unittest.mock import MagicMock, patch

import pytest

from scripts.discover_articles import (
    extract_article_metadata,
    discover_articles,
    save_article_index,
)


class TestExtractArticleMetadata:
    """Test metadata extraction from DOM elements."""

    def test_extract_full_metadata(self):
        """Extract all metadata fields from element."""
        mock_element = MagicMock()
        mock_element.get_attribute.side_effect = lambda attr: {
            "href": "https://example.substack.com/p/my-article",
        }.get(attr)
        mock_element.inner_text.return_value = "My Article Title"

        # Mock sibling date element
        mock_parent = MagicMock()
        mock_date = MagicMock()
        mock_date.get_attribute.return_value = "2024-01-15"
        mock_parent.query_selector.return_value = mock_date
        mock_element.evaluate_handle.return_value = mock_parent

        result = extract_article_metadata(mock_element)

        assert result["url"] == "https://example.substack.com/p/my-article"
        assert result["title"] == "My Article Title"
        assert "date" in result

    def test_handle_missing_date(self):
        """Handle missing date gracefully."""
        mock_element = MagicMock()
        mock_element.get_attribute.return_value = "https://example.substack.com/p/no-date"
        mock_element.inner_text.return_value = "No Date Article"

        mock_parent = MagicMock()
        mock_parent.query_selector.return_value = None
        mock_element.evaluate_handle.return_value = mock_parent

        result = extract_article_metadata(mock_element)

        assert result["url"] == "https://example.substack.com/p/no-date"
        assert result["title"] == "No Date Article"
        assert result["date"] is None


class TestSaveArticleIndex:
    """Test saving article index to JSON."""

    def test_save_index(self, tmp_path):
        """Save article list to JSON file."""
        output_file = tmp_path / "index.json"
        articles = [
            {"url": "https://example.substack.com/p/article-1", "title": "Article 1", "date": "2024-01-01"},
            {"url": "https://example.substack.com/p/article-2", "title": "Article 2", "date": "2024-01-02"},
        ]

        save_article_index(articles, str(output_file))

        saved = json.loads(output_file.read_text())
        assert len(saved) == 2
        assert saved[0]["title"] == "Article 1"

    def test_creates_parent_directory(self, tmp_path):
        """Create parent directory if needed."""
        output_file = tmp_path / "subdir" / "index.json"
        articles = [{"url": "https://example.substack.com/p/test", "title": "Test"}]

        save_article_index(articles, str(output_file))

        assert output_file.exists()


class TestDiscoverArticles:
    """Test full discovery workflow (mocked Playwright)."""

    @patch("scripts.discover_articles.sync_playwright")
    def test_discover_returns_articles(self, mock_playwright):
        """Discover articles from archive page."""
        # Set up mock chain
        mock_p = MagicMock()
        mock_playwright.return_value.__enter__.return_value = mock_p

        mock_browser = MagicMock()
        mock_p.chromium.launch.return_value = mock_browser

        mock_context = MagicMock()
        mock_browser.new_context.return_value = mock_context

        mock_page = MagicMock()
        mock_context.new_page.return_value = mock_page

        # Mock article elements
        mock_element = MagicMock()
        mock_element.get_attribute.return_value = "https://test.substack.com/p/article-1"
        mock_element.inner_text.return_value = "Test Article"
        mock_parent = MagicMock()
        mock_parent.query_selector.return_value = None
        mock_element.evaluate_handle.return_value = mock_parent

        # Return same count on each call (simulates no new articles loading)
        # Called: once in scroll loop, once after loop for extraction
        mock_page.query_selector_all.return_value = [mock_element]

        result = discover_articles(
            "https://test.substack.com",
            "/fake/state.json",
        )

        assert len(result) == 1
        assert result[0]["url"] == "https://test.substack.com/p/article-1"
        mock_browser.close.assert_called_once()

    @patch("scripts.discover_articles.sync_playwright")
    def test_discover_handles_empty_archive(self, mock_playwright):
        """Handle archive with no articles."""
        mock_p = MagicMock()
        mock_playwright.return_value.__enter__.return_value = mock_p

        mock_browser = MagicMock()
        mock_p.chromium.launch.return_value = mock_browser

        mock_context = MagicMock()
        mock_browser.new_context.return_value = mock_context

        mock_page = MagicMock()
        mock_context.new_page.return_value = mock_page

        mock_page.query_selector_all.return_value = []

        result = discover_articles(
            "https://empty.substack.com",
            "/fake/state.json",
        )

        assert result == []
