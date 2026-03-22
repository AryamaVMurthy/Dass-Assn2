"""White-box tests for property trading behavior."""

from moneypoly.game import Game
from moneypoly.property import Property


def test_trade_transfers_cash_to_seller():
    """A successful trade should move cash from buyer to seller."""
    game = Game(["Alice", "Bob"])
    seller = game.players[0]
    buyer = game.players[1]
    prop = Property("Trade Avenue", 1, 100, 10)
    prop.owner = seller
    seller.add_property(prop)

    seller_start = seller.balance
    buyer_start = buyer.balance

    traded = game.trade(seller, buyer, prop, 200)

    assert traded is True
    assert seller.balance == seller_start + 200
    assert buyer.balance == buyer_start - 200
    assert prop.owner is buyer
