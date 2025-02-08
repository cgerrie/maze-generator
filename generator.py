#!/usr/bin/env python
# By Charlie Gerrie 2025
# Outputs the maze into maze.png
# Usage:
#   python3 generator.py   (generates 5x5 proper maze)
#   python3 generator.py 3 5   (generates 5x5 improper maze with 3 walls removed and 5 added back)
#   python3 generator.py 0 0 7 (generates 7x7 proper maze)
# i.e. first 2 arguments allow you to add or remove walls to deviate from normal maze behavior,
# and the last argument lets you modify the maze dimensions from a default of 5x5.

import sys
import random
import png

### Maze generating code

def join_walls(components, cell1, cell2):
    cell1_comp = []
    for component in components:
        if cell1 in component:
            cell1_comp = component
            break
    if cell1_comp == []:
        raise Exception("couldn't find comp")
    if cell2 in cell1_comp:
        join = False
        return components, join

    join = True

    cell2_comp = []
    for component in components:
        if cell2 in component:
            cell2_comp = component
            break
    if cell2_comp == []:
        raise Exception("couldn't find comp")

    newComponent = cell1_comp.union(cell2_comp)

    newComponents = [component for component in components if component != cell1_comp and component != cell2_comp]
    newComponents.append(newComponent)
    return newComponents, join

# Does a flood fill to check if all parts are reachable but only once
def is_maze(n,  walls_removed):
    visited_cells = set([(0, 0)])
    boundary = set([(0, 0)])

    while len(boundary) > 0:
        destinations = set()
        for cell in boundary:
            for wall in walls_removed:
                if wall[0] == cell and wall[1] not in visited_cells:
                    if wall[1] in destinations:
                        print("Cycle detected")
                        return False
                    destinations.add(wall[1])
                elif wall[1] == cell and wall[0] not in visited_cells:
                    if wall[0] in destinations:
                        print("Cycle detected")
                        return False
                    destinations.add(wall[0])
        visited_cells = visited_cells.union(destinations)
        boundary = destinations

    # check visited all possible cells
    if len(visited_cells) != n*n:
        print("Unreachable component detected")
        return False

    # Otherwise
    return True


def generate_maze(n, extra_added = 0, extra_removed = 0):
    cells = [(i, j) for i in range(n) for j in range(n)]
    random.shuffle(cells)
    walls = []

    # Generate all possible walls
    for i in range(n):
        for j in range(n):
            # Right wall (to the right neighbor)
            if j < n - 1:
                walls.append(((i, j), (i, j + 1)))
            # Down wall (to the bottom neighbor)
            if i < n - 1:
                walls.append(((i, j), (i + 1, j)))
    random.shuffle(walls)

    removed_walls = []
    remaining_walls = list(walls)

    components = [set([cell]) for cell in cells]
    for wall in walls:
        components, join = join_walls(components, wall[0], wall[1])
        if join:
            removed_walls.append(wall)
            remaining_walls.remove(wall)

    # Remove extra_removed walls
    random.shuffle(remaining_walls)
    extra_removed_walls = []
    for i in range(min(len(remaining_walls), extra_removed)):
        extra_removed_walls.append(remaining_walls[i])
    for wall in extra_removed_walls:
        removed_walls.append(wall)
        remaining_walls.remove(wall)


    # Add back extra_added walls
    random.shuffle(removed_walls)
    extra_added_walls = []
    for i in range(min(len(removed_walls), extra_added)):
        extra_added_walls.append(removed_walls[i])
    for wall in extra_added_walls:
        remaining_walls.append(wall)
        removed_walls.remove(wall)

    return remaining_walls, removed_walls

### Rendering Code

# Takes x and y as pixel indices
def draw_rectangle(pixels, x1, x2, y1, y2):
    for i in range(min(x1, x2), max(x1, x2)):
        for j in range(min(y1, y2), max(y1, y2)):
            pixels[i][j] = True

# Takes x and y as indices, draws to the right of the cell
def add_horizontal_wall_to_pixels(pixels, x, y, path_width=20, wall_width=4):
    startX = x * path_width + (x + 1) * wall_width
    startY = (y + 1) * (path_width + wall_width)
    endX = startX + path_width
    endY = startY + wall_width
    draw_rectangle(pixels, startX, endX, startY, endY)

# Takes x and y as indices, draws on the bottom of the cell
def add_vertical_wall_to_pixels(pixels, x, y, path_width=20, wall_width=4):
    startX = (x + 1) * (path_width + wall_width)
    startY = y * path_width + (y + 1) * wall_width
    endX = startX + wall_width
    endY = startY + path_width
    draw_rectangle(pixels, startX, endX, startY, endY)

def output_maze_to_png(n, remaining_walls, path_width=20, wall_width=4):
    pixel_dimension = (n * path_width + (n + 1) * wall_width) # in actual pixels

    # make logical pixels, indexed by cell coordinate
    pixels = [[False] * pixel_dimension for _ in range(pixel_dimension)]
    for i in range(n):
        # top & left sides
        new_vertical = ((-1, i), (0, i))
        new_horizontal = ((i, -1), (i, 0))
        remaining_walls.append(new_vertical)
        remaining_walls.append(new_horizontal)

        # bottom and right sides
        new_vertical = ((n - 1, i), (n, i))
        new_horizontal = ((i, n - 1), (i, n))
        remaining_walls.append(new_vertical)
        remaining_walls.append(new_horizontal)

    for wall in remaining_walls:
        p1, p2 = wall
        x1, y1 = p1
        x2, y2 = p2
        if abs(x1 - x2) == 1 and y1 == y2:
            add_vertical_wall_to_pixels(pixels, min(x1, x2), y1, path_width, wall_width)
        elif abs(y1 - y2) == 1 and x1 == x2:
            add_horizontal_wall_to_pixels(pixels, x1, min(y1, y2), path_width, wall_width)

    # make colour pixels
    wall_colour = (0, 0, 0)
    background_colour = (255, 255, 255)
    colour_pixels = []
    for i in range(pixel_dimension):
        row = ()
        for j in range(pixel_dimension):
            colour = wall_colour if pixels[i][j] else background_colour
            row = row + colour
        colour_pixels.append(row)

    # output file
    with open('maze.png', 'wb') as f:
        w = png.Writer(pixel_dimension, pixel_dimension, greyscale=False)
        w.write(f, colour_pixels)

### Main code

def main():
    extra_removed, extra_added = 0, 0
    n = 5 # Default if third argument not supplied

    if len(sys.argv) > 1:
        try:
            extra_removed = int(sys.argv[1])
        except ValueError:
            pass

    if len(sys.argv) > 2:
        try:
            extra_added = int(sys.argv[2])
        except ValueError:
            pass

    if len(sys.argv) > 3:
        try:
            n = int(sys.argv[3])
        except ValueError:
            pass

    looking_for_proper = not (extra_removed > 0 or extra_added > 0)

    while True:
        remaining_walls, removed_walls = generate_maze(n, extra_added, extra_removed)
        proper_maze = is_maze(n, removed_walls)
        if proper_maze == looking_for_proper:
            break

    print(remaining_walls)
    print(f"Is proper maze: {is_maze(n, removed_walls)}")
    output_maze_to_png(n, remaining_walls)

if __name__ == "__main__":
    main()