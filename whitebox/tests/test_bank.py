"""White-box tests for bank behavior."""

from moneypoly.bank import Bank
from moneypoly.player import Player


def test_give_loan_reduces_bank_funds():
    """Issuing a loan should debit the bank by the same amount."""
    bank = Bank()
    player = Player("Alice")
    starting_funds = bank.get_balance()

    bank.give_loan(player, 100)

    assert bank.get_balance() == starting_funds - 100
