"""White-box tests for unmortgaging behavior."""

from moneypoly.game import Game
from moneypoly.property import Property


def test_unmortgage_keeps_property_mortgaged_when_player_cannot_afford_cost():
    """A failed unmortgage attempt should not clear the mortgage state."""
    game = Game(["Alice", "Bob"])
    player = game.players[0]
    prop = Property("Mortgage Avenue", 1, 200, 20)
    prop.owner = player
    player.add_property(prop)
    prop.is_mortgaged = True
    player.balance = 50

    unmortgaged = game.unmortgage_property(player, prop)

    assert unmortgaged is False
    assert prop.is_mortgaged is True
