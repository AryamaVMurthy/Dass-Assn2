"""Final white-box coverage cases to round the suite to 73 tests."""

import pytest

from moneypoly.bank import Bank
from moneypoly.game import Game


def test_move_and_resolve_railroad_without_property_only_checks_bankruptcy(monkeypatch):
    """A railroad tile with no property should fall through to bankruptcy checking."""
    game = Game(["Alice", "Bob"])
    player = game.players[0]
    seen = []

    monkeypatch.setattr(player, "move", lambda _steps: setattr(player, "position", 5))
    monkeypatch.setattr(game.board, "get_property_at", lambda _position: None)
    monkeypatch.setattr(game, "_check_bankruptcy", lambda target: seen.append(target))

    game._move_and_resolve(player, 0)

    assert seen == [player]


def test_move_and_resolve_property_without_property_object_only_checks_bankruptcy(monkeypatch):
    """A property tile with no resolved property object should not crash."""
    game = Game(["Alice", "Bob"])
    player = game.players[0]
    seen = []

    monkeypatch.setattr(player, "move", lambda _steps: setattr(player, "position", 1))
    monkeypatch.setattr(game.board, "get_property_at", lambda _position: None)
    monkeypatch.setattr(game.board, "get_tile_type", lambda _position: "property")
    monkeypatch.setattr(game, "_check_bankruptcy", lambda target: seen.append(target))

    game._move_and_resolve(player, 0)

    assert seen == [player]


def test_handle_property_tile_auction_branch_calls_auction(monkeypatch):
    """Choosing auction should delegate to the auction handler."""
    game = Game(["Alice", "Bob"])
    player = game.players[0]
    prop = game.board.get_property_at(1)
    seen = []

    monkeypatch.setattr("builtins.input", lambda _prompt: "a")
    monkeypatch.setattr(game, "auction_property", lambda target_prop: seen.append(target_prop))

    game._handle_property_tile(player, prop)

    assert seen == [prop]


def test_bank_collect_negative_amount_is_rejected():
    """Negative collections should fail fast instead of mutating bank state."""
    bank = Bank()
    starting_balance = bank.get_balance()

    with pytest.raises(ValueError, match="Cannot collect a negative amount"):
        bank.collect(-50)

    assert bank.get_balance() == starting_balance
