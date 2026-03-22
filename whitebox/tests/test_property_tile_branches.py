"""White-box tests covering property-tile decision branches."""

from moneypoly.game import Game
from moneypoly.property import Property


def test_handle_property_tile_buy_branch(monkeypatch):
    """Choosing 'b' should call the property purchase path."""
    game = Game(["Alice", "Bob"])
    player = game.players[0]
    prop = Property("Buy Avenue", 1, 100, 10)
    calls = []

    monkeypatch.setattr("builtins.input", lambda _prompt: "b")
    monkeypatch.setattr(game, "buy_property", lambda target_player, target_prop: calls.append((target_player, target_prop)))

    game._handle_property_tile(player, prop)

    assert calls == [(player, prop)]


def test_handle_property_tile_skip_branch(monkeypatch, capsys):
    """Any non-buy and non-auction choice should skip the property."""
    game = Game(["Alice", "Bob"])
    player = game.players[0]
    prop = Property("Skip Avenue", 1, 100, 10)

    monkeypatch.setattr("builtins.input", lambda _prompt: "s")

    game._handle_property_tile(player, prop)

    assert f"{player.name} passes on {prop.name}" in capsys.readouterr().out


def test_handle_property_tile_self_owned_branch(capsys):
    """Landing on your own property should not trigger rent."""
    game = Game(["Alice", "Bob"])
    player = game.players[0]
    prop = Property("Home Avenue", 1, 100, 10)
    prop.owner = player
    player.add_property(prop)

    game._handle_property_tile(player, prop)

    assert "No rent due" in capsys.readouterr().out


def test_handle_property_tile_opponent_owned_branch(monkeypatch):
    """Landing on another player's property should call pay_rent."""
    game = Game(["Alice", "Bob"])
    tenant = game.players[0]
    owner = game.players[1]
    prop = Property("Rent Avenue", 1, 100, 10)
    prop.owner = owner
    owner.add_property(prop)
    calls = []

    monkeypatch.setattr(game, "pay_rent", lambda target_player, target_prop: calls.append((target_player, target_prop)))

    game._handle_property_tile(tenant, prop)

    assert calls == [(tenant, prop)]
