"""Registration service for StreetRace Manager."""

from streetrace.models import CrewMember


class RegistrationService:
    """Registers and stores crew members."""

    def __init__(self):
        """Initialize registration storage."""
        self._members = {}
        self._next_member_number = 1

    def register_member(self, name, role):
        """Create and store a new crew member."""
        member_id = f"member-{self._next_member_number}"
        self._next_member_number += 1
        member = CrewMember(member_id=member_id, name=name, role=role)
        self._members[member_id] = member
        return member

    def get_member(self, member_id):
        """Return a previously registered member."""
        member = self._members.get(member_id)
        if member is None:
            raise ValueError(f"Unknown crew member: {member_id}")
        return member

    def list_members(self):
        """Return all registered members."""
        return list(self._members.values())
