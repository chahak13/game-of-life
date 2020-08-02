from src import quadlife
from src.utils import plot_points

import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--filename",
    default="patterns/test3.txt",
    help="Filename that contains the pattern where 1 marks an alive cell",
)
parser.add_argument(
    "--iterations",
    default=1,
    type=int,
    help="Number of iterations to run for the game"
)
args = vars(parser.parse_args())

if __name__ == "__main__":
    result = quadlife.play(args["filename"], args["iterations"])
    ax = plot_points(result, title=f"Life status after {args['iterations']} iterations")
