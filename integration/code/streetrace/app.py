"""Top-level application wiring for StreetRace Manager."""

from streetrace.crew import CrewService
from streetrace.registration import RegistrationService


class StreetRaceApp:
    """Application shell used to compose StreetRace services."""

    def __init__(self):
        """Initialize shared services for the CLI and tests."""
        self.registration = RegistrationService()
        self.crew = CrewService(self.registration)
