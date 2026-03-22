"""White-box tests for property group ownership rules."""

from moneypoly.player import Player
from moneypoly.property import Property, PropertyGroup


def test_rent_is_not_doubled_without_full_group_ownership():
    """Owning only one property in a group should not trigger monopoly rent."""
    owner = Player("Alice")
    group = PropertyGroup("Test Group", "red")
    first = Property("First", 1, 100, 20, group)
    Property("Second", 3, 100, 20, group)
    first.owner = owner
    owner.add_property(first)

    assert first.get_rent() == 20
