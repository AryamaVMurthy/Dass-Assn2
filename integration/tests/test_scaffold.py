"""Smoke tests for the StreetRace Manager package scaffold."""

from streetrace.app import StreetRaceApp


def test_app_can_be_constructed():
    """The top-level application object should be importable and constructible."""
    app = StreetRaceApp()

    assert app is not None
