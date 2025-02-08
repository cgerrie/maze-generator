import sys
import random

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

def main():
    # Initialize the numbers to 0
    extra_removed, extra_added = 0, 0

    # Check if there are at least 2 arguments
    if len(sys.argv) > 1:
        try:
            extra_removed = int(sys.argv[1])
        except ValueError:
            extra_removed = 0

    if len(sys.argv) > 2:
        try:
            extra_added = int(sys.argv[2])
        except ValueError:
            extra_added = 0

    looking_for_proper = not (extra_removed > 0 or extra_added > 0)

    while True:
        n = 3
        remaining_walls, removed_walls = generate_maze(n, extra_added, extra_removed)
        proper_maze = is_maze(n, removed_walls)
        if proper_maze == looking_for_proper:
            break

    print(remaining_walls)
    print(is_maze(n, removed_walls))

if __name__ == "__main__":
    main()