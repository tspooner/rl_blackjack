from blackjack.player import Dealer, Agent
from blackjack.policy import FixedPolicy, EpsSoftPolicy
from blackjack.game import Blackjack
from blackjack.deck import Deck

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

import argparse
import datetime
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run a blackjack simulation.')
    parser.add_argument('n_simulations', metavar='n', type=int, default=1, help='number of iterations')
    parser.add_argument('--verbose', type=bool, default=False, help='print out game results (default: false)')
    args = parser.parse_args()

    d = Dealer(Blackjack.Hand())
    # p = Agent(FixedPolicy(limit=18), Blackjack.Hand())
    p = Agent(EpsSoftPolicy(), Blackjack.Hand())

    g = Blackjack(deck=Deck(), dealer=d, players=[p])

    i = 1
    for _ in range(args.n_simulations):
        sys.stdout.write("\x1b[2K")
        g.play()
        sys.stdout.write(str(i) + '\r')
        sys.stdout.flush()

        d.clear(); p.clear()
        i += 1

    fname_prefix = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    np.save('./results/'+fname_prefix+'__values', p.Q)
    np.save('./results/'+fname_prefix+'__policy', p.policy.pi)

    Q = p.Q
    X, Y = np.meshgrid(range(1,11), range(12,22))

    fig = plt.figure()

    ax = fig.add_subplot(221)
    ax.imshow((p.policy.pi[:, :, 0, 0] > p.policy.pi[:, :, 0, 1]).astype(int))
    ax.set_title('Policy under: No usable ace')

    ax = fig.add_subplot(222, projection='3d')
    ax.plot_wireframe(X, Y, (Q[:, :, 0, 0]+Q[:, :, 0, 1])/2)
    ax.set_title('No usable ace')

    ax = fig.add_subplot(223)
    ax.imshow((p.policy.pi[:, :, 1, 0] > p.policy.pi[:, :, 1, 1]).astype(int))
    ax.set_title('Policy under: Usable ace')

    ax = fig.add_subplot(224, projection='3d')
    ax.plot_wireframe(X, Y, (Q[:, :, 1, 0]+Q[:, :, 1, 1])/2)
    ax.set_title('Usable ace')

    plt.show()
