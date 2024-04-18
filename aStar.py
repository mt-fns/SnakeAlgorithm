import math


class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

def a_star(maze, start, end):
    # start/end = coords
    open_list = []
    closed_list = []

    start_node = Node(None, start)
    start_node.g = 0
    start_node.f = 0
    start_node.h = 0

    end_node = Node(None, end)
    end_node.g = 0
    end_node.f = 0
    end_node.h = 0

    open_list.append(start_node)

    while open_list:
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        open_list.pop(current_index)
        closed_list.append(current_node)

        if current_node == end_node:
            path = []
            current = current_node

            # back track to get path
            while current is not None:
                path.append(current.position)
                print(current.position)
                current = current.parent

            return path[::-1]  # reversed path

        children = []
        adjacent = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        for x in adjacent:
            node_position = tuple(map(lambda i, j: i - j, current_node.position, x))  # generate adjacent coordinates

            # check if node is within boundaries
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (
                    len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
                continue

            # check for obstacles/walls
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            child_node = Node(current_node, node_position)  # create child node
            children.append(child_node)

        for child in children:
            for closed in closed_list:  # check if child in closed list
                if child == closed:
                    break
            else:
                child.g = current_node.g + 1
                child.h = abs(child.position[0] - end_node.position[0]) + abs(child.position[1] - end_node.position[1])  # manhattan distance
                child.f = child.g + child.h

                for open_node in open_list:
                    if child == open_node:
                        if child.g >= open_node.g:
                            break
                else:
                    open_list.append(child)

def main():

    maze = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    start = (0, 0)
    end = (2, 2)

    path = a_star(maze, start, end)
    print(path)





