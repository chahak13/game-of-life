import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors


def read_pattern(filename):
    root, ext = os.path.splitext(filename)
    if ext == ".txt":
        return _read_txt(filename)
    elif ext == ".lif" or ext == ".life":
        return _read_lif(filename)
    else:
        raise Exception(
            "File type provided as input is not supported. Please provide a .txt or .lif/.life file"
        )


def _read_txt(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
    description = []
    positions = []
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if c == "1" or char == "*":
                positions.append((j, i))
    return positions, description


def _read_lif(filename):
    with open(filename, "r") as f:
        lines = f.readlines()

    description = []
    positions = []
    origin = [0, 0]
    y = 0

    for line in lines:
        if line[0] == "#":
            if line.startswith("#Life"):
                continue
            elif line[1] == "D":
                if len(description) <= 22:
                    description.append(line[2:].strip())
                else:
                    raise Exception(
                        "LIF/LIFE file should not have more than 22 #D lines. Please refer https://www.conwaylife.com/wiki/Life_1.05 for more information about the format"
                    )
            elif line[1] == "R":
                raise Exception(
                    "Rules in LIF not supported in this version. The game runs on the standard rules for now."
                )
            elif line[1] == "P":
                point_coords = [int(x) for x in line[2:].strip().split()]
                origin = point_coords
                y = 0
            else:
                continue
        else:
            if len(line) > 0:
                for x, c in enumerate(line):
                    if c == "1" or c == "*":
                        positions.append((x + origin[0], y + origin[1]))
                y += 1

    description = "\n".join(description)
    return positions, description


def plot_points(
    pattern, result, title="Game of Life", output_image_name="outputs/output.png"
):
    x_max_pat = max([x for x, y in pattern])
    y_max_pat = max([y for x, y in pattern])
    x_max_res = max([x for x, y in result])
    y_max_res = max([y for x, y in result])

    x_min_pat = min([x for x, y in pattern])
    y_min_pat = min([y for x, y in pattern])
    x_min_res = min([x for x, y in result])
    y_min_res = min([y for x, y in result])

    cmap_res = np.zeros((y_max_res - y_min_res + 3, x_max_res - x_min_res + 3))
    cmap_pat = np.zeros((y_max_pat - y_min_pat + 3, x_max_pat - x_min_pat + 3))
    for x, y in pattern:
        cmap_pat[y - y_min_pat + 1, x - x_min_pat + 1] = 1

    for x, y in result:
        cmap_res[y - y_min_res + 1, x - x_min_res + 1] = 1

    cmap = plt.get_cmap('viridis')
    bounds=[0, 0.5, 1]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    fig, ax = plt.subplots(1, 2)
    ax[0].imshow(cmap_pat, cmap=cmap, norm=norm)
    ax[0].set_title("Original")
    ax[0].xaxis.set_visible(False)
    ax[0].yaxis.set_visible(False)
    ax[1].imshow(cmap_res, cmap=cmap, norm=norm)
    ax[1].set_title(title)
    ax[1].xaxis.set_visible(False)
    ax[1].yaxis.set_visible(False)
    plt.savefig(output_image_name, dpi=450, bbox_inches="tight")
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
        return f"Node: level-{self.level} ({1<<self.level}x{1<<self.level}), population: ({self.n})"

    def __repr__(self):
        return f"Node: level-{self.level} ({1<<self.level}x{1<<self.level}), population: ({self.n})"


_DEAD = Node(level=0, n=0, hashvalue=0)
_ALIVE = Node(level=0, n=1, hashvalue=1)


def get_dead():
    return _DEAD


def get_alive():
    return _ALIVE
