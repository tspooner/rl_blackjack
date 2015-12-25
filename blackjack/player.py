from enum import Enum
import numpy as np
import random

class Action(Enum):
    stand = 0
    hit = 1

class Player(object):
    def __init__(self, hand, name):
        self.name = name
        self.hand = hand

    def draw(self, n_cards, deck):
        cards = deck.draw(n_cards)
        self.hand.add_cards(cards)

    def clear(self):
        self.hand.clear()

    def get_action(self, upcard):
        raise NotImplementedError("Please implement this method {Player.get_action}")

    def response(self, result):
        raise NotImplementedError("Please implement this method {Player.response}")

    def __str__(self): return str(self.name)

class Dealer(Player):
    def __init__(self, hand, name='Dealer'):
        super().__init__(hand, name=name)

    def upcard(self):
        return self.hand[0]

    def get_action(self, upcard):
        if self.hand.value() < 17: return Action.hit
        else: return Action.stand

    def response(self, result): pass

###################
# Learning players:

class MonteCarloLearner(Player):
    def __init__(self, hand, n_states, name='Learner'):
        super().__init__(hand, name)

        self.states_seen = []

        self.visits = np.zeros((10, 10, 2))
        self.returns = np.zeros((10, 10, 2))

    def clear(self):
        super().clear()

        self.states_seen = []

    def value(self, state):
        return self.returns[state] / self.visits[state]

    def learn(self, reward):
        for s in self.states_seen:
            self.visits[s] += 1
            self.returns[s] += reward

class Agent(MonteCarloLearner):
    def __init__(self, hand, n_states, name='Learner'):
        super().__init__(hand, n_states, name=name)

    def get_action(self, upcard):
        h_val = self.hand.value()
        if h_val > 11 and h_val <= 21:
            state = (h_val-12, int(upcard)-1, int(self.hand.usable_ace))
            self.states_seen.append(state)

        if h_val < 20: return Action.hit
        else: return Action.stand

    def response(self, result):
        self.learn(result)
