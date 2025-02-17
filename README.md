## Maze Generator

Requires `pypng`. Run `pip install pypng`. Made to answer the question of if stable diffusion can learn mazes.

```
# By Charlie Gerrie 2025
# Outputs the maze into maze.png
# Usage:
#   python3 generator.py   (generates 5x5 proper maze)
#   python3 generator.py 3 5   (generates 5x5 improper maze with 3 walls removed and 5 added back)
#   python3 generator.py 0 0 7 (generates 7x7 proper maze)
# i.e. first 2 arguments allow you to add or remove walls to deviate from normal maze behavior,
# and the last argument lets you modify the maze dimensions from a default of 5x5.
```

You can also use `batch.sh` and `batch.bat` to generate many mazes at a time.

A proper 15x15 maze:

![image](https://github.com/cgerrie/maze-generator/blob/master/proper_maze.png)

An improper 15x15 maze. Note the unreachable areas and open areas allowing cycles:

![image](https://github.com/cgerrie/maze-generator/blob/master/improper_maze.png)
