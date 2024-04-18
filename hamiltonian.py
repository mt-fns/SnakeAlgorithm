import random

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0


grid = [[0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]]


def prim_algorithm(start, grid):  # takes in tuple for start coordinates, array of grids
    # improve: check for neighbors already in the maze before adding parents
    frontier = []
    adjacent = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    maze = []
    current = Node(None, start)
    frontier.append(current)
    # get adjacent nodes
    while frontier:
        for adj in adjacent:
            adj_coord = (current.position[0] - adj[0], current.position[1] - adj[1])
            if 0 <= adj_coord[0] < len(grid[0]) and 0 <= adj_coord[1] < len(grid):
                if adj_coord not in maze:
                    print(maze)
                    adj_node = Node(current, adj_coord)
                    frontier.append(adj_node)
        frontier.remove(current)
        maze.append(current.position)
        current = random.choice(frontier)

    print(maze)

prim_algorithm((0, 0), grid)
