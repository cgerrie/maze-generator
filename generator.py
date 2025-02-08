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

def generate_maze(n):
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

    print(remaining_walls)
    # print(removed_walls)
    return remaining_walls


def main():
    # Initialize the numbers to 0
    extraRemoved, extraAdded = 0, 0

    # Check if there are at least 2 arguments
    if len(sys.argv) > 1:
        try:
            extraRemoved = int(sys.argv[1])
        except ValueError:
            extraRemoved = 0

    if len(sys.argv) > 2:
        try:
            extraAdded = int(sys.argv[2])
        except ValueError:
            extraAdded = 0

    generate_maze(3)

if __name__ == "__main__":
    main()