"""Additional white-box tests for play-turn branches."""

from moneypoly.game import Game


def test_play_turn_advances_turn_after_normal_non_double_roll(monkeypatch):
    """A normal turn should advance to the next player."""
    game = Game(["Alice", "Bob"])
    player = game.players[0]

    monkeypatch.setattr(game, "interactive_menu", lambda *_args: None)
    monkeypatch.setattr(game.dice, "roll", lambda: 7)
    monkeypatch.setattr(game.dice, "describe", lambda: "3 + 4 = 7")
    monkeypatch.setattr(game.dice, "is_doubles", lambda: False)
    game.dice.doubles_streak = 0
    monkeypatch.setattr(game, "_move_and_resolve", lambda *_args: None)

    game.play_turn()

    assert game.current_index == 1
    assert game.turn_number == 1
    assert game.current_player() is not player


def test_play_turn_keeps_same_player_on_doubles(monkeypatch):
    """Rolling doubles should not advance the turn order."""
    game = Game(["Alice", "Bob"])

    monkeypatch.setattr(game, "interactive_menu", lambda *_args: None)
    monkeypatch.setattr(game.dice, "roll", lambda: 8)
    monkeypatch.setattr(game.dice, "describe", lambda: "4 + 4 = 8 (DOUBLES)")
    monkeypatch.setattr(game.dice, "is_doubles", lambda: True)
    game.dice.doubles_streak = 1
    monkeypatch.setattr(game, "_move_and_resolve", lambda *_args: None)

    game.play_turn()

    assert game.current_index == 0
    assert game.turn_number == 0


def test_play_turn_sends_player_to_jail_after_three_doubles(monkeypatch):
    """Three consecutive doubles should jail the current player immediately."""
    game = Game(["Alice", "Bob"])
    player = game.players[0]

    monkeypatch.setattr(game, "interactive_menu", lambda *_args: None)
    monkeypatch.setattr(game.dice, "roll", lambda: 6)
    monkeypatch.setattr(game.dice, "describe", lambda: "3 + 3 = 6 (DOUBLES)")
    monkeypatch.setattr(game.dice, "is_doubles", lambda: True)
    game.dice.doubles_streak = 3

    game.play_turn()

    assert player.in_jail is True
    assert game.current_index == 1
    assert game.turn_number == 1


def test_play_turn_calls_jail_handler_for_jailed_player(monkeypatch):
    """Jailed players should take the jail branch before any normal roll."""
    game = Game(["Alice", "Bob"])
    player = game.players[0]
    player.in_jail = True
    calls = []

    monkeypatch.setattr(game, "_handle_jail_turn", lambda target: calls.append(target))

    game.play_turn()

    assert calls == [player]
    assert game.current_index == 1
    assert game.turn_number == 1


def test_play_turn_calls_interactive_menu_before_normal_roll(monkeypatch):
    """Non-jailed turns should expose the pre-roll menu before rolling."""
    game = Game(["Alice", "Bob"])
    player = game.players[0]
    calls = []

    monkeypatch.setattr(game, "interactive_menu", lambda target: calls.append(target))
    monkeypatch.setattr(game.dice, "roll", lambda: 7)
    monkeypatch.setattr(game.dice, "describe", lambda: "3 + 4 = 7")
    monkeypatch.setattr(game.dice, "is_doubles", lambda: False)
    game.dice.doubles_streak = 0
    monkeypatch.setattr(game, "_move_and_resolve", lambda *_args: None)

    game.play_turn()

    assert calls == [player]
