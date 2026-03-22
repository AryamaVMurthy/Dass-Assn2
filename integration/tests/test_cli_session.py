"""CLI-session tests for the StreetRace Manager terminal interface."""

import json

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
