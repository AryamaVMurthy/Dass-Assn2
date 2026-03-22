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


@dataclass
class Race:
    """Represents a race and its selected entry."""

    race_id: str
    name: str
    prize_money: int
    driver_id: str | None = None
    vehicle_id: str | None = None
    status: str = "planned"


@dataclass
class RaceResult:
    """Represents the final outcome of a completed race."""

    race_id: str
    member_id: str
    position: int
    prize_money: int
    damaged: bool


@dataclass
class RankingEntry:
    """Represents accumulated race points for a crew member."""

    member_id: str
    points: int


@dataclass
class LedgerEntry:
    """Represents a money movement in the system."""

    kind: str
    amount: int
    description: str


@dataclass
class Mission:
    """Represents a mission and its crew-role requirements."""

    mission_id: str
    name: str
    required_roles: list[str]
    vehicle_id: str | None = None
    status: str = "planned"
