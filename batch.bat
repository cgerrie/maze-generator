@echo off
rem This script will run the generator.py script 100 times, passing all arguments,
rem and then rename the output maze.png files to maze1.png, maze2.png, ..., maze100.png
for /l %%x in (1, 1, 100) do (
    python generator.py %*
    move /Y maze.png maze%%x.png
)