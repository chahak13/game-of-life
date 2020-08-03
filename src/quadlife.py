from functools import lru_cache
from .utils import read_pattern, Node, get_dead, get_alive
import time


def play(filename, iterations):
    points, desc = read_pattern(filename)
    root_node = _list_to_tree(points)
    start_t = time.time()
    result = _play_game(root_node, iterations)
    end_t = time.time()
    time_taken = end_t - start_t
    # all_nodes_points = [_tree_to_list(node) for node in all_nodes]
    result_points = _tree_to_list(result)
    return points, result_points, time_taken


def _play_game(node, iterations=0):
    """
    Play the game of life for `iterations`. This calculates the game state
    after the given number of iterations.
    """
    if iterations == 0:
        return node

    iterations_binary = [int(x) for x in bin(iterations)[2:]]
    for _ in range(len(iterations_binary)):
        node = _center_node(node)

    for i, bit in enumerate(iterations_binary):
        if bit:
            steps = len(iterations_binary) - i - 1
            node = _calculate_generations(node, steps)
    return _clip(node)


def _tree_to_list(node, x=0, y=0, level=0):
    if node.n == 0:
        return []

    size = 1 << node.level

    if node.level == level:
        return [(x >> level, y >> level)]

    else:
        offset = size >> 1
        result_list = (
            _tree_to_list(node.nw, x, y, level)
            + _tree_to_list(node.ne, x + offset, y, level)
            + _tree_to_list(node.sw, x, y + offset, level)
            + _tree_to_list(node.se, x + offset, y + offset, level)
        )
        return result_list


def _list_to_tree(points):
    x_min = min([x for x, y in points])
    y_min = min([y for x, y in points])
    pattern = {(x - x_min, y - y_min): get_alive() for x, y in points}
    level = 0
    while len(pattern) != 1:
        next_level = {}
        z = _zero_node(level)
        while len(pattern) > 0:
            x, y = next(iter(pattern))
            x, y = x - (x & 1), y - (y & 1)
            nw = pattern.pop((x, y), z)
            ne = pattern.pop((x + 1, y), z)
            sw = pattern.pop((x, y + 1), z)
            se = pattern.pop((x + 1, y + 1), z)
            next_level[x >> 1, y >> 1] = _combine(nw, ne, sw, se)
        pattern = next_level
        level += 1
    return _pad(pattern.popitem()[1])


@lru_cache()
def _calculate_generations(node, step=None):
    step = node.level - 2 if step is None else min(step, node.level - 2)
    if node.n == 0:
        return node.nw
    elif node.level == 2:
        return _simulate_level_2(node)
    else:
        m1 = _calculate_generations(
            _combine(node.nw.nw, node.nw.ne, node.nw.sw, node.nw.se), step
        )
        m2 = _calculate_generations(
            _combine(node.nw.ne, node.ne.nw, node.nw.se, node.ne.sw), step
        )
        m3 = _calculate_generations(
            _combine(node.ne.nw, node.ne.ne, node.ne.sw, node.ne.se), step
        )
        m4 = _calculate_generations(
            _combine(node.nw.sw, node.nw.se, node.sw.nw, node.sw.ne), step
        )
        m5 = _calculate_generations(
            _combine(node.nw.se, node.ne.sw, node.sw.ne, node.se.nw), step
        )
        m6 = _calculate_generations(
            _combine(node.ne.sw, node.ne.se, node.se.nw, node.se.ne), step
        )
        m7 = _calculate_generations(
            _combine(node.sw.nw, node.sw.ne, node.sw.sw, node.sw.se), step
        )
        m8 = _calculate_generations(
            _combine(node.sw.ne, node.se.nw, node.sw.se, node.se.sw), step
        )
        m9 = _calculate_generations(
            _combine(node.se.nw, node.se.ne, node.se.sw, node.se.se), step
        )

        if step < node.level - 2:
            result = _combine(
                _combine(m1.se, m2.sw, m4.ne, m5.nw),
                _combine(m2.se, m3.sw, m5.ne, m6.nw),
                _combine(m4.se, m5.sw, m7.ne, m8.nw),
                _combine(m5.se, m6.sw, m8.ne, m9.nw),
            )
        else:
            result = _combine(
                _calculate_generations(_combine(m1, m2, m4, m5), step),
                _calculate_generations(_combine(m2, m3, m5, m6), step),
                _calculate_generations(_combine(m4, m5, m7, m8), step),
                _calculate_generations(_combine(m5, m6, m8, m9), step),
            )
        return result


@lru_cache()
def _simulate_level_2(node):
    nw = _update_cell_state(
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
    ne = _update_cell_state(
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
    sw = _update_cell_state(
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
    se = _update_cell_state(
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
    return _combine(nw, ne, sw, se)


def _update_cell_state(cell, neighbour_list):
    """ neighbour_list = [nw, n, ne, w, e, sw, s, se] """
    neighbours = sum([c.n for c in neighbour_list])
    if cell is not None:
        new_cell = (
            get_alive()
            if neighbours == 3 or (cell.n and neighbours == 2)
            else get_dead()
        )
    else:
        new_cell = get_alive() if neighbours == 3 else get_dead()
    return new_cell


@lru_cache()
def _combine(nw, ne, sw, se):
    level = nw.level + 1
    n = nw.n + ne.n + sw.n + se.n
    hashvalue = id(nw) + id(ne) + id(sw) + id(se)
    return Node(level=level, nw=nw, ne=ne, sw=sw, se=se, n=n, hashvalue=hashvalue)


def _zero_node(level):
    if level == 0:
        return get_dead()
    else:
        return _combine(
            _zero_node(level - 1),
            _zero_node(level - 1),
            _zero_node(level - 1),
            _zero_node(level - 1),
        )


def _center_node(node):
    """
    Center the node by adding zero padding to the boudaries.
    """
    z = _zero_node(node.nw.level)
    result = _combine(
        nw=_combine(z, z, z, node.nw),
        ne=_combine(z, z, node.ne, z),
        sw=_combine(z, node.sw, z, z),
        se=_combine(node.se, z, z, z),
    )
    return result


def _get_center_node(node):
    """
    Get the center node of a padded node.
    """
    return _combine(node.nw.se, node.ne.sw, node.sw.ne, node.se.nw)


def _is_padded(node):
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


def _pad(node):
    """
    If node is smaller than a 2nd level (4x4) node, and is not a padded node
    such that the pattern is in the center, then center the node and apply
    padding around the node.
    """
    if node.level <= 3 or not _is_padded(node):
        return _pad(_center_node(node))
    else:
        return node


def _clip(node):
    """
    Repeatedly take the inner node, until all padding is removed.
    """
    if node.level <= 3 or not _is_padded(node):
        return node
    else:
        return _clip(_get_center_node(node))
