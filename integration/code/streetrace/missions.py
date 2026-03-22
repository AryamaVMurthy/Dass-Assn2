"""Mission planning service for StreetRace Manager."""

from collections import Counter

from streetrace.models import Mission


class MissionPlanningService:
    """Creates missions and validates operational readiness."""

    def __init__(self, crew_service, garage_service):
        """Bind missions to crew and vehicle availability."""
        self._crew = crew_service
        self._garage = garage_service
        self._missions = {}
        self._next_mission_number = 1

    def create_mission(self, name, required_roles, vehicle_id=None):
        """Create a mission definition."""
        mission_id = f"mission-{self._next_mission_number}"
        self._next_mission_number += 1
        mission = Mission(
            mission_id=mission_id,
            name=name,
            required_roles=list(required_roles),
            vehicle_id=vehicle_id,
        )
        self._missions[mission_id] = mission
        return mission

    def start_mission(self, mission_id):
        """Start a mission if all role and vehicle checks pass."""
        mission = self._get_mission(mission_id)
        self.validate_required_roles(mission.required_roles)
        if mission.vehicle_id and not self._garage.is_vehicle_available(mission.vehicle_id):
            raise ValueError("Vehicle is damaged and unavailable for mission")
        mission.status = "active"
        return mission

    def validate_required_roles(self, required_roles):
        """Ensure all required roles exist in the crew roster."""
        required_counts = Counter(required_roles)
        missing_roles = []
        for role, required_count in required_counts.items():
            available_count = len(self._crew.get_members_by_role(role))
            if available_count < required_count:
                missing_roles.append(f"{role} x{required_count}")
        if missing_roles:
            raise ValueError(
                f"Missing required role slots: {', '.join(missing_roles)}"
            )
        return True

    def _get_mission(self, mission_id):
        """Return a mission by id."""
        mission = self._missions.get(mission_id)
        if mission is None:
            raise ValueError(f"Unknown mission: {mission_id}")
        return mission
