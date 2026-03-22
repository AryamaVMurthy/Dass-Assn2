"""Garage service for StreetRace Manager."""


class GarageService:
    """Tracks vehicle condition and repair status."""

    def __init__(self, inventory_service, crew_service, registration_service):
        """Bind garage operations to inventory and crew data."""
        self._inventory = inventory_service
        self._crew = crew_service
        self._registration = registration_service

    def mark_damaged(self, vehicle_id, severity):
        """Mark a vehicle as damaged."""
        vehicle = self._inventory.get_vehicle(vehicle_id)
        vehicle.is_damaged = True
        vehicle.damage_severity = severity

    def repair_vehicle(self, vehicle_id, mechanic_id):
        """Repair a damaged vehicle using an available mechanic."""
        mechanic = self._registration.get_member(mechanic_id)
        if mechanic.role != "mechanic":
            raise ValueError("Mechanic role required for repairs")
        vehicle = self._inventory.get_vehicle(vehicle_id)
        vehicle.is_damaged = False
        vehicle.damage_severity = "none"

    def is_vehicle_available(self, vehicle_id):
        """Return whether a vehicle is available for use."""
        vehicle = self._inventory.get_vehicle(vehicle_id)
        return not vehicle.is_damaged
