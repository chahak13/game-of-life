# Game of Life

This is a Python implementation of [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) using the Hashlife algorithm. The idea of the algorithm is to store subpatterns in a hash table so that the results of their evolution don't have to be recomputed if they arise again at another place or time. This implementation calculates the required number of generations by taking steps of sizes that are a power of two. These steps are taken in such a way, that
the sum of the steps is equal to the required number of generations. For example, if the user wants to calculate the 29th generation of a given pattern, the algorithm takes steps of sizes 16, 8, 4 and 1 during each calculation. This runs closely with how in the algorithm 2^N × 2^N tiles are run 2^N-2 ticks into the future and then reuses them without re-calculating, by the means of caching. This provides an efficient way to jump to the required number of iterations but has one drawback of not
being able to store every generation in particular.

For caching purposes, we can simply use a HashMap of pre-computed nodes using a dictionary, but Python provides a nifty tool in its functools package that can be found in the core packages and can be used for caching - [lru_cache](https://docs.python.org/3/library/functools.html#functools.lru_cache). Using this decorator, we can easily cache the values of functions and hence can use direct results instead of computation.

## Usage

There are two ways in which one can use this program:

### 1. Docker

If the user has Docker installed on their system, they can use docker to build an image and run their simulations on the image. The steps for the same are as follows:

1. Create the docker image:
 ```
 docker build -t life .
 ```
2. Run the docker image:
    a. Using a custom pattern file:
```
docker run --name life-cont -v </path/to/pattern/file>:/life/patterns/<filename> -it life:latest /bin/bash -c 'python runner.py --filename <filename> --iterations <iterations> && tree outputs'
```


If the user wants to use the pre-existing patterns, or has added their patterns in the `patterns/` folder before building the image, the user can simply run this command to use the file inside the docker context directly:
```
docker run --name life-cont -it life:latest /bin/bash -c 'python runner.py --filename patterns/<filename> --iterations <iterations> && tree outputs'

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


**The output images are made using a color map where a dead cell corresponds to the purple color and an alive cell corresponds to yellow.**

## Pattern Files

There are two pattern file formats supported currently:

### 1. Standard text file

A standard text file that contains the pattern in it. The pattern can be of any form and doesn't need to be a square particularly. `1` or `*` in the pattern denotes a live cell, any other character denotes a dead cell. For example, the content of `pattern.txt` should be:
```
--1----
----1--
-11-111
-------
```

### 2. Life 1.05 File format

There is also an experimental support of the [Life 1.05 File Format](https://www.conwaylife.com/wiki/Life_1.05) which is used to create large patterns. The parser follows strict format as described in the wiki and doesn't support custom rules as of now. `1` or `*` in the pattern denotes a live cell, any other character denotes a dead cell. An example file of this format is:

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

## Examples
There are certain patterns that are provided with the functionality in the patterns folder. The user can use those files directly to generate further generations.


A few examples of the 30th and 300th generation of the [Acorn](https://www.conwaylife.com/wiki/Acorn) pattern are below. The outputs folder also contains examples for 30th and 300th generation of [Breeder](https://conwaylife.com/wiki/Breeder_1). 

1. 30th generation:
![Example output of 30th generation](https://github.com/chahak13/game-of-life/blob/master/outputs/acorn_output_30_iterations.png)

1. 300th generation:
![Example output of 300th generation](https://github.com/chahak13/game-of-life/blob/master/outputs/acorn_output_300_iterations.png)

