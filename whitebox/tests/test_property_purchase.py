"""White-box tests for property purchase behavior."""

from moneypoly.game import Game
from moneypoly.property import Property


def test_buy_property_allows_exact_balance_purchase():
    """A player should be able to buy a property using their full balance."""
    game = Game(["Alice", "Bob"])
    player = game.players[0]
    prop = Property("Test Avenue", 1, 100, 10)
    player.balance = 100

    bought = game.buy_property(player, prop)

    assert bought is True
    assert prop.owner is player
    assert player.balance == 0
