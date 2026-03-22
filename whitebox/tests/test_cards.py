"""White-box tests for card deck edge cases."""

from moneypoly.cards import CardDeck


def test_empty_deck_reports_zero_remaining_and_safe_repr():
    """Empty decks should not crash when queried for status information."""
    deck = CardDeck([])

    assert deck.cards_remaining() == 0
    assert repr(deck) == "CardDeck(0 cards, next=empty)"
