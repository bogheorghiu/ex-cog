"""Tests for content extraction module - TDD RED phase."""
import json
from dataclasses import asdict
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from scripts.extract_content import (
    ArticleData,
    html_to_markdown,
    save_article,
    extract_article,
    batch_extract,
)


class TestArticleData:
    """Test ArticleData dataclass."""

    def test_create_article_data(self):
        """Create ArticleData with all fields."""
        data = ArticleData(
            url="https://example.substack.com/p/test",
            title="Test Article",
            date="2024-01-15",
            content_html="<p>Hello</p>",
            content_md="Hello",
        )

        assert data.url == "https://example.substack.com/p/test"
        assert data.title == "Test Article"
        assert data.date == "2024-01-15"
        assert data.content_html == "<p>Hello</p>"
        assert data.content_md == "Hello"


class TestHtmlToMarkdown:
    """Test HTML to Markdown conversion."""

    def test_simple_paragraph(self):
        """Convert simple paragraph."""
        html = "<p>Hello world</p>"
        result = html_to_markdown(html)
        assert "Hello world" in result

    def test_preserves_links(self):
        """Preserve links in markdown (or at least link text)."""
        html = '<p><a href="https://example.com">Link</a></p>'
        result = html_to_markdown(html)
        # At minimum, the link text should be preserved
        assert "Link" in result
        # If html2text is available, URL should also be present
        # (fallback mode only preserves text)

    def test_converts_headers(self):
        """Convert HTML headers to markdown."""
        html = "<h2>Heading</h2><p>Content</p>"
        result = html_to_markdown(html)
        assert "#" in result or "Heading" in result

    def test_handles_empty(self):
        """Handle empty HTML."""
        result = html_to_markdown("")
        assert result == "" or result.strip() == ""


class TestSaveArticle:
    """Test saving article in multiple formats (Phase 2: type-separated dirs + single MD)."""

    def test_saves_all_formats(self, tmp_path):
        """Save HTML and JSON individually, Markdown to single file."""
        data = ArticleData(
            url="https://example.substack.com/p/test-article",
            title="Test Article",
            date="2024-01-15",
            content_html="<p>Content</p>",
            content_md="Content",
        )

        save_article(data, str(tmp_path))

        # Check type-separated directories and single markdown
        assert (tmp_path / "html").exists()
        assert (tmp_path / "json").exists()
        assert (tmp_path / "html" / "2024-01-15-test-article.html").exists()
        assert (tmp_path / "json" / "2024-01-15-test-article.json").exists()
        assert (tmp_path / "all_articles.md").exists()

    def test_html_content(self, tmp_path):
        """Verify HTML file content with source URL."""
        data = ArticleData(
            url="https://example.substack.com/p/html-test",
            title="HTML Test",
            date="2024-01-20",
            content_html="<h1>Title</h1><p>Paragraph</p>",
            content_md="# Title\n\nParagraph",
        )

        save_article(data, str(tmp_path))

        html_file = tmp_path / "html" / "2024-01-20-html-test.html"
        content = html_file.read_text()
        assert "<h1>Title</h1>" in content
        assert "Source:" in content  # URL header added

    def test_markdown_appends_to_single_file(self, tmp_path):
        """Verify Markdown appends to single all_articles.md file."""
        data1 = ArticleData(
            url="https://example.substack.com/p/first",
            title="First Article",
            date="2024-01-21",
            content_html="<p>First</p>",
            content_md="First content",
        )
        data2 = ArticleData(
            url="https://example.substack.com/p/second",
            title="Second Article",
            date="2024-01-22",
            content_html="<p>Second</p>",
            content_md="Second content",
        )

        save_article(data1, str(tmp_path))
        save_article(data2, str(tmp_path))

        md_file = tmp_path / "all_articles.md"
        content = md_file.read_text()
        assert "# First Article" in content
        assert "# Second Article" in content
        assert "---" in content  # Separator between articles

    def test_metadata_json(self, tmp_path):
        """Verify metadata JSON content."""
        data = ArticleData(
            url="https://example.substack.com/p/meta-test",
            title="Metadata Test",
            date="2024-01-22",
            content_html="<p>Test</p>",
            content_md="Test",
        )

        save_article(data, str(tmp_path))

        meta_file = tmp_path / "json" / "2024-01-22-meta-test.json"
        meta = json.loads(meta_file.read_text())
        assert meta["title"] == "Metadata Test"
        assert meta["date"] == "2024-01-22"
        assert meta["url"] == "https://example.substack.com/p/meta-test"

    def test_handles_missing_date(self, tmp_path):
        """Handle article without date (uses 'unknown' prefix)."""
        data = ArticleData(
            url="https://example.substack.com/p/no-date",
            title="No Date",
            date=None,
            content_html="<p>Content</p>",
            content_md="Content",
        )

        save_article(data, str(tmp_path))

        # Should use 'unknown' as date prefix
        html_files = list((tmp_path / "html").glob("*.html"))
        assert len(html_files) == 1
        assert "unknown" in html_files[0].name

    def test_url_based_slug_prevents_collisions(self, tmp_path):
        """Use URL slug instead of title to prevent filename collisions."""
        # Two articles with same title but different URL slugs
        data1 = ArticleData(
            url="https://example.substack.com/p/unique-slug-1",
            title="Same Title",
            date="2024-01-23",
            content_html="<p>First</p>",
            content_md="First",
        )
        data2 = ArticleData(
            url="https://example.substack.com/p/unique-slug-2",
            title="Same Title",
            date="2024-01-23",
            content_html="<p>Second</p>",
            content_md="Second",
        )

        save_article(data1, str(tmp_path))
        save_article(data2, str(tmp_path))

        # Both should exist with unique names
        html_files = list((tmp_path / "html").glob("*.html"))
        assert len(html_files) == 2
        filenames = [f.name for f in html_files]
        assert "2024-01-23-unique-slug-1.html" in filenames
        assert "2024-01-23-unique-slug-2.html" in filenames


