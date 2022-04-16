# utils.py

import matplotlib.pyplot as plt


def plot_walls(walls: {((int, int), (int, int))}, fmt: str):
    for pos1, pos2 in walls:
        x1, y1 = pos1
        x2, y2 = pos2
        assert (x1 == x2) ^ (y1 == y2)  # use XOR because only one of the pairs should be equal
        if x1 == x2:
            plt.plot([x1 - 0.5, x1 + 0.5], [(y1 + y2) / 2, (y1 + y2) / 2], fmt)
        elif y1 == y2:
            plt.plot([(x1 + x2) / 2, (x1 + x2) / 2], [y1 - 0.5, y1 + 0.5], fmt)
