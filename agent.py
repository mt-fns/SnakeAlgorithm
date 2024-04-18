from aStar import Node

def get_state(game):
    #  gets current state of the game: location of head, location of body, location of food (return an array depicting the game)
    snake = game.snake
    head = snake[0]
    body = snake[1:]
    food = game.food

    start = (head.x, head.y)  # start node
    end = (food.x, food.y)
    boundary = []

    for i in body:
        boundary.append((i.x, i.y))

    return start, end, boundary


def path_finding(size, start, end, boundaries):
    # start/end = coords, size = tuple of width and height of game
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
                current = current.parent

            return path[::-1]  # reversed path

        children = []
        adjacent = [(0, -20), (0, 20), (-20, 0), (20, 0)]

        for x in adjacent:
            node_position = tuple(map(lambda i, j: i - j, current_node.position, x))  # generate adjacent coordinates

            # check if node is within boundaries
            if node_position[0] > size[0] or node_position[0] < 0 or node_position[1] > size[1] or node_position[1] < 0:
                continue

            # check for obstacles/walls
            for body in boundaries:
                if node_position[0] == body[0] and node_position[1] == body[1]:
                    break

            else:
                child_node = Node(current_node, node_position)  # create child node
                children.append(child_node)

        for child in children:
            for closed in closed_list:  # check if child in closed list
                if child == closed:
                    break
            else:
                child.g = current_node.g + 20
                child.h = abs(child.position[0] - end_node.position[0]) + abs(child.position[1] - end_node.position[1])  # manhattan distance
                child.f = child.g + child.h

                for open_node in open_list:
                    if child == open_node:
                        if child.g >= open_node.g:
                            break
                else:
                    open_list.append(child)

def longest_path(size, start, end, boundaries):
    # start/end = coords
    open_list = []
    closed_list = []
    all_paths = []
    final_path = None


    start_node = Node(None, start)
    start_node.g = 0
    start_node.f = 0
    start_node.h = 0

    end_node = Node(None, end)
    end_node.g = 0
    end_node.f = 0
    end_node.h = 0

    open_list.append(start_node)
    counter = 0

    while open_list:
        counter += 1
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):  # get the largest f score to be the current node
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

            all_paths.append(path[::-1])  # reversed path

        children = []
        adjacent = [(0, -20), (0, 20), (-20, 0), (20, 0)]

        # generate adjacent coordinates
        for x in adjacent:
            node_position = tuple(map(lambda i, j: i - j, current_node.position, x))
            hit = False

            # check if node is within boundaries
            if node_position[0] > size[0] or node_position[0] < 0 or node_position[1] > size[1] or node_position[1] < 0:
                continue

            # check for obstacles/walls
            for body in boundaries:
                if node_position[0] == body[0] and node_position[1] == body[1]:
                    hit = True
                    break

            # create child node
            if not hit:
                child_node = Node(current_node, node_position)
                children.append(child_node)

        for child in children:
            for closed in closed_list:  # check if child in closed list
                if child == closed:
                    break
            else:
                child.g = current_node.g + 40
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

    for possible in all_paths:
        if not final_path:
            final_path = possible
        elif len(possible) >= len(final_path):
            final_path = possible

    return final_path[1:]
