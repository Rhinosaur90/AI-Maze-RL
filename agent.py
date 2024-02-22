import torch
import random
import numpy as np
import math
from MazeGame import MazeGame, Direction, Point
from collections import deque
from model import Linear_QNet, QTrainer
from helper import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 100
RHINO_SIZE = 20
LR = 0.0005

class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 #control randomness
        self.gamma = 0.99998 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) #popleft() if it fills
        self.model = Linear_QNet(9, 512, 4)
        self.trainer = QTrainer(self.model, lr=LR, gamma = self.gamma)
        #model, and trainer


    def get_state(self, game):
        head = game.Rhino
        point_l = Point(head.x - RHINO_SIZE, head.y)
        point_r = Point(head.x + RHINO_SIZE, head.y)
        point_u = Point(head.x, head.y - RHINO_SIZE)
        point_d = Point(head.x, head.y + RHINO_SIZE)
        
        #dir_l = game.direction == Direction.LEFT
        #dir_r = game.direction == Direction.RIGHT
        #dir_u = game.direction == Direction.UP
        #dir_d = game.direction == Direction.DOWN
        dist =math.hypot(head.x - game.WinPoint.x, head.y - game.WinPoint.y)
        if dist <= 0:
            dist = 1
        state = [ #need to refactor this
            # Danger up and down left and right
            (game.is_collision(point_r)),
            (game.is_collision(point_l)),
            (game.is_collision(point_u)),
            (game.is_collision(point_d)),

            #check if movement has already been done up down left right
            (game.is_alreadyseen(point_r)),
            (game.is_alreadyseen(point_l)),
            (game.is_alreadyseen(point_u)),
            (game.is_alreadyseen(point_d)),
            # Move direction
            #dir_l,
            #dir_r,
            #dir_u,
            #dir_d,
            
            # Win Distance 
            1 / ( dist/ 100)
            #game.WinPoint.x < game.Rhino.x,  # WinPoint left
            #game.WinPoint.x > game.Rhino.x,  # WinPoint right
            #game.WinPoint.y < game.Rhino.y,  # WinPoint up
            #game.WinPoint.y > game.Rhino.y   # WinPoint down
            ]

        return np.array(state, dtype=int)
        

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if filled

    def train_long_memory(self):
        print(len(self.memory))
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
            #mini_sample = self.memory[-BATCH_SIZE:]
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        #if self.epsilon > 20:
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0,0]
        if random.randint(0, 100) < self.epsilon:
            move = random.randint(0, 3)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move

def train():
    plot_scores=[]
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = MazeGame()
    while True:
        # get old state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            #train long memory and plot results
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game', agent.n_games, 'Score',score, 'Record: ',record)

            #plotting
            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)



if __name__ == '__main__':
    train()