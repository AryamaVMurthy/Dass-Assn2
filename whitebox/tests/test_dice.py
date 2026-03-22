"""White-box tests for dice behavior in MoneyPoly."""

from moneypoly.dice import Dice


def test_roll_uses_six_sided_dice(monkeypatch):
    """Dice rolls should sample values from 1 to 6 inclusive."""
    calls = []

    def fake_randint(low, high):
        calls.append((low, high))
        return 1

    monkeypatch.setattr("moneypoly.dice.random.randint", fake_randint)

    dice = Dice()
    dice.roll()

    assert calls == [(1, 6), (1, 6)]
