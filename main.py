from blackjack.player import Dealer, Agent
from blackjack.game import Blackjack
from blackjack.deck import Deck

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import sys

if __name__ == '__main__':
    d = Dealer(Blackjack.Hand())
    p = Agent(Blackjack.Hand(), Blackjack.GOAL+10)
    g = Blackjack(deck=Deck(), dealer=d, players=[p])

    i = 1
    for _ in range(100000):
        sys.stdout.write("\x1b[2K")
        g.play()
        sys.stdout.write(str(i) + '\r')
        sys.stdout.flush()

        d.clear(); p.clear()
        i += 1

    with np.errstate(invalid='ignore'):
        values = np.nan_to_num(p.returns / p.visits)

    X, Y = np.meshgrid(range(1,11), range(12,22))

    fig = plt.figure()

    ax = fig.add_subplot(211, projection='3d')
    ax.plot_wireframe(X, Y, values[:, :, 0])
    ax.set_title('No usable ace')

    ax = fig.add_subplot(212, projection='3d')
    ax.plot_wireframe(X, Y, values[:, :, 1])
    ax.set_title('Usable ace')

    plt.show()
