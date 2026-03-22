"""Inventory service for StreetRace Manager."""

from streetrace.models import Vehicle


class InventoryService:
    """Tracks vehicles, supplies, and the system cash balance."""

    def __init__(self):
        """Initialize inventory state."""
        self._vehicles = {}
        self._parts = {}
        self._tools = {}
        self.cash_balance = 0
        self._next_vehicle_number = 1

    def add_vehicle(self, model, brand):
        """Create and store a vehicle."""
        vehicle_id = f"vehicle-{self._next_vehicle_number}"
        self._next_vehicle_number += 1
        vehicle = Vehicle(vehicle_id=vehicle_id, model=model, brand=brand)
        self._vehicles[vehicle_id] = vehicle
        return vehicle

    def get_vehicle(self, vehicle_id):
        """Return a tracked vehicle."""
        vehicle = self._vehicles.get(vehicle_id)
        if vehicle is None:
            raise ValueError(f"Unknown vehicle: {vehicle_id}")
        return vehicle

    def list_vehicles(self):
        """Return all tracked vehicles."""
        return list(self._vehicles.values())

    def reserve_vehicle(self, vehicle_id):
        """Reserve a vehicle for active use."""
        vehicle = self.get_vehicle(vehicle_id)
        if vehicle.is_reserved:
            raise ValueError(f"Vehicle is already reserved: {vehicle_id}")
        vehicle.is_reserved = True
        return vehicle

    def release_vehicle(self, vehicle_id):
        """Release a vehicle from active use."""
        vehicle = self.get_vehicle(vehicle_id)
        vehicle.is_reserved = False
        return vehicle

    def adjust_cash(self, amount, _reason):
        """Adjust the tracked cash balance."""
        self.cash_balance += amount

    def add_part(self, name, quantity):
        """Increase spare-part inventory."""
        self._parts[name] = self._parts.get(name, 0) + quantity

    def add_tool(self, name, quantity):
        """Increase tool inventory."""
        self._tools[name] = self._tools.get(name, 0) + quantity
