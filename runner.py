from src import quadlife
from src.utils import plot_points
import matplotlib.pyplot as plt

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--filename', default='patterns/test3.txt', help='Filename that contains the pattern where 1 marks an alive cell')
args = vars(parser.parse_args())

if __name__ == '__main__':
    result = quadlife.play(args['filename'], 1)
    ax3 = plot_points(result)
    ax3.set_title("quad")
    plt.show()
