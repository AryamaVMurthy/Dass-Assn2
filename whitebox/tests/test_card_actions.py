"""White-box tests covering card-action branches."""

from moneypoly.game import Game


def test_apply_collect_card_adds_money_to_player():
    """Collect cards should transfer money from the bank to the player."""
    game = Game(["Alice", "Bob"])
    player = game.players[0]
    starting_balance = player.balance

    game._apply_card(player, {"description": "Collect", "action": "collect", "value": 50})

    assert player.balance == starting_balance + 50


def test_apply_jail_free_card_increments_card_count():
    """Jail-free cards should increment the player's saved card count."""
    game = Game(["Alice", "Bob"])
    player = game.players[0]

    game._apply_card(
        player, {"description": "Get Out of Jail Free", "action": "jail_free", "value": 0}
    )

    assert player.get_out_of_jail_cards == 1


def test_apply_birthday_card_collects_from_other_players():
    """Birthday cards should transfer money from each eligible opponent."""
    game = Game(["Alice", "Bob", "Cara"])
    player = game.players[0]
    other_one = game.players[1]
    other_two = game.players[2]
    other_two.balance = 5
    starting_balance = player.balance

    game._apply_card(player, {"description": "Birthday", "action": "birthday", "value": 10})

    assert player.balance == starting_balance + 10
    assert other_one.balance == 1490
    assert other_two.balance == 5


def test_apply_move_to_card_resolves_property_tile(monkeypatch):
    """Move-to cards should delegate to property handling when landing on a property."""
    game = Game(["Alice", "Bob"])
    player = game.players[0]
    calls = []

    def fake_handle_property_tile(target_player, prop):
        calls.append((target_player, prop.name))

    monkeypatch.setattr(game, "_handle_property_tile", fake_handle_property_tile)
    player.position = 0

    game._apply_card(
        player, {"description": "Advance to Boardwalk", "action": "move_to", "value": 39}
    )

    assert player.position == 39
    assert calls == [(player, "Boardwalk")]
