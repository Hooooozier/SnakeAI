import pygame
from enum import Enum
from collections import namedtuple
from random import randint
import numpy as np
from pygame.constants import KEYDOWN

pygame.init()

font = pygame.font.Font('arial.ttf', 31)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (0, 255, 255)
BLUE = (255, 0, 0)

class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

Point = namedtuple('Point', 'x, y')
BLOCKSIZE = 20


class SnakeAI(object):

    def __init__(self, width=1280, height=760, speed=40):
        self.width = width
        self.height = height
        self.speed = speed

        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('snake')
        self.clock = pygame.time.Clock()
        self.reset()


    def reset(self):
        self.score = 0

        self.direction = Direction.RIGHT
        self.head = Point(self.width//2, self.height//2)
        self.snake = [self.head,
                      Point(self.head.x-BLOCKSIZE, self.head.y),
                      Point(self.head.x-2*BLOCKSIZE, self.head.y)]

        self.frame_itertions = 0
        self.food = None
        self._place_food()

    def _place_food(self):
        x = randint(0, (self.width-BLOCKSIZE)//BLOCKSIZE)*BLOCKSIZE
        y = randint(0, (self.height-BLOCKSIZE)//BLOCKSIZE)*BLOCKSIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def _draw_ui(self):
        self.display.fill(BLACK)
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCKSIZE, BLOCKSIZE))

        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE, pygame.Rect(pt.x, pt.y, BLOCKSIZE, BLOCKSIZE))

        text = font.render('Score: ' + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])

        pygame.display.flip()

    def _move(self, action):

        close_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = close_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = close_wise[idx]
        elif np.array_equal(action, [0, 1, 0]):
            new_dir = close_wise[(idx+1)%4]
        elif np.array_equal(action, [0, 0, 1]):
            new_dir = close_wise[(idx-1)%4]

        self.direction = new_dir
        x, y = self.head.x, self.head.y
        if self.direction == Direction.UP:
            y -= BLOCKSIZE
        elif self.direction == Direction.DOWN:
            y += BLOCKSIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCKSIZE
        elif self.direction == Direction.RIGHT:
            x += BLOCKSIZE

        self.head = Point(x, y)
        
        

    def det_collision(self, pt=None):
        if pt is None:
            pt = self.head
        if pt in self.snake[1:]:
            return True
        # if self.head.x > self.width-BLOCKSIZE or self.head.x < 0 or self.head.y > self.height-BLOCKSIZE or self.head.y < 0:
        #     return True
        return False

    def _cross_wall(self):
        for i in range(len(self.snake)):
            pt = self.snake[i]
            if pt.x > self.width:
                pt_new = Point(pt.x - self.width, pt.y)
                self.snake[i] = pt_new
            elif pt.x < 0:
                pt_new = Point(pt.x + self.width, pt.y)
                self.snake[i] = pt_new
            if pt.y > self.height:
                pt_new = Point(pt.x, pt.y - self.height)
                self.snake[i] = pt_new
            elif pt.y < 0:
                pt_new = Point(pt.x, pt.y + self.height)
                self.snake[i] = pt_new
        # lose head when move across wall, resign head 
        self.head = self.snake[0]

    def play_game(self, action):
        self.frame_itertions += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            
        self._move(action)
        self.snake.insert(0, self.head)
        self._cross_wall()
        
        
        game_over = False
        if self.det_collision() or self.frame_itertions > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score
        
        reward = 0
        if self.head == self.food:
            self.score += 1
            reward += 10
            self._place_food()
        else:
            self.snake.pop()

        self._draw_ui()
        self.clock.tick(self.speed)

        return reward, game_over, self.score

if __name__ == '__main__':
    snake = SnakeAI(1280, 720, 10)

    while True:
        idx = randint(0, 2)
        action = [0, 0, 0]
        action[idx] = 1
        reward, game_over, score = snake.play_game(action)

        if game_over:
            print('Final Score: %d' %score)
            break

    pygame.quit()