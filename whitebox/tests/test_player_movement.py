"""White-box tests for player movement behavior."""

from moneypoly.config import GO_SALARY
from moneypoly.player import Player


def test_move_awards_go_salary_when_passing_go():
    """Players should collect the Go salary when wrapping around the board."""
    player = Player("Alice")
    player.position = 39
    starting_balance = player.balance

    new_position = player.move(2)

    assert new_position == 1
    assert player.balance == starting_balance + GO_SALARY
