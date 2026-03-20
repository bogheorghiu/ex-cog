"""Tests for config module - TDD RED phase."""
import json
import tempfile
from pathlib import Path

import pytest

from scripts.config import Config, load_config


class TestConfig:
    """Test Config dataclass."""

    def test_default_values(self):
        """Config has sensible defaults."""
        config = Config(substack_url="https://example.substack.com")

        assert config.substack_url == "https://example.substack.com"
        assert config.rate_limit_seconds == 2.5
        assert config.output_dir == "data/articles"
        assert config.auth_state_path == "auth/browser_state.json"
        assert config.progress_file == "progress.json"
        assert config.max_articles is None  # None means all

    def test_custom_values(self):
        """Config accepts custom values."""
        config = Config(
            substack_url="https://test.substack.com",
            rate_limit_seconds=5.0,
            output_dir="custom/output",
            max_articles=50,
        )

        assert config.rate_limit_seconds == 5.0
        assert config.output_dir == "custom/output"
        assert config.max_articles == 50


class TestLoadConfig:
    """Test load_config function."""

    def test_load_from_json(self, tmp_path):
        """Load config from JSON file."""
        config_file = tmp_path / "config.json"
        config_file.write_text(
            json.dumps(
                {
                    "substack_url": "https://loaded.substack.com",
                    "rate_limit_seconds": 3.0,
                }
            )
        )

        config = load_config(str(config_file))

        assert config.substack_url == "https://loaded.substack.com"
        assert config.rate_limit_seconds == 3.0

    def test_defaults_when_missing_fields(self, tmp_path):
        """Use defaults for missing fields."""
        config_file = tmp_path / "config.json"
        config_file.write_text(
            json.dumps({"substack_url": "https://minimal.substack.com"})
        )

        config = load_config(str(config_file))

        assert config.substack_url == "https://minimal.substack.com"
        assert config.rate_limit_seconds == 2.5  # Default
        assert config.output_dir == "data/articles"  # Default

    def test_file_not_found_error(self, tmp_path):
        """Raise error if config file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            load_config(str(tmp_path / "nonexistent.json"))

    def test_invalid_json_error(self, tmp_path):
        """Raise error on invalid JSON."""
        config_file = tmp_path / "config.json"
        config_file.write_text("not valid json")

        with pytest.raises(json.JSONDecodeError):
            load_config(str(config_file))

    def test_missing_required_field(self, tmp_path):
        """Raise error if required field missing."""
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps({"rate_limit_seconds": 3.0}))

        with pytest.raises((KeyError, TypeError)):
            load_config(str(config_file))

    def test_all_fields(self, tmp_path):
        """Load config with all fields specified."""
        config_file = tmp_path / "config.json"
        config_file.write_text(
            json.dumps(
                {
                    "substack_url": "https://full.substack.com",
                    "rate_limit_seconds": 4.0,
                    "output_dir": "custom/articles",
                    "auth_state_path": "custom/auth.json",
                    "progress_file": "custom/progress.json",
                    "max_articles": 100,
                }
            )
        )

        config = load_config(str(config_file))

        assert config.substack_url == "https://full.substack.com"
        assert config.rate_limit_seconds == 4.0
        assert config.output_dir == "custom/articles"
        assert config.auth_state_path == "custom/auth.json"
        assert config.progress_file == "custom/progress.json"
        assert config.max_articles == 100
