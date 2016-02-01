from blackjack.policy import FixedPolicy, AdaptivePolicy
from blackjack.utilities import to_state
import numpy as np
import random

class Player(object):
    def __init__(self, policy, hand, name):
        self.name = name
        self.hand = hand
        self.policy = policy

    def draw(self, n_cards, deck):
        cards = deck.draw(n_cards)
        self.hand.add_cards(cards)

    def clear(self):
        self.hand.clear()

    def get_action(self, upcard):
        return self.policy.get_action(self.hand, upcard)

    def response(self, result):
        raise NotImplementedError("Please implement this method {Player.response}")

    def __str__(self): return str(self.name)

class Dealer(Player):
    def __init__(self, hand, policy=FixedPolicy(limit=17), name='Dealer'):
        super().__init__(policy, hand, name=name)

    def upcard(self):
        return self.hand[0]

    def response(self, result): pass

###################
# Learning players:

class MonteCarloLearner(Player):
    def __init__(self, policy, hand, name='Learner'):
        super().__init__(policy, hand, name)

        self.history = []

        # s_0, s_1, s_2, a
        self.visits = np.zeros((10, 10, 2, 2))
        self.returns = np.zeros((10, 10, 2, 2))

    def clear(self):
        super().clear()

        self.history = []

    def value(self, state):
        return self.returns[state] / self.visits[state]

    def learn(self, reward):
        for s,a in self.history:
            ind = s+(a.value,)

            self.visits[ind] += 1
            self.returns[ind] += reward

        if isinstance(self.policy, AdaptivePolicy):
            self.policy.learn(self.Q, self.history)

    @property
    def Q(self):
        with np.errstate(invalid='ignore'):
            return np.nan_to_num(self.returns / self.visits)

class Agent(MonteCarloLearner):
    def __init__(self, policy, hand, name='Learner'):
        super().__init__(policy, hand, name=name)

    def get_action(self, upcard):
        action = super().get_action(upcard)

        h_val = self.hand.value()
        if h_val > 11 and h_val <= 21:
            state = to_state(self.hand, upcard)
            self.history.append((state, action))

        return action

    def response(self, result):
        self.learn(result)
