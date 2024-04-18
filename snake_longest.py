import pygame
import random
from enum import Enum
from collections import namedtuple
from agent import get_state, longest_path

pygame.init()
font = pygame.font.Font('arial.ttf', 25)


# font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

BLOCK_SIZE = 20
SPEED = 50


class SnakeGame:

    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()

        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [self.head,
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()

        self.moves = []
        self.path = []

        self.display_moves = True  # display move

    def _place_food(self):
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self, action):
        # 1. display moves
        if self.display_moves:
            previous = self.head
            for coords in self.moves:
                x, y = self._get_moves(coords, previous)
                previous = Point(x, y)
                self.path.append(previous)

        # 2. move
        self._move(action)  # update the head
        self.snake.insert(0, self.head)

        # 3. check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()

        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return game_over, self.score

    def _is_collision(self):
        # hits boundary
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            print("boundary")
            return True
        # hits itself
        if self.head in self.snake[1:]:
            print("self")
            return True

        return False

    def _update_ui(self):
        self.display.fill(BLACK)

        if self.display_moves == True:
            for i in range(len(self.path)):
                if i < len(self.path) - 1:
                    pygame.draw.line(self.display, WHITE, Point(self.path[i].x + 10, self.path[i].y + 10), Point(self.path[i + 1].x + 10, self.path[i + 1].y + 10))

        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))
        # pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, direction):
        x = self.head.x
        y = self.head.y

        move = (direction[0]-x, direction[1]-y)   # direction - head
        x += move[0]
        y += move[1]
        self.head = Point(x, y)

    def _get_moves(self, path, previous):
        #x = self.head.x
        #y = self.head.y

        x = previous.x
        y = previous.y

        move = (path[0] - x, path[1] - y)  # direction - head
        x += move[0]
        y += move[1]

        return x, y





if __name__ == '__main__':
    #update algorithm so that snake gets fed in new information about boundary but same tail target (dont do this every first move of function, finish the moves while changing the boundaries and keeping the end goal the same
    game = SnakeGame()
    game_over = False
    score = 0
    actions = []
    # game loop

    while True:
        if not actions:
            head, apple, body = get_state(game)
            size = (game.w - 20, game.h - 20)
            start = head
            end = body[-1]  # end is tail
            boundary = body[:-1]  # boundary excludes head and tail
            actions = longest_path(size, start, end, boundary)
            game.moves = longest_path(size, start, end, boundary)  # store full move sequence in the game object

        game.path = []
        game_over, score = game.play_step(actions[0])
        actions.pop(0)

        if game_over == True:
            break
    print("Game Over")
    print('Final Score', score)
    pygame.quit()


