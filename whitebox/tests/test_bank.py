"""White-box tests for bank behavior."""

import pytest

from moneypoly.bank import Bank
from moneypoly.player import Player


def test_give_loan_reduces_bank_funds():
    """Issuing a loan should debit the bank by the same amount."""
    bank = Bank()
    player = Player("Alice")
    starting_funds = bank.get_balance()

    bank.give_loan(player, 100)

    assert bank.get_balance() == starting_funds - 100


def test_give_loan_raises_when_bank_lacks_funds():
    """Loans larger than the bank reserve should fail without side effects."""
    bank = Bank()
    player = Player("Alice", balance=0)
    bank._funds = 50  # pylint: disable=protected-access

    with pytest.raises(ValueError, match="Bank cannot pay \\$100"):
        bank.give_loan(player, 100)

    assert player.balance == 0
    assert bank.get_balance() == 50
    assert bank.loan_count() == 0
