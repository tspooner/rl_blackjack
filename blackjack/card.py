from enum import Enum

Suit = Enum('Suit', [
    ('clubs', 1),
    ('hearts', 2),
    ('spades', 3),
    ('diamonds', 4)
])

# TODO: Consider using a custom Enum object to allow for soft and hard ranks.
Rank = Enum('Rank', [
    ('a', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5),
    ('6', 6), ('7', 7), ('8', 8), ('9', 9), ('10', 10),
    ('j', 11), ('q', 12), ('k', 13)
])

class Card(object):
    def __init__(self, suit, rank):
        if isinstance(suit, Suit): self.suit = suit
        elif isinstance(suit, str): self.suit = Suit[suit]
        else: self.suit = Suit(suit)

        if isinstance(rank, Rank): self.rank = rank
        elif isinstance(rank, Rank): self.rank = Rank[rank]
        else: self.rank = Rank(rank)

    def _as_tuple(self):
        return (self.rank.value, self.suit.value)

    def __str__(self):
        return '%s of %s' % (self.rank.name.capitalize(),
                             self.suit.name.capitalize())

    def __int__(self):
        return min(self.rank.value, 10)

    def __lt__(self, other):
        return self._as_tuple() < other._as_tuple()

    def __eq__(self, other):
        return self._as_tuple() == other._as_tuple()

    def __hash__(self):
        return hash(self._as_tuple())
