from src import quadlife
from src.utils import plot_points

import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--filename",
    required=True,
    help="Filename that contains the pattern where 1 marks an alive cell",
)
parser.add_argument(
    "--iterations",
    type=int,
    required=True,
    help="Number of iterations to run for the game"
)
args = vars(parser.parse_args())

if __name__ == "__main__":
    result = quadlife.play(args["filename"], args["iterations"])
    output_image_name = f"./outputs/{args['filename'].rsplit('/')[-1].split('.')[0]}_output_{args['iterations']}_iterations.png"
    ax = plot_points(result, title=f"Life status after {args['iterations']} iterations", output_image_name=output_image_name)
