"""Tests for the app-level orchestration facade."""

from streetrace.app import StreetRaceApp


def test_app_summary_reports_cash_rankings_and_resource_counts():
    """The app facade should expose a readable summary of system state."""
    app = StreetRaceApp()

    driver = app.register_member("Leena", "rookie")
    app.assign_role(driver.member_id, "driver", 9)
    vehicle = app.add_vehicle("Impreza", "Subaru")
    race = app.create_race("City Sprint", 3200)
    app.enter_race(race.race_id, driver.member_id, vehicle.vehicle_id)
    app.complete_race(race.race_id, position=1, damaged=False)

    summary = app.summary()

    assert summary["cash_balance"] == 3200
    assert summary["registered_members"] == 1
    assert summary["vehicles"] == 1
    assert summary["rankings"][0]["member_id"] == driver.member_id
