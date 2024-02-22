import pygame
import random
from enum import Enum
import math
import numpy as np
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
SPEED = 180

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
        #self.Rhino = Point(self.w/2, self.h/2)
        self.WinPoint = Point(0,0)
        self.score = 0
        # self.maze = [
        #             [0,0,1,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
        #             [0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
        #             [0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
        #             [0,0,1,0,1,1,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0],
        #             [0,0,1,0,1,2,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
        #             [0,0,1,0,1,0,1,1,1,1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
        #             [0,0,1,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        #             [0,0,1,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        #             [0,0,1,1,1,1,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        #             [0,0,1,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        #             [0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
        #             [0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
        #             [0,1,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
        #             [0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
        #             [0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0],
        #             [0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0],
        #             [0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0],
        #             [0,0,0,0,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,1,0,0,0,0,0,0],
        #             [0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,1,1,1,1,0,0,0,0],
        #             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0],
        #             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0],
        #             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
        #             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        #             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        #             ]
        self.maze = [
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                    [1,3,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
                    [1,1,1,1,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
                    [1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,1],
                    [1,0,1,1,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,1,1,1,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,1,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1],
                    [1,0,0,1,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,1,0,0,0,1,1,1,1,1,1],
                    [1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,1,0,0,1,1,0,0,1,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,1,1,0,0,0,0,0,1,0,0,0,0,1],
                    [1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1,1],
                    [1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
                    [1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
                    [1,0,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,1,0,1],
                    [1,0,0,1,0,0,0,1,0,0,1,1,1,1,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,1],
                    [1,0,1,1,1,1,0,1,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,1],
                    [1,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,2,1],
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                    ]
        self.mazeCollisions = []
        self.placeRhino()
        self.createMaze()
        self.frame_iteration = 0      
        self.visitedPoints = []

    def placeRhino(self):
        blockW = int(self.w/BLOCK_SIZE)
        blockH = int(self.h/BLOCK_SIZE)
        for len in range(blockW):
            for heig in range(blockH):
                if self.maze[heig][len] == 3:
                    self.Rhino = Point(len*BLOCK_SIZE,heig*BLOCK_SIZE)

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
                


    def play_step(self, action):
            self.frame_iteration += 1
            # 1. collect user input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            # 2. move
            self._move(action)
            
            # 3. check if game over
            reward = 0
            game_over = False
            if self.is_collision() or self.frame_iteration > 130:
                reward = -150
                self.score -= 150
                game_over = True
                return reward, game_over, self.score
            
            if self._is_win_collision(): # will add different things if you win or lose like a score
                self.score += 3000
                reward = 3000
                game_over = True
                return reward, game_over, self.score

            # distance reward based on how close you are to win point
            distance = math.hypot(self.Rhino.x - self.WinPoint.x, self.Rhino.y - self.WinPoint.y)
            reward = (2000 * math.exp(-0.5 * math.pow((distance / 200), 2))) / (self.frame_iteration*2)

            if self.Rhino not in self.visitedPoints:
                self.visitedPoints.append(self.Rhino)              
            else:
                #self.score -= 20
                reward = 0

            self.score += reward

            # 5. update ui and clock
            self._update_ui()
            self.clock.tick(SPEED)
            # 6. return game over and score
            return reward, game_over, self.score

    def is_collision(self,pt=None):
        if pt is None:
            pt = self.Rhino
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        elif pt in self.mazeCollisions:
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

    def _move(self, action):
        # [straign, right, left]
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]

        if np.array_equal(action,[1,0,0,0]):
            new_dir = clock_wise[0] #Right
        elif np.array_equal(action,[0,1,0,0]):
            new_dir = clock_wise[1] # Down
        elif np.array_equal(action,[0,0,1,0]):
            new_dir = clock_wise[2] #Left
        elif np.array_equal(action,[0,0,0,1]):
            new_dir = clock_wise[3] # Up

        self.direction = new_dir

        x = self.Rhino.x
        y = self.Rhino.y

        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
            
        self.Rhino = Point(x, y)
    
    def is_alreadyseen(self,pt=None):
        if pt is None:           
            pt = self.Rhino
        if pt in self.visitedPoints:
            return True
        else:
            return False
