"""Integration-style tests for inventory and garage services."""

import pytest

from streetrace.app import StreetRaceApp


def test_added_vehicle_becomes_unavailable_when_damaged_and_available_after_repair():
    """Garage repairs should restore availability when a mechanic is assigned."""
    app = StreetRaceApp()

    mechanic = app.registration.register_member("Kabir", "rookie")
    app.crew.assign_role(mechanic.member_id, "mechanic", 7)
    vehicle = app.inventory.add_vehicle("Skyline", "Nissan")

    assert app.garage.is_vehicle_available(vehicle.vehicle_id) is True

    app.garage.mark_damaged(vehicle.vehicle_id, "medium")

    assert app.garage.is_vehicle_available(vehicle.vehicle_id) is False

    app.garage.repair_vehicle(vehicle.vehicle_id, mechanic.member_id)

    assert app.garage.is_vehicle_available(vehicle.vehicle_id) is True


def test_repair_requires_a_mechanic_role():
    """Repairs should fail when the assigned crew member is not a mechanic."""
    app = StreetRaceApp()

    driver = app.registration.register_member("Asha", "rookie")
    app.crew.assign_role(driver.member_id, "driver", 9)
    vehicle = app.inventory.add_vehicle("Supra", "Toyota")
    app.garage.mark_damaged(vehicle.vehicle_id, "high")

    with pytest.raises(ValueError, match="Mechanic role required"):
        app.garage.repair_vehicle(vehicle.vehicle_id, driver.member_id)
