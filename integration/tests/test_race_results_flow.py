"""Integration tests for race execution, results, and prize money flow."""

import pytest

from streetrace.app import StreetRaceApp


def test_registered_driver_can_complete_race_and_update_cash_rankings_and_ledger():
    """Race completion should update rankings and inventory cash."""
    app = StreetRaceApp()

    driver = app.registration.register_member("Mira", "rookie")
    app.crew.assign_role(driver.member_id, "driver", 9)
    vehicle = app.inventory.add_vehicle("RX-7", "Mazda")
    race = app.race.create_race("Harbor Sprint", 5000)

    app.race.enter_driver(race.race_id, driver.member_id, vehicle.vehicle_id)
    result = app.race.complete_race(race.race_id, position=1, damaged=False)

    app.results.record_result(result)

    rankings = app.results.get_rankings()
    ledger_entries = app.ledger.list_entries()

    assert rankings[0].member_id == driver.member_id
    assert rankings[0].points == 10
    assert app.inventory.cash_balance == 5000
    assert ledger_entries[-1].amount == 5000
    assert ledger_entries[-1].kind == "prize"


def test_only_registered_drivers_can_be_entered_into_a_race():
    """Race entry should fail for unknown members and non-drivers."""
    app = StreetRaceApp()

    strategist = app.registration.register_member("Neel", "rookie")
    app.crew.assign_role(strategist.member_id, "strategist", 6)
    vehicle = app.inventory.add_vehicle("Evo", "Mitsubishi")
    race = app.race.create_race("Dock Run", 3000)

    with pytest.raises(ValueError, match="Unknown crew member"):
        app.race.enter_driver(race.race_id, "missing-member", vehicle.vehicle_id)

    with pytest.raises(ValueError, match="Driver role required"):
        app.race.enter_driver(race.race_id, strategist.member_id, vehicle.vehicle_id)
