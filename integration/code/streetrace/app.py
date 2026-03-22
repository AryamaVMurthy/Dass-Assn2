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
        registration = RegistrationService()
        crew = CrewService(registration)
        inventory = InventoryService()
        garage = GarageService(inventory, crew, registration)
        ledger = LedgerService()
        race = RaceService(registration, inventory, garage)
        results = ResultsService(inventory, ledger)
        missions = MissionPlanningService(crew, garage)
        self._services = {
            "registration": registration,
            "crew": crew,
            "inventory": inventory,
            "garage": garage,
            "ledger": ledger,
            "race": race,
            "results": results,
            "missions": missions,
        }

    @property
    def registration(self):
        """Return the registration service."""
        return self._services["registration"]

    @property
    def crew(self):
        """Return the crew-management service."""
        return self._services["crew"]

    @property
    def inventory(self):
        """Return the inventory service."""
        return self._services["inventory"]

    @property
    def garage(self):
        """Return the garage service."""
        return self._services["garage"]

    @property
    def ledger(self):
        """Return the ledger service."""
        return self._services["ledger"]

    @property
    def race(self):
        """Return the race-management service."""
        return self._services["race"]

    @property
    def results(self):
        """Return the results service."""
        return self._services["results"]

    @property
    def missions(self):
        """Return the mission-planning service."""
        return self._services["missions"]

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
