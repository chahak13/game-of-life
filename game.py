import numpy as np
from pprint import pprint


def count_neighbours(matrix, i, j):
    count = 0
    n = matrix.shape[1]

    neighbour_perimeter_min = -1
    neighbout_perimeter_max = 2
    for row_mod in range(neighbour_perimeter_min, neighbout_perimeter_max):
        for col_mod in range(neighbour_perimeter_min, neighbout_perimeter_max):
            row = i + row_mod
            col = j + col_mod

            if row < 0 or row >= n:
                continue
            elif col < 0 or col >= n:
                continue
            elif row == i and col == j:
                continue
            else:
                count += matrix[row, col]

    return count


def game(matrix):
    from copy import deepcopy
    new_matrix = deepcopy(matrix)
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            neighbours = count_neighbours(matrix, i, j)
            if matrix[i, j]==1 and (neighbours == 2 or neighbours == 3):
                new_matrix[i, j] = 1
            elif matrix[i, j]==0 and neighbours==3:
                new_matrix[i, j] = 1
            else:
                new_matrix[i, j] = 0
    del matrix
    return new_matrix


runs = 3
matrix = np.array([[0,1,0], [0,1,0], [0,1,0]])
pprint(matrix)
for i in range(runs):
    matrix = game(matrix)
    pprint(matrix)
