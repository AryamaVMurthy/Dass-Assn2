"""White-box tests covering additional jail-turn branches."""

from moneypoly.config import JAIL_FINE
from moneypoly.game import Game


def test_handle_jail_turn_uses_jail_free_card_when_confirmed(monkeypatch):
    """Using a jail-free card should consume the card and release the player."""
    game = Game(["Alice", "Bob"])
    player = game.players[0]
    player.in_jail = True
    player.get_out_of_jail_cards = 1

    monkeypatch.setattr("moneypoly.game.ui.confirm", lambda _prompt: True)
    monkeypatch.setattr(game.dice, "roll", lambda: 0)
    monkeypatch.setattr(game.dice, "describe", lambda: "0 + 0 = 0")
    monkeypatch.setattr(game, "_move_and_resolve", lambda *_args: None)

    game._handle_jail_turn(player)

    assert player.in_jail is False
    assert player.get_out_of_jail_cards == 0
    assert player.jail_turns == 0


def test_handle_jail_turn_forces_release_after_third_turn(monkeypatch):
    """Serving three turns in jail should force release with the mandatory fine."""
    game = Game(["Alice", "Bob"])
    player = game.players[0]
    player.in_jail = True
    player.jail_turns = 2
    starting_balance = player.balance

    monkeypatch.setattr("moneypoly.game.ui.confirm", lambda _prompt: False)
    monkeypatch.setattr(game.dice, "roll", lambda: 0)
    monkeypatch.setattr(game.dice, "describe", lambda: "0 + 0 = 0")
    monkeypatch.setattr(game, "_move_and_resolve", lambda *_args: None)

    game._handle_jail_turn(player)

    assert player.in_jail is False
    assert player.jail_turns == 0
    assert player.balance == starting_balance - JAIL_FINE
