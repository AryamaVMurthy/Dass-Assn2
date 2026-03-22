"""White-box tests for winner selection in MoneyPoly."""

from moneypoly.game import Game


def test_find_winner_returns_player_with_highest_net_worth():
    """Winner selection should choose the richest remaining player."""
    game = Game(["Alice", "Bob"])
    game.players[0].balance = 1500
    game.players[1].balance = 2200

    winner = game.find_winner()

    assert winner is game.players[1]
