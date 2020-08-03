import os
import numpy as np
import matplotlib.pyplot as plt


def read_pattern(filename):
    root, ext = os.path.splitext(filename)
    if ext == '.txt':
        return _read_txt(filename)
    elif ext == '.lif' or ext == '.life':
        return _read_lif(filename)
    else:
        raise Exception("File type provided as input is not supported. Please provide a .txt or .lif/.life file")

def _read_txt(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
    description = []
    positions = []
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == "1":
                positions.append((j, i))
    return positions, description

def _read_lif(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    description = []
    positions = []
    origin = [0, 0]

    for line in lines:
        if line[0] == '#':
            if line.startswith('#Life'):
                continue
            elif line[1] == 'D':
                if len(description) <= 22:
                    description.append(line[2:].strip())
                else:
                    raise Exception("LIF/LIFE file should not have more than 22 #D lines. Please refer https://www.conwaylife.com/wiki/Life_1.05 for more information about the format")
            elif line[1] == "R":
                raise Exception("Rules in LIF not supported in this version. The game runs on the standard rules for now.")
            elif line[1] == "P":
                point_coords = [int(x) for x in line[2:].strip().split()]
                origin = [-point_coords[0], -point_coords[1]]
                y = origin[1]
            else:
                raise Exception(f"# should be followed by D/R/P. Found: {line}")
        else:
            if len(line) > 0:
                for x, c in enumerate(line):
                    if c == '*':
                        positions.append((x + origin[0], y + origin[1]))
                y += 1

    description = '\n'.join(description)
    return positions, description

def plot_points(pattern, result, title="Game of Life", output_image_name='outputs/output.png'):
    cmap = np.zeros((200,200))
    cmap_original = np.zeros((200,200))
    for x, y in pattern:
        cmap_original[y+cmap_original.shape[0]//2, x+cmap_original.shape[1]//2] = 1

    for x, y in result:
        cmap[y+cmap.shape[0]//2, x+cmap.shape[1]//2] = 1


    # from pprint import pprint
    # pprint(cmap)

    fig, ax = plt.subplots(1, 2)
    ax[0].imshow(cmap_original)
    ax[0].set_title("Original")
    ax[1].imshow(cmap)
    ax[1].set_title(title)
    plt.savefig(output_image_name, dpi=450)
    return ax, output_image_name


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
