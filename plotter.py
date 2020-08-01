import numpy as np
import matplotlib.pyplot as plt


def plot_points(points):
    x_max = max([x for x, y in points]) + 5
    y_max = max([y for x, y in points]) + 5

    cmap = np.zeros((y_max, x_max))
    for x, y in points:
        cmap[y][x] = 1

    fig, ax = plt.subplots()
    ax.imshow(cmap)
    return ax


if __name__ == "__main__":
    points = [(0, 1), (1, 1), (2, 1)]
    plot_points(points)
    plt.show()
