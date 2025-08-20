"""Tests for the main module."""

from mypython.__main__ import main


def test_main() -> None:
    """Test the main function returns the expected greeting."""
    assert main() == "Hello from mypython!"
