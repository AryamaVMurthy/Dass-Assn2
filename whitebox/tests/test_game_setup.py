"""White-box tests for MoneyPoly game setup validation."""

import pytest

from moneypoly.game import Game


@pytest.mark.parametrize("player_names", [[], ["Solo"]])
def test_game_requires_at_least_two_players(player_names):
    """Game setup should reject sessions with fewer than two players."""
    with pytest.raises(ValueError):
        Game(player_names)
