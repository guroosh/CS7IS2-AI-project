import Functions
from GridWorld import GridWorld
import tkinter as tk
import numpy as np
from collections import defaultdict
from matplotlib import pylab
from pylab import *
import random
import time


EPISODES = 1000
class Agent:
    def __init__(self,actions):
        self.alpha = 0.1
        self.gamma = 0.85
        self.epsilon = 0.01
        # actions which agent can do
        self.action_space = ['u', 'd', 'l', 'r']
        self.n_actions = len(self.action_space)
        self.actions = actions
        self.q_table = defaultdict(lambda : [0.0,0.0,0.0,0.0])
    
    def get_action(self, state):
        #next_action = np.random.choice(self.actions)
        if np.random.uniform() > self.epsilon :
            #choosing the best action
            action_values = self.q_table[str(state)]
            argmax_actions=[] # choosing random action if best is not available
            for i in range (len(action_values)) :
                if action_values[i] == np.max(action_values) :
                    argmax_actions.append(i)
            next_action = np.random.choice(argmax_actions) 
        else :
             next_action = np.random.choice(self.actions)
        if self.epsilon > 0 :
            self.epsilon -= 0.00001 
        if self.epsilon < 0 :
            self.epsilon = 0
        return next_action
        
    def learn(self,current_state,current_action,reward,next_state):
        next_action = self.arg_max(self.q_table[next_state])
        new_q = reward + self.gamma * self.q_table[next_state][next_action]
        self.q_table[current_state][current_action] = (1 - self.alpha) * self.q_table[current_state][current_action] + self.alpha * new_q

    @staticmethod    
    def arg_max(state_action):
        max_index_list = []
        max_value = state_action[0]
        for index, value in enumerate(state_action):
            if value > max_value:
                max_index_list.clear()
                max_value = value
                max_index_list.append(index)
            elif value == max_value:
                max_index_list.append(index)
        return random.choice(max_index_list)






if __name__ == "__main__":
    grid_world = GridWorld(10,10)
    agent = Agent(list(range(4)))

    global_step = 0
    scores, episodes = [], []
    
    #grid_world.set_obstacle_reward()
    #Functions.create_random_obstacles(grid_world, 0.05)
    Functions.create_random_obstacles(grid_world, 0.205)
    grid_world.scan_grid_and_generate_graph()
    grid_world.print_graph()
    Functions.create_fixed_obstacles(grid_world, 5)
    grid_world.create_grid_ui(grid_world.m, grid_world.n, (grid_world.start_x, grid_world.start_y),
                          (grid_world.end_x, grid_world.end_y), grid_world.obstacles)
    
    

    for e in range(EPISODES):
        done = False
        score = 0
        start_time = time.time()
        state = grid_world.reset()
        grid_world.is_visited = [[0] * grid_world.m for temp in range(grid_world.n)]

        while not done:
            # fresh env
            grid_world.render()
            global_step += 1

            # get action for the current state and go one step in environment
            action = agent.get_action(str(state))
            next_state, reward, done = grid_world.step(action)
            agent.learn(str(state), action, reward, str(next_state))
            #if reward != 0:
               # print("<state:{0} , action:{1} , reward:{2} , next_state:{3}>".format(
                 #   str(state), str(action), str(reward), str(next_state)))
            grid_world.is_visited[state[0]][state[1]] += 1
            state = next_state
            
            score += reward
           

            if done:
                scores.append(score)
                episodes.append(e)
                pylab.plot(episodes, scores, 'b')
                pylab.savefig("./save_graph/q_learning10.png")
                
                print("episode:", e, "  score:", score, "global_step",
                      global_step, "  epsilon:", agent.epsilon)
    end_time = time.time()
    total_time = end_time - start_time
    print(total_time)
    #print(agent.q_table)    