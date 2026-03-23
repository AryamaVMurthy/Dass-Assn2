"""CLI-session tests for the StreetRace Manager terminal interface."""

import json

import pytest

from main import run_cli_session
from streetrace.app import StreetRaceApp


def test_cli_session_can_run_end_to_end_workflow():
    """The interactive CLI should support a full workflow in one process."""
    app = StreetRaceApp()
    commands = iter(
        [
            "register Mira rookie",
            "assign-role member-1 driver 9",
            "add-vehicle RX7 Mazda",
            "create-race HarborSprint 5000",
            "enter-race race-1 member-1 vehicle-1",
            "complete-race race-1 1 false",
            "summary",
            "quit",
        ]
    )
    outputs = []

    run_cli_session(
        app,
        input_func=lambda _prompt: next(commands),
        output_func=outputs.append,
    )

    summary = json.loads(outputs[-2])
    assert summary["registered_members"] == 1
    assert summary["vehicles"] == 1
    assert summary["cash_balance"] == 5000
    assert summary["rankings"][0]["member_id"] == "member-1"


def test_cli_session_rejects_invalid_damaged_token():
    """The CLI should fail fast on damaged flags other than true or false."""
    app = StreetRaceApp()
    commands = iter(
        [
            "register Mira rookie",
            "assign-role member-1 driver 9",
            "add-vehicle RX7 Mazda",
            "create-race HarborSprint 5000",
            "enter-race race-1 member-1 vehicle-1",
            "complete-race race-1 1 maybe",
        ]
    )

    with pytest.raises(ValueError, match="Damaged must be true or false"):
        run_cli_session(
            app,
            input_func=lambda _prompt: next(commands),
            output_func=lambda _message: None,
        )