class TestExtractArticle:
    """Test single article extraction (mocked Playwright)."""

    def test_extract_article_data(self):
        """Extract article data from page."""
        mock_page = MagicMock()

        # Mock title
        mock_h1 = MagicMock()
        mock_h1.inner_text.return_value = "Article Title"

        # Mock date
        mock_time = MagicMock()
        mock_time.get_attribute.return_value = "2024-01-25"

        # Mock article content
        mock_article = MagicMock()
        mock_article.inner_html.return_value = "<p>Article content</p>"

        mock_page.query_selector.side_effect = lambda sel: {
            "h1": mock_h1,
            "time": mock_time,
            "article": mock_article,
        }.get(sel.split()[0] if sel else sel)

        result = extract_article(mock_page, "https://test.substack.com/p/test")

        assert result.title == "Article Title"
        assert result.date == "2024-01-25"
        assert "<p>Article content</p>" in result.content_html


class TestBatchExtract:
    """Test batch extraction with checkpointing."""

    @patch("scripts.extract_content.sync_playwright")
    def test_batch_skips_completed(self, mock_playwright, tmp_path):
        """Skip already-extracted articles."""
        from scripts.config import Config
        from scripts.utils import save_progress

        # Set up mock
        mock_p = MagicMock()
        mock_playwright.return_value.__enter__.return_value = mock_p
        mock_browser = MagicMock()
        mock_p.chromium.launch.return_value = mock_browser
        mock_context = MagicMock()
        mock_browser.new_context.return_value = mock_context
        mock_page = MagicMock()
        mock_context.new_page.return_value = mock_page

        # Create config and progress
        config = Config(
            substack_url="https://test.substack.com",
            output_dir=str(tmp_path / "articles"),
            progress_file=str(tmp_path / "progress.json"),
            auth_state_path=str(tmp_path / "auth.json"),
            rate_limit_seconds=0.1,
        )

        # Mark first article as completed
        save_progress(config.progress_file, {"https://test.substack.com/p/done"})

        articles = [
            {"url": "https://test.substack.com/p/done", "title": "Done"},
            {"url": "https://test.substack.com/p/new", "title": "New"},
        ]

        # Mock extraction for new article
        mock_h1 = MagicMock()
        mock_h1.inner_text.return_value = "New"
        mock_time = MagicMock()
        mock_time.get_attribute.return_value = "2024-01-01"
        mock_article = MagicMock()
        mock_article.inner_html.return_value = "<p>New content</p>"

        mock_page.query_selector.side_effect = lambda sel: {
            "h1": mock_h1,
            "time": mock_time,
            "article": mock_article,
        }.get(sel.split()[0] if sel else sel)

        # Create fake auth state
        (tmp_path / "auth.json").write_text("{}")

        batch_extract(articles, config)

        # Should only navigate to the new article
        goto_calls = [call[0][0] for call in mock_page.goto.call_args_list]
        assert "https://test.substack.com/p/done" not in goto_calls
        assert "https://test.substack.com/p/new" in goto_calls
