import pygame
import random
from enum import Enum
from collections import namedtuple

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
pygame.init()
font = pygame.font.Font('arial.ttf', 25)
    
Point = namedtuple('Point', 'x, y')
# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)

BLOCK_SIZE = 20
SPEED = 20

class MazeGame:

    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display
        self.direction = Direction.RIGHT
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Maze')
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.Rhino = Point(self.w/2, self.h/2)
        self.WinPoint = Point(0,0)
        self.score = 0
        self.maze = [
                    [0,0,1,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
                    [0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
                    [0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
                    [0,0,1,0,1,1,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0],
                    [0,0,1,0,1,2,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,1,0,1,0,1,1,1,1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,1,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,1,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,1,1,1,1,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,1,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
                    [0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
                    [0,1,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
                    [0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
                    [0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0],
                    [0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0],
                    [0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0],
                    [0,0,0,0,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,1,0,0,0,0,0,0],
                    [0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,1,1,1,1,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    ]
        self.mazeCollisions = []
        self.createMaze()
        self.frame_iteration = 0

    def createMaze(self): #start by creating an array and then print out if 1 and nothing if 0 and make each 0 or 1 be 20 px like the character
        blockW = int(self.w/BLOCK_SIZE)
        blockH = int(self.h/BLOCK_SIZE)
        for len in range(blockW):
            for heig in range(blockH):
                if self.maze[heig][len] == 1:
                    self.mazeCollisions.append(Point(len*BLOCK_SIZE,heig*BLOCK_SIZE))
                    pygame.draw.rect(self.display, RED, pygame.Rect(len*BLOCK_SIZE,heig*BLOCK_SIZE,BLOCK_SIZE,BLOCK_SIZE))
                elif self.maze[heig][len] == 2:
                    self.WinPoint = Point(len*BLOCK_SIZE,heig*BLOCK_SIZE)
                    pygame.draw.rect(self.display, WHITE, pygame.Rect(len*BLOCK_SIZE,heig*BLOCK_SIZE,BLOCK_SIZE,BLOCK_SIZE))


    def play_step(self):           
            self.frame_iteration += 1
            print(self.frame_iteration)
            # 1. collect user input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.direction = Direction.LEFT
                    elif event.key == pygame.K_RIGHT:
                        self.direction = Direction.RIGHT
                    elif event.key == pygame.K_UP:
                        self.direction = Direction.UP
                    elif event.key == pygame.K_DOWN:
                        self.direction = Direction.DOWN
                    # 2. move
                    self._move(self.direction)
            

            # 3. check if game over
            game_over = False
            if self._is_collision():
                game_over = True
                return game_over, self.score
            elif self._is_win_collision(): # will add different things if you win or lose like a score
                self.score += 100
                game_over = True
                return game_over, self.score

            # 5. update ui and clock
            self._update_ui()
            self.clock.tick(SPEED)
            # 6. return game over and score
            return game_over, self.score

    def _is_collision(self):
        # hits boundary
        if self.Rhino.x > self.w - BLOCK_SIZE or self.Rhino.x < 0 or self.Rhino.y > self.h - BLOCK_SIZE or self.Rhino.y < 0:
            return True
        elif self.Rhino in self.mazeCollisions:
            return True
        return False

    def _is_win_collision(self):
        if self.Rhino == self.WinPoint:
            return True
        return False

    def _update_ui(self):
        self.display.fill(BLACK)

        pygame.draw.rect(self.display, BLUE1, pygame.Rect(self.Rhino.x, self.Rhino.y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.display, BLUE2, pygame.Rect(self.Rhino.x+4, self.Rhino.y+4, 12, 12))
        self.createMaze()
        
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, direction):
        x = self.Rhino.x
        y = self.Rhino.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE

        self.Rhino = Point(x, y)

if __name__ == '__main__':
    game = MazeGame()
    
    while True:
        game_over, score = game.play_step()
        
        if game_over == True:
            break

    

