"""Integration tests for the full pipeline."""
import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from main import check_auth_state, main, run_discovery, run_extraction
from scripts.config import Config


class TestCheckAuthState:
    """Test auth state checking."""

    def test_returns_true_when_exists(self, tmp_path):
        """Return True when auth state file exists."""
        auth_file = tmp_path / "auth.json"
        auth_file.write_text("{}")

        config = Config(
            substack_url="https://test.substack.com",
            auth_state_path=str(auth_file),
        )

        assert check_auth_state(config) is True

    def test_returns_false_when_missing(self, tmp_path):
        """Return False when auth state file missing."""
        config = Config(
            substack_url="https://test.substack.com",
            auth_state_path=str(tmp_path / "nonexistent.json"),
        )

        assert check_auth_state(config) is False


class TestRunDiscovery:
    """Test discovery phase."""

    @patch("main.discover_articles")
    @patch("main.save_article_index")
    def test_discovers_and_saves_index(
        self, mock_save, mock_discover, tmp_path
    ):
        """Discover articles and save index."""
        mock_discover.return_value = [
            {"url": "https://test.substack.com/p/article-1", "title": "Article 1"},
            {"url": "https://test.substack.com/p/article-2", "title": "Article 2"},
        ]

        config = Config(
            substack_url="https://test.substack.com",
            output_dir=str(tmp_path / "articles"),
            auth_state_path=str(tmp_path / "auth.json"),
        )

        articles = run_discovery(config)

        assert len(articles) == 2
        mock_discover.assert_called_once_with(
            "https://test.substack.com",
            str(tmp_path / "auth.json"),
        )
        mock_save.assert_called_once()


class TestRunExtraction:
    """Test extraction phase."""

    @patch("main.batch_extract")
    def test_extracts_all_articles(self, mock_batch, tmp_path):
        """Extract all articles when no limit."""
        articles = [
            {"url": "https://test.substack.com/p/article-1", "title": "Article 1"},
            {"url": "https://test.substack.com/p/article-2", "title": "Article 2"},
        ]

        config = Config(
            substack_url="https://test.substack.com",
            output_dir=str(tmp_path / "articles"),
        )

        run_extraction(articles, config)

        mock_batch.assert_called_once_with(articles, config)

    @patch("main.batch_extract")
    def test_respects_max_articles_limit(self, mock_batch, tmp_path):
        """Limit extraction when max_articles set."""
        articles = [
            {"url": "https://test.substack.com/p/article-1", "title": "Article 1"},
            {"url": "https://test.substack.com/p/article-2", "title": "Article 2"},
            {"url": "https://test.substack.com/p/article-3", "title": "Article 3"},
        ]

        config = Config(
            substack_url="https://test.substack.com",
            output_dir=str(tmp_path / "articles"),
            max_articles=2,
        )

        run_extraction(articles, config)

        # Should only extract first 2
        call_args = mock_batch.call_args[0]
        assert len(call_args[0]) == 2


class TestMain:
    """Test main entry point."""

    def test_fails_without_config(self, tmp_path, monkeypatch):
        """Return 1 when config file missing."""
        monkeypatch.chdir(tmp_path)

        result = main("nonexistent.json")

        assert result == 1

    def test_fails_without_auth_state(self, tmp_path, monkeypatch):
        """Return 1 when auth state missing."""
        monkeypatch.chdir(tmp_path)

        # Create config but no auth file
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps({
            "substack_url": "https://test.substack.com",
            "auth_state_path": str(tmp_path / "auth.json"),
        }))

        result = main(str(config_file))

        assert result == 1

    @patch("main.run_discovery")
    def test_returns_0_when_no_articles(self, mock_discovery, tmp_path, monkeypatch):
        """Return 0 (success) when no articles found."""
        monkeypatch.chdir(tmp_path)

        # Create config and auth file
        config_file = tmp_path / "config.json"
        auth_file = tmp_path / "auth.json"
        auth_file.write_text("{}")
        config_file.write_text(json.dumps({
            "substack_url": "https://test.substack.com",
            "auth_state_path": str(auth_file),
        }))

        mock_discovery.return_value = []

        result = main(str(config_file))

        assert result == 0

    @patch("main.run_extraction")
    @patch("main.run_discovery")
    def test_full_pipeline_success(
        self, mock_discovery, mock_extraction, tmp_path, monkeypatch
    ):
        """Return 0 on successful full pipeline."""
        monkeypatch.chdir(tmp_path)

        # Create config and auth file
        config_file = tmp_path / "config.json"
        auth_file = tmp_path / "auth.json"
        auth_file.write_text("{}")
        config_file.write_text(json.dumps({
            "substack_url": "https://test.substack.com",
            "auth_state_path": str(auth_file),
            "output_dir": str(tmp_path / "articles"),
        }))

        mock_discovery.return_value = [
            {"url": "https://test.substack.com/p/article-1", "title": "Test"},
        ]

        result = main(str(config_file))

        assert result == 0
        mock_discovery.assert_called_once()
        mock_extraction.assert_called_once()
