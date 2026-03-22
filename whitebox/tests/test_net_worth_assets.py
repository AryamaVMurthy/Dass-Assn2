"""White-box tests for asset-aware net worth calculations."""

from moneypoly.game import Game


def test_net_worth_includes_owned_property_value():
    """Owned property prices should contribute to a player's net worth."""
    game = Game(["Alice", "Bob"])
    player = game.players[0]
    prop = game.board.get_property_at(39)
    prop.owner = player
    player.add_property(prop)

    assert player.net_worth() == player.balance + prop.price


def test_find_winner_accounts_for_cash_and_property_assets():
    """Winner selection should include asset value, not cash alone."""
    game = Game(["Alice", "Bob"])
    alice = game.players[0]
    bob = game.players[1]
    alice.balance = 1000
    bob.balance = 1200
    prop = game.board.get_property_at(39)
    prop.owner = alice
    alice.add_property(prop)

    winner = game.find_winner()

    assert winner is alice
