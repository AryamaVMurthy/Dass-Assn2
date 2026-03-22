"""White-box tests for jail-turn behavior."""

from moneypoly.config import JAIL_FINE
from moneypoly.game import Game


def test_paying_jail_fine_deducts_money_from_player(monkeypatch):
    """Voluntarily paying the jail fine should reduce the player's balance."""
    game = Game(["Alice", "Bob"])
    player = game.players[0]
    player.in_jail = True
    starting_balance = player.balance

    monkeypatch.setattr("moneypoly.game.ui.confirm", lambda _prompt: True)
    monkeypatch.setattr(game.dice, "roll", lambda: 0)
    monkeypatch.setattr(game.dice, "describe", lambda: "0 + 0 = 0")
    monkeypatch.setattr(game, "_move_and_resolve", lambda *_args: None)

    game._handle_jail_turn(player)

    assert player.balance == starting_balance - JAIL_FINE
