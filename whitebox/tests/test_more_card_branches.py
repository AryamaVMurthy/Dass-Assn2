"""Additional white-box tests for remaining card-action branches."""

from moneypoly.config import GO_SALARY
from moneypoly.game import Game


def test_apply_card_none_does_nothing():
    """A missing card should be ignored safely."""
    game = Game(["Alice", "Bob"])
    player = game.players[0]
    starting_balance = player.balance

    game._apply_card(player, None)

    assert player.balance == starting_balance


def test_apply_pay_card_deducts_money_and_credits_bank():
    """Pay cards should reduce player balance and increase bank funds."""
    game = Game(["Alice", "Bob"])
    player = game.players[0]
    starting_balance = player.balance
    starting_bank = game.bank.get_balance()

    game._apply_card(player, {"description": "Pay", "action": "pay", "value": 40})

    assert player.balance == starting_balance - 40
    assert game.bank.get_balance() == starting_bank + 40


def test_apply_jail_card_sends_player_to_jail():
    """Jail cards should set the player to the jailed state."""
    game = Game(["Alice", "Bob"])
    player = game.players[0]

    game._apply_card(player, {"description": "Jail", "action": "jail", "value": 0})

    assert player.in_jail is True
    assert player.position == 10


def test_apply_collect_from_all_card_collects_only_from_eligible_players():
    """Collect-from-all should skip players who cannot afford the transfer."""
    game = Game(["Alice", "Bob", "Cara"])
    player = game.players[0]
    other_one = game.players[1]
    other_two = game.players[2]
    other_two.balance = 5
    starting_balance = player.balance

    game._apply_card(
        player, {"description": "Collect from all", "action": "collect_from_all", "value": 10}
    )

    assert player.balance == starting_balance + 10
    assert other_one.balance == 1490
    assert other_two.balance == 5


def test_apply_move_to_card_collects_go_salary_when_wrapping():
    """Move-to cards should award Go salary when they wrap around the board."""
    game = Game(["Alice", "Bob"])
    player = game.players[0]
    player.position = 39
    starting_balance = player.balance

    game._apply_card(player, {"description": "Advance to Go", "action": "move_to", "value": 0})

    assert player.position == 0
    assert player.balance == starting_balance + GO_SALARY
