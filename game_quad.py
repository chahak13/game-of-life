from collections import Counter
from functools import lru_cache
from plotter import plot_points
import matplotlib.pyplot as plt


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


DEAD = Node(level=0, n=0, hashvalue=0)
ALIVE = Node(level=0, n=1, hashvalue=1)


@lru_cache()
def combine(nw, ne, sw, se):
    level = nw.level + 1
    n = nw.n + ne.n + sw.n + se.n
    hashvalue = level + n + (1 << level)
    return Node(level=level, nw=nw, ne=ne, sw=sw, se=se, n=n, hashvalue=hashvalue)


@lru_cache()
def zeros(level):
    if level == 0:
        return DEAD
    else:
        return combine(
            zeros(level - 1), zeros(level - 1), zeros(level - 1), zeros(level - 1)
        )


def center(node):
    """
    Center the node by adding zero padding to the boudaries.
    """
    z = zeros(node.nw.level)
    result = combine(
        nw=combine(z, z, z, node.nw),
        ne=combine(z, z, node.ne, z),
        sw=combine(z, node.sw, z, z),
        se=combine(node.se, z, z, z),
    )
    return result


def base_life(cell, neighbour_list):
    """ neighbour_list = [nw, n, ne, w, e, sw, s, se] """
    neighbours = sum([c.n for c in neighbour_list])
    if cell is not None:
        new_cell = ALIVE if neighbours == 3 or (cell.n and neighbours == 2) else DEAD
    else:
        new_cell = ALIVE if neighbours == 3 else DEAD
    return new_cell


def life_level_2(node):
    nw = base_life(
        node.nw.se,
        [
            node.nw.nw,
            node.nw.ne,
            node.ne.nw,
            node.nw.sw,
            node.ne.sw,
            node.sw.nw,
            node.sw.ne,
            node.se.nw,
        ],
    )
    ne = base_life(
        node.ne.sw,
        [
            node.nw.ne,
            node.ne.nw,
            node.ne.ne,
            node.nw.se,
            node.ne.se,
            node.sw.ne,
            node.se.nw,
            node.se.ne,
        ],
    )
    sw = base_life(
        node.sw.ne,
        [
            node.nw.sw,
            node.nw.se,
            node.ne.sw,
            node.sw.nw,
            node.se.nw,
            node.sw.sw,
            node.sw.se,
            node.se.sw,
        ],
    )
    se = base_life(
        node.se.nw,
        [
            node.nw.se,
            node.ne.sw,
            node.ne.se,
            node.sw.ne,
            node.se.ne,
            node.sw.se,
            node.se.sw,
            node.se.se,
        ],
    )
    return combine(nw, ne, sw, se)


@lru_cache()
def calculate_generation(node, step=None):
    step = node.level - 2 if step is None else min(step, node.level - 2)
    if node.n == 0:
        return node.nw
    elif node.level == 2:
        return life_level_2(node)
    else:
        m1 = calculate_generation(
            combine(node.nw.nw, node.nw.ne, node.nw.sw, node.nw.se), step
        )
        m2 = calculate_generation(
            combine(node.nw.ne, node.ne.nw, node.nw.se, node.ne.sw), step
        )
        m3 = calculate_generation(
            combine(node.ne.nw, node.ne.ne, node.ne.sw, node.ne.se), step
        )
        m4 = calculate_generation(
            combine(node.nw.sw, node.nw.se, node.sw.nw, node.sw.ne), step
        )
        m5 = calculate_generation(
            combine(node.nw.se, node.ne.sw, node.sw.ne, node.se.nw), step
        )
        m6 = calculate_generation(
            combine(node.ne.sw, node.ne.se, node.se.nw, node.se.ne), step
        )
        m7 = calculate_generation(
            combine(node.sw.nw, node.sw.ne, node.sw.sw, node.sw.se), step
        )
        m8 = calculate_generation(
            combine(node.sw.ne, node.se.nw, node.sw.se, node.se.sw), step
        )
        m9 = calculate_generation(
            combine(node.se.nw, node.se.ne, node.se.sw, node.se.se), step
        )

        if step < node.level - 2:
            result = combine(
                combine(m1.se, m2.sw, m4.ne, m5.nw),
                combine(m2.se, m3.sw, m5.ne, m6.nw),
                combine(m4.se, m5.sw, m7.ne, m8.nw),
                combine(m5.se, m6.sw, m8.ne, m9.nw),
            )
        else:
            result = combine(
                calculate_generation(combine(m1, m2, m4, m5), step),
                calculate_generation(combine(m2, m3, m5, m6), step),
                calculate_generation(combine(m4, m5, m7, m8), step),
                calculate_generation(combine(m5, m6, m8, m9), step),
            )
        return result


