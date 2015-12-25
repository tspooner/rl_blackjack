from blackjack.player import Dealer, Agent, Action
from blackjack.deck import StandardDeck
from blackjack.card import Card

import numpy as np

class Hand(object):
    def __init__(self, cards=None):
        self.cards = cards if cards is not None else []

    def clear(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)
    def add_cards(self, cards):
        for c in cards:
            self.add_card(c)

    def remove_card(self, card):
        try:
            self.cards.remove(card)
        except:
            pass

    def remove_cards(self, cards):
        for c in cards:
            self.remove_card(card)

    def __getitem__(self, index):
        return self.cards[index]

    def value(self):
        raise NotImplementedError("Please implement this method")

class Game(object):
    def __init__(self, deck, dealer, players=None, verbose=False):
        self.deck = deck
        self.dealer = dealer
        self.players = players if players is not None else []

        self.verbose = verbose

    def play(self):
        raise NotImplementedError("Please implement this method")

    def set_deck(self, deck): self.deck = deck
    def set_dealer(self, dealer): self.dealer = dealer

    def add_player(self, player): self.players.append(player)
    def remove_player(self, player): self.players.remove(player)
    def clear_players(self): self.players = []

class Blackjack(Game):
    GOAL = 21

    class Hand(Hand):
        def __init__(self, cards=None):
            self.cards = cards if cards is not None else []

            self.ace = False
            self.usable_ace = False

        def add_card(self, card):
            super().add_card(card)

            if int(card) == 1:
                self.ace = True

            if self.ace:
                self.usable_ace = False
                if self.value() <= 11:
                    self.usable_ace = True

        def value(self):
            return self._value(self.cards)

        def last_value(self):
            return self._value(self.cards[0:-1])

        def is_bust(self):
            return self.value() > Blackjack.GOAL

        def _value(self, cards):
            total_val = 0
            for c in cards:
                c_val = int(c)
                total_val += c_val

            if self.usable_ace: total_val += 10

            return total_val


    def __init__(self, deck=None, dealer=None, players=None, verbose=False):
        deck = deck if deck is not None else StandardDeck()
        dealer = dealer if dealer is not None else \
            Dealer(Blackjack.Hand(), self.GOAL+9)

        super().__init__(deck, dealer, players, verbose)

    @staticmethod
    def _get_result(dealer, players):
        w_val = 0
        winners = []
        for p in players:
            p_val = p.hand.value()

            if p.hand.is_bust() or p_val < w_val: continue
            elif p_val == w_val: winners.append(p)
            else: # p_val > w_val
                winners = [p]
                w_val = p_val

        d_val = dealer.hand.value()
        if not dealer.hand.is_bust() and d_val >= w_val:
            w_val = d_val
            winners = [dealer]

        return winners, [p for p in [dealer]+players if p not in winners]

    def _init_hands(self):
        for p in [self.dealer]+self.players:
            if len(p.hand.cards) == 0:
                p.draw(2, self.deck)

    def _play(self, player):
        # Players play
        upcard = self.dealer.upcard()

        a = player.get_action(upcard)
        if a == Action.stand: return

        if a == Action.hit: player.draw(1, self.deck)

        if not player.hand.is_bust():
            self._play(player)
        else:
            return

    def play(self):
        # Initiate game
        self._init_hands()

        # Players play
        for p in self.players:
            self._play(p)
        # Dealer plays
        self._play(self.dealer)

        # Who won/lost
        winners, losers = Blackjack._get_result(self.dealer, self.players)

        # Set responses
        n_winners = len(winners)
        if n_winners == 0:
            for l in losers:
                l.response(-1)

            if self.verbose:
                print('No winners.')
        elif n_winners == 1:
            winners[0].response(1)
            for l in losers: l.response(-1)

            if self.verbose:
                print(str(winners[0]) + ' won with:', winners[0].hand.value(),
                      '->', [str(c) for c in winners[0].hand])
        else:
            for l in losers: l.response(-1)
            for w in winners:
                w.response(0)

                if self.verbose:
                    print(str(w) + ' drew with:', w.hand.value(),
                          '->', [str(c) for c in w.hand])
