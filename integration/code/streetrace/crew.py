"""Crew management service for StreetRace Manager."""


class CrewService:
    """Manages crew roles and skill levels."""

    def __init__(self, registration_service):
        """Bind crew management to registered members."""
        self._registration = registration_service

    def assign_role(self, member_id, role, skill_level):
        """Assign a role and skill level to a registered member."""
        member = self._registration.get_member(member_id)
        member.role = role
        member.skill_level = skill_level
        return member

    def get_members_by_role(self, role):
        """Return all members that match a role."""
        return [
            member for member in self._registration.list_members() if member.role == role
        ]

    def role_available(self, role):
        """Return whether at least one member has the requested role."""
        return bool(self.get_members_by_role(role))
