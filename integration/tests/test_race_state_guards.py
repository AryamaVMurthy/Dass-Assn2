"""Integration tests for race state and vehicle availability guards."""

import pytest

from streetrace.app import StreetRaceApp


def test_vehicle_cannot_be_entered_into_two_active_races():
    """A vehicle reserved for one race should be unavailable to another."""
    app = StreetRaceApp()

    first_driver = app.register_member("Mira", "rookie")
    second_driver = app.register_member("Kian", "rookie")
    app.assign_role(first_driver.member_id, "driver", 9)
    app.assign_role(second_driver.member_id, "driver", 8)
    vehicle = app.add_vehicle("R34", "Nissan")
    first_race = app.create_race("Harbor Sprint", 2000)
    second_race = app.create_race("Dock Run", 1500)

    app.enter_race(first_race.race_id, first_driver.member_id, vehicle.vehicle_id)

    with pytest.raises(ValueError, match="Vehicle is not available"):
        app.enter_race(second_race.race_id, second_driver.member_id, vehicle.vehicle_id)

    app.complete_race(first_race.race_id, position=2, damaged=False)
    app.enter_race(second_race.race_id, second_driver.member_id, vehicle.vehicle_id)

    assert second_race.status == "ready"


def test_completed_race_cannot_be_reentered_or_completed_again():
    """Completed races should be terminal and reject repeat processing."""
    app = StreetRaceApp()

    driver = app.register_member("Sana", "rookie")
    app.assign_role(driver.member_id, "driver", 9)
    vehicle = app.add_vehicle("Eclipse", "Mitsubishi")
    race = app.create_race("Night Loop", 3200)

    app.enter_race(race.race_id, driver.member_id, vehicle.vehicle_id)
    first = app.complete_race(race.race_id, position=1, damaged=False)

    with pytest.raises(ValueError, match="Race is already completed"):
        app.enter_race(race.race_id, driver.member_id, vehicle.vehicle_id)

    with pytest.raises(ValueError, match="Race is already completed"):
        app.complete_race(race.race_id, position=1, damaged=False)

    assert first.race_id == race.race_id
