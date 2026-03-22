"""Integration-style tests for registration and crew services."""

import pytest

from streetrace.app import StreetRaceApp


def test_register_member_and_assign_role_updates_skill_level():
    """A registered member should be assignable to a role with a skill level."""
    app = StreetRaceApp()

    member = app.registration.register_member("Riya", "rookie")
    updated = app.crew.assign_role(member.member_id, "driver", 8)

    assert updated.role == "driver"
    assert updated.skill_level == 8
    assert app.crew.role_available("driver") is True


def test_assign_role_requires_registered_member():
    """Role assignment should fail for unknown crew members."""
    app = StreetRaceApp()

    with pytest.raises(ValueError, match="Unknown crew member"):
        app.crew.assign_role("missing-member", "driver", 5)
