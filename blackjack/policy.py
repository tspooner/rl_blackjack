from blackjack.utilities import to_state
from enum import Enum
import numpy as np
import random

class Action(Enum):
    stand = 0
    hit = 1

class Policy(object):
    def get_action(self, hand, upcard):
        raise NotImplementedError("Please implement this method {Policy.get_action}")

class FixedPolicy(Policy):
    def __init__(self, limit=20):
        self.limit = limit

    def get_action(self, hand, upcard):
        if hand.value() < self.limit: return Action.hit
        else: return Action.stand

class AdaptivePolicy(Policy):
    def __init__(self):
        self.pi = np.random.random((10, 10, 2, 2))

    def learn(self, Q, history):
        raise NotImplementedError("Please implement this method {AdaptivePolicy.learn}")

    def get_action(self, hand, upcard):
        raise NotImplementedError("Please implement this method {AdaptivePolicy.learn}")

class EpsSoftPolicy(AdaptivePolicy):
    def __init__(self, epsilon=0.30, decay_schedule=None):
        super().__init__()

        self.k = 0
        self.epsilon = epsilon

        if decay_schedule is None:
            self.decay_schedule = lambda x: x*0.9999999
        else:
            self.decay_schedule = decay_schedule

    def get_action(self, hand, upcard):
        state = to_state(hand, upcard)

        if random.random() < self.epsilon:
            return random.choice(list(Action))
        else:
            return Action(np.argmax(self.pi[state]))

    def learn(self, Q, history):
        for s,a in history:
            A = Action(np.argmax(Q[s]))

            for a in Action:
                ind = s+(a.value,)

                if a == A:
                    self.pi[ind] = 1 - self.epsilon + self.epsilon/len(Action)
                else:
                    self.pi[ind] = self.epsilon/len(Action)

        self.k += 1
        self.epsilon = self.decay_schedule(self.epsilon)
