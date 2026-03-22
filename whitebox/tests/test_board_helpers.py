"""Additional white-box tests for board helper methods."""

from moneypoly.board import Board
from moneypoly.player import Player


def test_get_tile_type_returns_blank_for_non_special_empty_tile():
    """Blank board positions should be identified as blank."""
    board = Board()

    assert board.get_tile_type(12) == "blank"


def test_get_tile_type_returns_railroad_for_railroad_position():
    """Railroad positions should resolve to the railroad tile type."""
    board = Board()

    assert board.get_tile_type(5) == "railroad"


def test_is_special_tile_distinguishes_special_and_normal_tiles():
    """Special tile lookup should only be true for configured special positions."""
    board = Board()

    assert board.is_special_tile(7) is True
    assert board.is_special_tile(1) is False


def test_properties_owned_by_returns_only_matching_players_properties():
    """Property ownership filtering should return only properties owned by the target player."""
    board = Board()
    alice = Player("Alice")
    bob = Player("Bob")
    first = board.get_property_at(1)
    second = board.get_property_at(3)
    first.owner = alice
    second.owner = bob

    assert board.properties_owned_by(alice) == [first]


def test_unowned_properties_excludes_owned_properties():
    """Unowned property listing should not include already owned properties."""
    board = Board()
    owner = Player("Owner")
    first = board.get_property_at(1)
    first.owner = owner

    assert first not in board.unowned_properties()
