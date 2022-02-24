import pygame
from enum import Enum
from collections import namedtuple
from random import randint

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


class Snake(object):

    def __init__(self, width, height, speed):
        self.width = width
        self.height = height
        self.speed = speed

        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('snake')
        self.clock = pygame.time.Clock()
        self.score = 0

        self.direction = Direction.RIGHT
        self.head = Point(self.width//2, self.height//2)
        self.snake = [self.head,
                      Point(self.head.x-BLOCKSIZE, self.head.y),
                      Point(self.head.x-2*BLOCKSIZE, self.head.y)]


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

    def _move(self, direction):
        
        # self.snake.pop()
        x, y = self.head.x, self.head.y
        if direction == Direction.UP:
            y -= BLOCKSIZE
        elif direction == Direction.DOWN:
            y += BLOCKSIZE
        elif direction == Direction.LEFT:
            x -= BLOCKSIZE
        elif direction == Direction.RIGHT:
            x += BLOCKSIZE

        self.head = Point(x, y)
        
        

    def _det_collision(self):
        if self.head in self.snake[1:]:
            return True
        # if self.head.x >= self.width or self.head.x < 0 or self.head.y >= self.height or self.head.y < 0:
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

    def _play_game(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if self.direction == Direction.DOWN:
                        continue
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    if self.direction == Direction.UP:
                        continue
                    self.direction = Direction.DOWN
                elif event.key == pygame.K_LEFT:
                    if self.direction == Direction.RIGHT:
                        continue
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    if self.direction == Direction.LEFT:
                        continue
                    self.direction = Direction.RIGHT
            
        self._move(self.direction)
        self.snake.insert(0, self.head)
        self._cross_wall()
        self._draw_ui()
        self.clock.tick(self.speed)
        
        

        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()

        game_over = False
        if self._det_collision():
            game_over = True
            return game_over, self.score

        return game_over, self.score

if __name__ == '__main__':
    snake = Snake(1280, 720, 10)

    while True:
        game_over, score = snake._play_game()

        if game_over:
            print('Final Score: %d' %score)
            break

    pygame.quit()