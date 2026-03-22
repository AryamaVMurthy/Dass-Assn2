"""Race management service for StreetRace Manager."""

from streetrace.models import Race, RaceResult


class RaceService:
    """Creates races, validates entries, and completes races."""

    def __init__(self, registration_service, inventory_service, garage_service):
        """Bind race management to crew and vehicle state."""
        self._registration = registration_service
        self._inventory = inventory_service
        self._garage = garage_service
        self._races = {}
        self._next_race_number = 1

    def create_race(self, name, prize_money):
        """Create a new race."""
        race_id = f"race-{self._next_race_number}"
        self._next_race_number += 1
        race = Race(race_id=race_id, name=name, prize_money=prize_money)
        self._races[race_id] = race
        return race

    def enter_driver(self, race_id, member_id, vehicle_id):
        """Enter a valid driver and vehicle into a race."""
        race = self._get_race(race_id)
        member = self._registration.get_member(member_id)
        if member.role != "driver":
            raise ValueError("Driver role required for race entry")
        self._inventory.get_vehicle(vehicle_id)
        if not self._garage.is_vehicle_available(vehicle_id):
            raise ValueError("Vehicle is not available for race entry")
        self._inventory.reserve_vehicle(vehicle_id)
        race.driver_id = member_id
        race.vehicle_id = vehicle_id
        race.status = "ready"

    def complete_race(self, race_id, position, damaged):
        """Complete a race and return the result payload."""
        race = self._get_race(race_id)
        if race.driver_id is None or race.vehicle_id is None:
            raise ValueError("Race entry required before completion")
        if damaged:
            self._garage.mark_damaged(race.vehicle_id, "race-damage")
        self._inventory.release_vehicle(race.vehicle_id)
        race.status = "completed"
        prize_money = race.prize_money if position == 1 else 0
        return RaceResult(
            race_id=race.race_id,
            member_id=race.driver_id,
            position=position,
            prize_money=prize_money,
            damaged=damaged,
        )

    def _get_race(self, race_id):
        """Return a stored race by id."""
        race = self._races.get(race_id)
        if race is None:
            raise ValueError(f"Unknown race: {race_id}")
        return race
