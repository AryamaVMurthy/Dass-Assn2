"""White-box tests for rent payment behavior."""

from moneypoly.game import Game
from moneypoly.property import Property


def test_pay_rent_transfers_money_to_property_owner():
    """Rent should be deducted from the tenant and credited to the owner."""
    game = Game(["Alice", "Bob"])
    tenant = game.players[0]
    owner = game.players[1]
    prop = Property("Test Avenue", 1, 100, 25)
    prop.owner = owner
    owner.add_property(prop)

    tenant_start = tenant.balance
    owner_start = owner.balance

    game.pay_rent(tenant, prop)

    assert tenant.balance == tenant_start - 25
    assert owner.balance == owner_start + 25