def tree_to_list(node, x=0, y=0, level=0):
    if node.n == 0:  # quick zero check
        return []

    size = 1 << node.level

    if node.level == level:
        return [(x >> level, y >> level)]

    else:
        # return all points contained inside this node
        offset = size >> 1
        result_list = (
            tree_to_list(node.nw, x, y, level)
            + tree_to_list(node.ne, x + offset, y, level)
            + tree_to_list(node.sw, x, y + offset, level)
            + tree_to_list(node.se, x + offset, y + offset, level)
        )
        return result_list


def list_to_tree(pts):
    """
    Turn a list of (x,y) coordinates into a quadtree
    and return the top-level Node.
    """
    min_x = min([x for x, y in pts])
    # min_x=0
    min_y = min([y for x, y in pts])
    # min_y=0
    pattern = {(x - min_x, y - min_y): ALIVE for x, y in pts}
    level = 0
    while len(pattern) != 1:
        # bottom-up construction
        next_level = {}
        z = zeros(level)
        while len(pattern) > 0:
            x, y = next(iter(pattern))
            x, y = x - (x & 1), y - (y & 1)
            # read all 2x2 neighbours, removing from those to work through
            # at least one of these must exist by definition
            a = pattern.pop((x, y), z)
            b = pattern.pop((x + 1, y), z)
            c = pattern.pop((x, y + 1), z)
            d = pattern.pop((x + 1, y + 1), z)
            next_level[x >> 1, y >> 1] = combine(a, b, c, d)
        # merge at the next level
        pattern = next_level
        level += 1
    return pad(pattern.popitem()[1])


def is_padded(node):
    """
    If the node has a padding around it, then the population of the vertices
    of the center node will be the same as the population of each node of the
    quad tree.
    """
    return (
        node.nw.n == node.nw.se.n
        and node.ne.n == node.ne.sw.n
        and node.sw.n == node.sw.ne.n
        and node.se.n == node.se.nw.n
    )


def pad(node):
    """
    If node is smaller than a 2nd level (4x4) node, and is not a padded node
    such that the pattern is in the center, then center the node and apply
    padding around the node.
    """
    if node.level <= 3 or not is_padded(node):
        return pad(center(node))
    else:
        return node


def play_game(node, iterations=1):
    """
    Play the game of life for `iterations`. This calculates the game state
    after the given number of iterations.
    """
    if iterations == 0:
        return node

    bits = []
    while iterations > 0:
        bits.append(iterations & 1)
        iterations = iterations >> 1
        node = center(node)

    for i, bit in enumerate(reversed(bits)):
        steps = len(bits) - i - 1
        if bit:
            node = calculate_generation(node, steps)
    return clip(node)


def get_center(node):
    """
    Get the center node of a padded node.
    """
    return combine(node.nw.se, node.ne.sw, node.sw.ne, node.se.nw)


def clip(node):
    """
    Repeatedly take the inner node, until all padding is removed.
    """
    if node.level <= 3 or not is_padded(node):
        return node
    else:
        return clip(get_center(node))


def read_pattern(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
    positions = []
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == "1":
                positions.append((j, i))
    return positions


if __name__ == "__main__":
    # matrix = [[0,1,0], [0,1,0], [0,1,0]]
    points = read_pattern("patterns/test4.txt")
    tree = list_to_tree(points)
    result = play_game(tree, 1)
    ax1 = plot_points(points)
    ax1.set_title("original points")
    ax2 = plot_points(baseline_life(points).keys())
    ax2.set_title("baseline")
    ax3 = plot_points(tree_to_list(result))
    ax3.set_title("quad")
    plt.show()
