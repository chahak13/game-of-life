import numpy as np
import matplotlib.pyplot as plt


def read_pattern(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
    positions = []
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == "1":
                positions.append((j, i))
    return positions


def plot_points(points):
    x_max = max([x for x, y in points]) + 5
    y_max = max([y for x, y in points]) + 5

    cmap = np.zeros((y_max, x_max))
    for x, y in points:
        cmap[y][x] = 1

    fig, ax = plt.subplots()
    ax.imshow(cmap)
    return ax


class Node:
    def __init__(
        self, level=0, nw=None, ne=None, sw=None, se=None, n=0, hashvalue=None
    ):
        self.level = level
        self.nw, self.ne, self.sw, self.se = nw, ne, sw, se
        self.n = n
        self.hash = hashvalue

    def __hash__(self):
        return self.hash

    def __str__(self):
        return f"Node: level-{self.level} ({1<<self.level}x{1<<self.level}), population: {self.n}"

    def __repr__(self):
        return f"Node: level-{self.level} ({1<<self.level}x{1<<self.level}), population: {self.n}"

_DEAD = Node(level=0, n=0, hashvalue=0)
_ALIVE = Node(level=0, n=1, hashvalue=1)

def get_dead():
    return _DEAD

def get_alive():
    return _ALIVE
