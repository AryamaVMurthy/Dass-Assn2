"""Additional white-box tests for CardDeck helper behavior."""

from moneypoly.cards import CardDeck


def test_draw_cycles_back_to_start_after_exhaustion():
    """Drawing past the end of the deck should cycle back to the first card."""
    deck = CardDeck([{"id": 1}, {"id": 2}])

    assert deck.draw() == {"id": 1}
    assert deck.draw() == {"id": 2}
    assert deck.draw() == {"id": 1}


def test_peek_does_not_advance_draw_index():
    """Peeking should not consume the next card."""
    deck = CardDeck([{"id": 1}, {"id": 2}])

    assert deck.peek() == {"id": 1}
    assert deck.draw() == {"id": 1}


def test_reshuffle_resets_index(monkeypatch):
    """Reshuffling should reset the draw position back to the start."""
    deck = CardDeck([{"id": 1}, {"id": 2}])
    deck.draw()
    monkeypatch.setattr("moneypoly.cards.random.shuffle", lambda cards: None)

    deck.reshuffle()

    assert deck.index == 0


def test_len_returns_number_of_cards():
    """The deck length should equal the number of stored cards."""
    deck = CardDeck([{"id": 1}, {"id": 2}, {"id": 3}])

    assert len(deck) == 3
