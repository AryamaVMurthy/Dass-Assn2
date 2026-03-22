"""Additional white-box tests for player helper methods."""

import pytest

from moneypoly.player import Player


def test_add_money_rejects_negative_values():
    """Negative additions should raise a value error."""
    player = Player("Alice")

    with pytest.raises(ValueError):
        player.add_money(-1)


def test_deduct_money_rejects_negative_values():
    """Negative deductions should raise a value error."""
    player = Player("Alice")

    with pytest.raises(ValueError):
        player.deduct_money(-1)


def test_is_bankrupt_returns_true_at_zero_balance():
    """Zero balance should count as bankrupt."""
    player = Player("Alice")
    player.balance = 0

    assert player.is_bankrupt() is True


def test_status_line_includes_jail_tag_when_jailed():
    """The status line should show when a player is jailed."""
    player = Player("Alice")
    player.in_jail = True

    assert "[JAILED]" in player.status_line()


def test_remove_property_ignores_missing_property():
    """Removing a property not held by the player should be harmless."""
    player = Player("Alice")
    other = object()

    player.remove_property(other)

    assert player.properties == []
