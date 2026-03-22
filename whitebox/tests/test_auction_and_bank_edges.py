"""Additional white-box tests for auction and bank edge behavior."""

import pytest

from moneypoly.bank import Bank
from moneypoly.game import Game
from moneypoly.property import Property


def test_auction_property_awards_property_to_highest_valid_bidder(monkeypatch):
    """The highest valid bidder should win the auction."""
    game = Game(["Alice", "Bob"])
    prop = Property("Auction Avenue", 1, 100, 10)
    bids = iter([50, 80])

    monkeypatch.setattr(
        "moneypoly.game.ui.safe_int_input", lambda _prompt, default=0: next(bids)
    )

    game.auction_property(prop)

    assert prop.owner is game.players[1]


def test_auction_property_rejects_bid_below_minimum_raise(monkeypatch):
    """Bids below the required raise should not replace the current high bid."""
    game = Game(["Alice", "Bob"])
    prop = Property("Auction Avenue", 1, 100, 10)
    bids = iter([50, 55])

    monkeypatch.setattr(
        "moneypoly.game.ui.safe_int_input", lambda _prompt, default=0: next(bids)
    )

    game.auction_property(prop)

    assert prop.owner is game.players[0]


def test_auction_property_rejects_unaffordable_bid(monkeypatch):
    """Players should not be able to win with bids beyond their balance."""
    game = Game(["Alice", "Bob"])
    prop = Property("Auction Avenue", 1, 100, 10)
    game.players[1].balance = 20
    bids = iter([30, 40])

    monkeypatch.setattr(
        "moneypoly.game.ui.safe_int_input", lambda _prompt, default=0: next(bids)
    )

    game.auction_property(prop)

    assert prop.owner is game.players[0]


def test_bank_pay_out_zero_returns_zero():
    """Zero-value payouts should return zero and not change reserves."""
    bank = Bank()
    starting_balance = bank.get_balance()

    assert bank.pay_out(0) == 0
    assert bank.get_balance() == starting_balance


def test_bank_pay_out_raises_when_funds_are_insufficient():
    """Oversized payouts should raise a value error."""
    bank = Bank()

    with pytest.raises(ValueError):
        bank.pay_out(bank.get_balance() + 1)
