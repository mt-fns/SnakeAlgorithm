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
    all_paths = []

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
        for index, item in enumerate(open_list):  # get the smallest f score to be the current node
            if item.f > current_node.f:
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
                current = current.parent

            all_paths.append(path[::-1]) # reversed path

        children = []
        adjacent = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        # generate adjacent coordinates
        for x in adjacent:
            node_position = tuple(map(lambda i, j: i - j, current_node.position, x))

            # check if node is within boundaries
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (
                    len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
                continue

            # check for obstacles/walls
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # create child node
            child_node = Node(current_node, node_position)
            children.append(child_node)

        for child in children:
            for closed in closed_list:  # check if child in closed list
                if child == closed:
                    break
            else:
                child.g = current_node.g + 1
                child.h = abs(child.position[0] - end_node.position[0]) + abs(child.position[1] - end_node.position[1])  # manhattan distance
                child.f = child.g + child.h
                present = False  # check if node is already present in open_node

                for open_node in open_list:
                    if child == open_node:
                        if child.g < open_node.g:
                            present = True
                    if child == open_node:
                        if child.g >= open_node.g:
                            ind = open_list.index(open_node)
                            open_list[ind] = child

                if not present:
                    open_list.append(child)

    longest_path = None
    for possible in all_paths:
        print(len(possible))
        if not longest_path:
            longest_path = possible
        elif len(possible) >= len(longest_path):
            longest_path = possible

    return longest_path


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
    end = (8, 6)

    print(a_star(maze, start, end))



