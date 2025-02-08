#!/bin/bash
# This script will run the generator.py script 100 times, passing all arguments,
# and then rename the output maze.png files to maze1.png, maze2.png, ..., maze100.png
for run in {1..100}
do
    python3 generator.py $@
    mv maze.png "maze$run.png"
done