"""Additional white-box tests for failure branches."""

from moneypoly.game import Game
from moneypoly.property import Property


def test_buy_property_fails_when_player_cannot_afford_cost():
    """Property purchase should fail when the player lacks enough money."""
    game = Game(["Alice", "Bob"])
    player = game.players[0]
    prop = Property("Expensive Avenue", 1, 500, 20)
    player.balance = 100

    bought = game.buy_property(player, prop)

    assert bought is False
    assert prop.owner is None


def test_mortgage_property_fails_for_non_owner():
    """Only the owner should be able to mortgage a property."""
    game = Game(["Alice", "Bob"])
    player = game.players[0]
    owner = game.players[1]
    prop = Property("Mortgage Avenue", 1, 200, 20)
    prop.owner = owner

    mortgaged = game.mortgage_property(player, prop)

    assert mortgaged is False
    assert prop.is_mortgaged is False


def test_mortgage_property_fails_when_already_mortgaged():
    """Already mortgaged properties should not be mortgaged again."""
    game = Game(["Alice", "Bob"])
    player = game.players[0]
    prop = Property("Mortgage Avenue", 1, 200, 20)
    prop.owner = player
    player.add_property(prop)
    prop.is_mortgaged = True

    mortgaged = game.mortgage_property(player, prop)

    assert mortgaged is False


def test_trade_fails_when_seller_does_not_own_property():
    """Trades should fail if the seller does not own the offered property."""
    game = Game(["Alice", "Bob"])
    seller = game.players[0]
    buyer = game.players[1]
    prop = Property("Trade Avenue", 1, 100, 10)

    traded = game.trade(seller, buyer, prop, 100)

    assert traded is False
    assert prop.owner is None


def test_trade_fails_when_buyer_cannot_afford_cash_amount():
    """Trades should fail if the buyer lacks the required cash."""
    game = Game(["Alice", "Bob"])
    seller = game.players[0]
    buyer = game.players[1]
    prop = Property("Trade Avenue", 1, 100, 10)
    prop.owner = seller
    seller.add_property(prop)
    buyer.balance = 50

    traded = game.trade(seller, buyer, prop, 100)

    assert traded is False
    assert prop.owner is seller
