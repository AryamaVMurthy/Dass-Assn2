"""Shared data models for StreetRace Manager."""

from dataclasses import dataclass


@dataclass
class CrewMember:
    """Represents a registered crew member."""

    member_id: str
    name: str
    role: str
    skill_level: int = 0


@dataclass
class Vehicle:
    """Represents a vehicle tracked by the system."""

    vehicle_id: str
    model: str
    brand: str
    is_damaged: bool = False
    damage_severity: str = "none"
