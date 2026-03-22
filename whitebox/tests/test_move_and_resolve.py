"""White-box tests covering tile-resolution branches."""

from moneypoly.config import INCOME_TAX_AMOUNT, LUXURY_TAX_AMOUNT
from moneypoly.game import Game


def test_move_and_resolve_go_to_jail_tile(monkeypatch):
    """Landing on the go-to-jail tile should jail the player."""
    game = Game(["Alice", "Bob"])
    player = game.players[0]
    monkeypatch.setattr(player, "move", lambda _steps: setattr(player, "position", 30))

    game._move_and_resolve(player, 0)

    assert player.in_jail is True
    assert player.position == 10


def test_move_and_resolve_income_tax_tile(monkeypatch):
    """Landing on income tax should deduct the configured amount."""
    game = Game(["Alice", "Bob"])
    player = game.players[0]
    starting_balance = player.balance
    starting_bank = game.bank.get_balance()
    monkeypatch.setattr(player, "move", lambda _steps: setattr(player, "position", 4))

    game._move_and_resolve(player, 0)

    assert player.balance == starting_balance - INCOME_TAX_AMOUNT
    assert game.bank.get_balance() == starting_bank + INCOME_TAX_AMOUNT


def test_move_and_resolve_luxury_tax_tile(monkeypatch):
    """Landing on luxury tax should deduct the configured amount."""
    game = Game(["Alice", "Bob"])
    player = game.players[0]
    starting_balance = player.balance
    starting_bank = game.bank.get_balance()
    monkeypatch.setattr(player, "move", lambda _steps: setattr(player, "position", 38))

    game._move_and_resolve(player, 0)

    assert player.balance == starting_balance - LUXURY_TAX_AMOUNT
    assert game.bank.get_balance() == starting_bank + LUXURY_TAX_AMOUNT


def test_move_and_resolve_chance_tile_draws_and_applies_card(monkeypatch):
    """Landing on chance should draw a card and apply its effect."""
    game = Game(["Alice", "Bob"])
    player = game.players[0]
    seen = []

    monkeypatch.setattr(player, "move", lambda _steps: setattr(player, "position", 7))
    monkeypatch.setattr(game.chance_deck, "draw", lambda: {"action": "collect", "value": 50})
    monkeypatch.setattr(game, "_apply_card", lambda target_player, card: seen.append((target_player, card)))

    game._move_and_resolve(player, 0)

    assert seen == [(player, {"action": "collect", "value": 50})]
