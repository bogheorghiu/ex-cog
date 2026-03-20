"""Tests for utils module - TDD RED phase."""
import json
import os
import tempfile
from pathlib import Path

import pytest

from scripts.utils import slugify, load_progress, save_progress, ensure_dir


class TestSlugify:
    """Test slugify function."""

    def test_basic_text(self):
        """Convert simple text to slug."""
        assert slugify("Hello World") == "hello-world"

    def test_special_characters(self):
        """Remove special characters."""
        assert slugify("What's New? (2024)") == "whats-new-2024"

    def test_multiple_spaces(self):
        """Collapse multiple spaces/dashes."""
        assert slugify("Too   Many   Spaces") == "too-many-spaces"

    def test_unicode(self):
        """Handle unicode characters."""
        assert slugify("Café & Résumé") == "cafe-resume"

    def test_leading_trailing_dashes(self):
        """Strip leading/trailing dashes."""
        assert slugify("  --Hello--  ") == "hello"

    def test_empty_string(self):
        """Handle empty input."""
        assert slugify("") == ""

    def test_numbers_preserved(self):
        """Keep numbers in slug."""
        assert slugify("Article 123") == "article-123"


class TestLoadProgress:
    """Test load_progress function."""

    def test_load_existing_file(self, tmp_path):
        """Load progress from existing JSON file."""
        progress_file = tmp_path / "progress.json"
        progress_file.write_text(json.dumps(["url1", "url2", "url3"]))

        result = load_progress(str(progress_file))

        assert result == {"url1", "url2", "url3"}

    def test_load_nonexistent_file(self, tmp_path):
        """Return empty set if file doesn't exist."""
        progress_file = tmp_path / "nonexistent.json"

        result = load_progress(str(progress_file))

        assert result == set()

    def test_load_empty_file(self, tmp_path):
        """Handle empty JSON array."""
        progress_file = tmp_path / "progress.json"
        progress_file.write_text("[]")

        result = load_progress(str(progress_file))

        assert result == set()

    def test_load_invalid_json(self, tmp_path):
        """Return empty set on invalid JSON."""
        progress_file = tmp_path / "progress.json"
        progress_file.write_text("not valid json")

        result = load_progress(str(progress_file))

        assert result == set()


class TestSaveProgress:
    """Test save_progress function."""

    def test_save_progress(self, tmp_path):
        """Save progress to JSON file."""
        progress_file = tmp_path / "progress.json"
        completed = {"url1", "url2"}

        save_progress(str(progress_file), completed)

        saved_data = json.loads(progress_file.read_text())
        assert set(saved_data) == completed

    def test_save_creates_file(self, tmp_path):
        """Create file if it doesn't exist."""
        progress_file = tmp_path / "new_progress.json"
        completed = {"url1"}

        save_progress(str(progress_file), completed)

        assert progress_file.exists()

    def test_save_overwrites(self, tmp_path):
        """Overwrite existing progress."""
        progress_file = tmp_path / "progress.json"
        progress_file.write_text(json.dumps(["old_url"]))

        save_progress(str(progress_file), {"new_url"})

        saved_data = json.loads(progress_file.read_text())
        assert set(saved_data) == {"new_url"}

    def test_save_empty_set(self, tmp_path):
        """Handle empty set."""
        progress_file = tmp_path / "progress.json"

        save_progress(str(progress_file), set())

        saved_data = json.loads(progress_file.read_text())
        assert saved_data == []


class TestEnsureDir:
    """Test ensure_dir function."""

    def test_create_new_directory(self, tmp_path):
        """Create directory if it doesn't exist."""
        new_dir = tmp_path / "new_directory"

        ensure_dir(str(new_dir))

        assert new_dir.exists()
        assert new_dir.is_dir()

    def test_existing_directory(self, tmp_path):
        """No error if directory exists."""
        existing = tmp_path / "existing"
        existing.mkdir()

        # Should not raise
        ensure_dir(str(existing))

        assert existing.exists()

    def test_nested_directories(self, tmp_path):
        """Create nested directories."""
        nested = tmp_path / "a" / "b" / "c"

        ensure_dir(str(nested))

        assert nested.exists()

    def test_returns_path(self, tmp_path):
        """Return the path that was ensured."""
        new_dir = tmp_path / "return_test"

        result = ensure_dir(str(new_dir))

        assert result == str(new_dir)
