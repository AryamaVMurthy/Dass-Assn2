"""Shared data models for StreetRace Manager."""

from dataclasses import dataclass


@dataclass
class CrewMember:
    """Represents a registered crew member."""

    member_id: str
    name: str
    role: str
    skill_level: int = 0
