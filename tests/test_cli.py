"""
Tests for the CLI module.
"""

import sys
from unittest.mock import patch

import pytest

from image_to_pdf.cli import main


class TestCLI:
    """Tests for CLI entry point."""

    def test_version_flag(self, capsys):
        """Test --version flag."""
        with pytest.raises(SystemExit) as exc_info:
            with patch.object(sys, "argv", ["image-to-pdf", "--version"]):
                main()

        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "1.0.0" in captured.out

    def test_help_flag(self, capsys):
        """Test --help flag."""
        with pytest.raises(SystemExit) as exc_info:
            with patch.object(sys, "argv", ["image-to-pdf", "--help"]):
                main()

        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "Convert images to PDF" in captured.out
        assert "-o" in captured.out
        assert "--output" in captured.out
