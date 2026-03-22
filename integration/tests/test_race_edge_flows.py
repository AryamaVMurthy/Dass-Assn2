"""Additional integration tests for race-related edge flows."""

import pytest

from streetrace.app import StreetRaceApp


def test_damaged_vehicle_cannot_be_entered_into_race():
    """Race entry should reject vehicles that are currently damaged."""
    app = StreetRaceApp()

    driver = app.registration.register_member("Ishaan", "rookie")
    app.crew.assign_role(driver.member_id, "driver", 8)
    vehicle = app.inventory.add_vehicle("Mustang", "Ford")
    app.garage.mark_damaged(vehicle.vehicle_id, "medium")
    race = app.race.create_race("Expressway Heat", 4000)

    with pytest.raises(ValueError, match="Vehicle is not available"):
        app.race.enter_driver(race.race_id, driver.member_id, vehicle.vehicle_id)


def test_rankings_are_sorted_by_points_after_multiple_results():
    """Higher-scoring drivers should appear first in rankings."""
    app = StreetRaceApp()

    first = app.registration.register_member("Sara", "rookie")
    second = app.registration.register_member("Kabir", "rookie")
    app.crew.assign_role(first.member_id, "driver", 9)
    app.crew.assign_role(second.member_id, "driver", 7)
    first_vehicle = app.inventory.add_vehicle("Civic", "Honda")
    second_vehicle = app.inventory.add_vehicle("Silvia", "Nissan")

    race_one = app.race.create_race("Metro Rush", 2000)
    app.race.enter_driver(race_one.race_id, second.member_id, second_vehicle.vehicle_id)
    app.results.record_result(app.race.complete_race(race_one.race_id, position=2, damaged=False))

    race_two = app.race.create_race("Coastal Dash", 4500)
    app.race.enter_driver(race_two.race_id, first.member_id, first_vehicle.vehicle_id)
    app.results.record_result(app.race.complete_race(race_two.race_id, position=1, damaged=False))

    rankings = app.results.get_rankings()

    assert [entry.member_id for entry in rankings] == [first.member_id, second.member_id]
