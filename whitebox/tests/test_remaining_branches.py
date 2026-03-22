"""Additional white-box tests for remaining edge branches."""

from moneypoly.board import Board
from moneypoly.game import Game


def test_handle_jail_turn_no_action_keeps_player_jailed(monkeypatch):
    """Declining all jail options before turn three should keep the player jailed."""
    game = Game(["Alice", "Bob"])
    player = game.players[0]
    player.in_jail = True
    player.jail_turns = 1

    monkeypatch.setattr("moneypoly.game.ui.confirm", lambda _prompt: False)

    game._handle_jail_turn(player)

    assert player.in_jail is True
    assert player.jail_turns == 2


def test_move_and_resolve_free_parking_does_not_change_balance(monkeypatch):
    """Free parking should leave the player's balance unchanged."""
    game = Game(["Alice", "Bob"])
    player = game.players[0]
    starting_balance = player.balance
    monkeypatch.setattr(player, "move", lambda _steps: setattr(player, "position", 20))

    game._move_and_resolve(player, 0)

    assert player.balance == starting_balance


def test_move_and_resolve_community_chest_draws_and_applies_card(monkeypatch):
    """Community chest tiles should draw and apply a community card."""
    game = Game(["Alice", "Bob"])
    player = game.players[0]
    seen = []

    monkeypatch.setattr(player, "move", lambda _steps: setattr(player, "position", 2))
    monkeypatch.setattr(game.community_deck, "draw", lambda: {"action": "collect", "value": 25})
    monkeypatch.setattr(game, "_apply_card", lambda target_player, card: seen.append((target_player, card)))

    game._move_and_resolve(player, 0)

    assert seen == [(player, {"action": "collect", "value": 25})]


def test_move_and_resolve_blank_tile_only_checks_bankruptcy(monkeypatch):
    """Blank tiles should not trigger special actions beyond bankruptcy checks."""
    game = Game(["Alice", "Bob"])
    player = game.players[0]
    seen = []

    monkeypatch.setattr(player, "move", lambda _steps: setattr(player, "position", 12))
    monkeypatch.setattr(game, "_check_bankruptcy", lambda target: seen.append(target))

    game._move_and_resolve(player, 0)

    assert seen == [player]


def test_check_bankruptcy_resets_current_index_when_removed_player_was_last():
    """Removing the last indexed player should reset current_index to zero."""
    game = Game(["Alice", "Bob"])
    player = game.players[1]
    game.current_index = 1
    player.balance = 0

    game._check_bankruptcy(player)

    assert game.current_index == 0


def test_board_is_purchasable_for_unowned_non_mortgaged_property():
    """Unowned, unmortgaged properties should be purchasable."""
    board = Board()

    assert board.is_purchasable(1) is True
