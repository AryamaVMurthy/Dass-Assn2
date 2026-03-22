"""Top-level application wiring for StreetRace Manager."""

from streetrace.crew import CrewService
from streetrace.garage import GarageService
from streetrace.inventory import InventoryService
from streetrace.ledger import LedgerService
from streetrace.missions import MissionPlanningService
from streetrace.race import RaceService
from streetrace.registration import RegistrationService
from streetrace.results import ResultsService


class StreetRaceApp:
    """Application shell used to compose StreetRace services."""

    def __init__(self):
        """Initialize shared services for the CLI and tests."""
        self.registration = RegistrationService()
        self.crew = CrewService(self.registration)
        self.inventory = InventoryService()
        self.garage = GarageService(self.inventory, self.crew, self.registration)
        self.ledger = LedgerService()
        self.race = RaceService(self.registration, self.inventory, self.garage)
        self.results = ResultsService(self.inventory, self.ledger)
        self.missions = MissionPlanningService(self.crew, self.garage)

    def register_member(self, name, role):
        """Register a crew member."""
        return self.registration.register_member(name, role)

    def assign_role(self, member_id, role, skill_level):
        """Assign a role to a crew member."""
        return self.crew.assign_role(member_id, role, skill_level)

    def add_vehicle(self, model, brand):
        """Add a vehicle to inventory."""
        return self.inventory.add_vehicle(model, brand)

    def create_race(self, name, prize_money):
        """Create a race."""
        return self.race.create_race(name, prize_money)

    def enter_race(self, race_id, member_id, vehicle_id):
        """Enter a driver and vehicle into a race."""
        self.race.enter_driver(race_id, member_id, vehicle_id)

    def complete_race(self, race_id, position, damaged):
        """Complete a race and record the resulting outcome."""
        result = self.race.complete_race(race_id, position, damaged)
        self.results.record_result(result)
        return result

    def create_mission(self, name, required_roles, vehicle_id=None):
        """Create a mission."""
        return self.missions.create_mission(name, required_roles, vehicle_id=vehicle_id)

    def start_mission(self, mission_id):
        """Start a mission after validation."""
        return self.missions.start_mission(mission_id)

    def repair_vehicle(self, vehicle_id, mechanic_id):
        """Repair a vehicle through the garage service."""
        self.garage.repair_vehicle(vehicle_id, mechanic_id)

    def summary(self):
        """Return a compact summary of current system state."""
        return {
            "registered_members": len(self.registration.list_members()),
            "vehicles": len(self.inventory.list_vehicles()),
            "cash_balance": self.inventory.cash_balance,
            "rankings": [
                {"member_id": entry.member_id, "points": entry.points}
                for entry in self.results.get_rankings()
            ],
        }
