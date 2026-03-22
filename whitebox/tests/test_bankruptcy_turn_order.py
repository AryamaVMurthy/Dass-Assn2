"""White-box tests for turn-order behavior after player elimination."""

from moneypoly.game import Game


def test_play_turn_keeps_next_player_after_current_player_is_eliminated(monkeypatch):
    """Eliminating the current player mid-turn should not skip the next player."""
    game = Game(["Alice", "Bob", "Cara"])
    game.current_index = 1
    player = game.current_player()

    monkeypatch.setattr(game.dice, "roll", lambda: 7)
    monkeypatch.setattr(game.dice, "describe", lambda: "3 + 4 = 7")
    monkeypatch.setattr(game.dice, "is_doubles", lambda: False)
    game.dice.doubles_streak = 0
    monkeypatch.setattr(game, "interactive_menu", lambda *_args: None)

    def bankrupt_current_player(target, _steps):
        target.balance = 0
        game._check_bankruptcy(target)

    monkeypatch.setattr(game, "_move_and_resolve", bankrupt_current_player)

    game.play_turn()

    assert player not in game.players
    assert game.current_player().name == "Cara"
    assert game.turn_number == 1


def test_play_turn_does_not_grant_doubles_retry_after_elimination(
    monkeypatch, capsys
):
    """A bankrupt player should not be told to roll again after doubles."""
    game = Game(["Alice", "Bob", "Cara"])
    game.current_index = 1
    player = game.current_player()

    monkeypatch.setattr(game.dice, "roll", lambda: 8)
    monkeypatch.setattr(game.dice, "describe", lambda: "4 + 4 = 8 (DOUBLES)")
    monkeypatch.setattr(game.dice, "is_doubles", lambda: True)
    game.dice.doubles_streak = 1
    monkeypatch.setattr(game, "interactive_menu", lambda *_args: None)

    def bankrupt_current_player(target, _steps):
        target.balance = 0
        game._check_bankruptcy(target)

    monkeypatch.setattr(game, "_move_and_resolve", bankrupt_current_player)

    game.play_turn()

    captured = capsys.readouterr().out
    assert player not in game.players
    assert "rolls again" not in captured
    assert game.current_player().name == "Cara"
    assert game.turn_number == 1


def test_play_turn_keeps_next_player_after_jailed_player_is_eliminated(monkeypatch):
    """Elimination during the jail branch should not skip the next active player."""
    game = Game(["Alice", "Bob", "Cara"])
    game.current_index = 1
    player = game.current_player()
    player.in_jail = True

    def eliminate_in_jail(target):
        target.balance = 0
        game._check_bankruptcy(target)

    monkeypatch.setattr(game, "_handle_jail_turn", eliminate_in_jail)

    game.play_turn()

    assert player not in game.players
    assert game.current_player().name == "Cara"
    assert game.turn_number == 1
