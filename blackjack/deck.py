from blackjack.card import Suit, Rank, Card
from itertools import product
from random import sample

class Deck(object):
    def __init__(self):
        self.cards = set(Card(s, r) for (s, r) in product(Suit, Rank))

    def draw(self, n=1):
        return sample(self.cards, n)

    def __iter__(self): return self

    def next(self):
        return self.draw()[0]

class StandardDeck(Deck):
    def __init__(self): self.reset()

    def reset(self):
        super().__init__()
        self.drawn = set()

    def draw(self, n=1):
        try:
            draw = sample(self.cards ^ self.drawn, n)
        except ValueError:
            if len(self.drawn) < 52:
                draw = self.remaining()
            else:
                raise StopIteration("No more cards in the deck!")

        self.drawn.update(draw)
        return draw

    def remaining(self):
        return list(self.cards)
