"""Ledger service for StreetRace Manager."""

from streetrace.models import LedgerEntry


class LedgerService:
    """Tracks money movements across the system."""

    def __init__(self):
        """Initialize the ledger."""
        self._entries = []

    def record_entry(self, kind, amount, description):
        """Store a ledger entry."""
        self._entries.append(
            LedgerEntry(kind=kind, amount=amount, description=description)
        )

    def list_entries(self):
        """Return recorded ledger entries."""
        return list(self._entries)
