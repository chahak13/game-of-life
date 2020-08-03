# Game of Life
----

This is a Python implementation of [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) using the Hashlife algorithm. The idea of the algorithm is to store subpatterns in a hash table so that the results of their evolution don't have to be recomputed if they arise again at another place or time. This implementation calculates the required number of generations by taking steps of sizes that are a power of two. These steps are taken in such a way, that
the sum of the steps is equal to the required number of generations. For example, if the user wants to calculate the 29th generation of a given pattern, the algorithm takes steps of sizes 16, 8, 4 and 1 during each calculation. This runs closely with how in the algorithm 2^N × 2^N tiles are run 2^N-2 ticks into the future and then reuses them without re-calculating, by the means of caching. This provides an efficient way to jump to the required number of iterations but has one drawback of not
being able to store every generation in particular.

## Usage

There are two ways in which one can use this program:

### 1. Docker

If the user has Docker installed on their system, they can use docker to build an image and run their simulations on the image. The steps for the same are as follows:

1. Create the docker image:
 ```
 docker build -t life .
 ```
2. Run the docker image using a custom pattern file:
```
docker run --name life-cont -v </path/to/pattern/file>:/life/patterns/<filename> -it life:latest /bin/bash -c 'python runner.py --filename <filename> --iterations <iterations> && tree outputs'
```
3. Copy the output from the docker container to local filesystem:
```
docker cp life-cont:/life/outputs/<output image name>
```

### 2. Local Setup

1. Create a Python virtual environment using `python -m venv env` and activate the environment using `source env/bin/activate`.
2. Install the dependencies via `pip install -r requirements.txt`
3. Create a pattern file using either simple textfile or the .lif [Life 1.05 file format](https://www.conwaylife.com/wiki/Life_1.05)
4. Run the code using `python runner.py --filename <path/to/pattern/file> --iterations <iterations>`
5. The output will be stored in the `outputs/` folder with the name `<pattern file name>_output_<iterations>_iterations.png`

## Pattern Files

There are two pattern file formats supported currently:

### 1. Standard text file

A standard text file that contains the pattern in it. For example, the content of `pattern.txt` should be:
```
--1----
----1--
-11-111
-------
```

### 2. Life 1.05 File format

There is also an experimental support of the [Life 1.05 File Format](https://www.conwaylife.com/wiki/Life_1.05) which is used to create large patterns. The parser follows strict rules of the format as described in the wiki and doesn't support custom rules as of now. An example file of this format is:

```
#Life 1.05
#D Description line 1
#D Description line 2
#P -3 -1
.*.
...*.
**..***.
```

For more details of this format, please check the [wiki](https://www.conwaylife.com/wiki/Life_1.05)
