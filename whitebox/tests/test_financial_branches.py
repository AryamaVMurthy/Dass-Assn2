"""White-box tests covering financial and cleanup branches."""

from moneypoly.game import Game
from moneypoly.property import Property


def test_mortgage_property_credits_player_and_marks_property():
    """Mortgaging should pay the player and mark the property as mortgaged."""
    game = Game(["Alice", "Bob"])
    player = game.players[0]
    prop = Property("Mortgage Avenue", 1, 200, 20)
    prop.owner = player
    player.add_property(prop)
    starting_balance = player.balance

    mortgaged = game.mortgage_property(player, prop)

    assert mortgaged is True
    assert prop.is_mortgaged is True
    assert player.balance == starting_balance + prop.mortgage_value


def test_mortgage_property_uses_bank_payout_without_fake_collection():
    """Mortgage payouts should not reduce the bank's collection totals."""
    game = Game(["Alice", "Bob"])
    player = game.players[0]
    prop = Property("Mortgage Avenue", 1, 200, 20)
    prop.owner = player
    player.add_property(prop)
    starting_funds = game.bank.get_balance()

    mortgaged = game.mortgage_property(player, prop)

    assert mortgaged is True
    assert game.bank.get_balance() == starting_funds - prop.mortgage_value
    assert game.bank._total_collected == 0  # pylint: disable=protected-access


def test_auction_property_with_no_bids_keeps_property_unowned(monkeypatch):
    """If every player passes, the auction should leave the property unowned."""
    game = Game(["Alice", "Bob"])
    prop = Property("Auction Avenue", 1, 100, 10)

    monkeypatch.setattr("moneypoly.game.ui.safe_int_input", lambda _prompt, default=0: 0)

    game.auction_property(prop)

    assert prop.owner is None


def test_check_bankruptcy_removes_player_and_releases_properties():
    """Bankrupt players should be removed and their properties reset."""
    game = Game(["Alice", "Bob"])
    player = game.players[0]
    prop = Property("Bankrupt Avenue", 1, 100, 10)
    prop.owner = player
    prop.is_mortgaged = True
    player.add_property(prop)
    player.balance = 0

    game._check_bankruptcy(player)

    assert player not in game.players
    assert prop.owner is None
    assert prop.is_mortgaged is False
