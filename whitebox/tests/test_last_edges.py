"""Final white-box edge cases to round out branch coverage."""

from moneypoly.board import Board
from moneypoly.game import Game


def test_board_is_not_purchasable_for_mortgaged_property():
    """Mortgaged properties should not be treated as purchasable."""
    board = Board()
    prop = board.get_property_at(1)
    prop.is_mortgaged = True

    assert board.is_purchasable(1) is False


def test_apply_move_to_card_on_blank_tile_does_not_call_property_handler(monkeypatch):
    """Move-to cards landing on non-property tiles should skip property handling."""
    game = Game(["Alice", "Bob"])
    player = game.players[0]
    calls = []

    monkeypatch.setattr(game, "_handle_property_tile", lambda *_args: calls.append("called"))

    game._apply_card(player, {"description": "Move", "action": "move_to", "value": 12})

    assert player.position == 12
    assert calls == []
