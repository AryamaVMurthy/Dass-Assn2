"""Integration tests for mission planning and cross-module validation."""

import pytest

from streetrace.app import StreetRaceApp


def test_mission_cannot_start_when_required_role_is_unavailable():
    """Mission start should fail fast when a required role is missing."""
    app = StreetRaceApp()

    app.registration.register_member("Tara", "rookie")
    mission = app.missions.create_mission("Night Delivery", ["driver", "mechanic"])

    with pytest.raises(
        ValueError, match="Missing required role slots: driver x1, mechanic x1"
    ):
        app.missions.start_mission(mission.mission_id)


def test_damaged_vehicle_blocks_mission_until_mechanic_repairs_it():
    """A damaged mission vehicle should block start until repaired."""
    app = StreetRaceApp()

    driver = app.registration.register_member("Zoya", "rookie")
    app.crew.assign_role(driver.member_id, "driver", 8)
    vehicle = app.inventory.add_vehicle("Charger", "Dodge")
    race = app.race.create_race("Tunnel Clash", 2500)
    app.race.enter_driver(race.race_id, driver.member_id, vehicle.vehicle_id)
    result = app.race.complete_race(race.race_id, position=2, damaged=True)
    app.results.record_result(result)

    mission = app.missions.create_mission(
        "Rescue Run", ["driver"], vehicle_id=vehicle.vehicle_id
    )

    with pytest.raises(ValueError, match="Vehicle is damaged"):
        app.missions.start_mission(mission.mission_id)

    mechanic = app.registration.register_member("Arjun", "rookie")
    app.crew.assign_role(mechanic.member_id, "mechanic", 7)
    app.garage.repair_vehicle(vehicle.vehicle_id, mechanic.member_id)

    started = app.missions.start_mission(mission.mission_id)

    assert started.status == "active"


def test_mission_requires_enough_people_for_duplicate_role_requirements():
    """Repeated role requirements should require multiple matching crew members."""
    app = StreetRaceApp()

    driver = app.registration.register_member("Nia", "rookie")
    app.crew.assign_role(driver.member_id, "driver", 8)
    mission = app.missions.create_mission("Twin Driver Run", ["driver", "driver"])

    with pytest.raises(ValueError, match="Missing required role slots: driver x2"):
        app.missions.start_mission(mission.mission_id)
