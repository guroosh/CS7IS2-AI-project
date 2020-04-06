import Functions
from GridWorldRL import GridWorld
import tkinter as tk
import numpy as np
from collections import defaultdict
from matplotlib import pylab
from pylab import *


EPISODES = 200
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
        next_action = np.argmax(self.q_table[next_state])
        new_q = reward + self.gamma * self.q_table[next_state][next_action]
        self.q_table[current_state][current_action] = (1 - self.alpha)*self.q_table[current_state][current_action] + self.alpha*new_q








if __name__ == "__main__":
    grid_world = GridWorld()
    agent = Agent(list(range(grid_world.n_actions)))

    global_step = 0
    scores, episodes = [], []
    #grid_world = GridWorld()
    grid_world.set_obstacle_reward()
    #Functions.create_random_obstacles(grid_world, 0.05)
    Functions.create_fixed_obstacles(grid_world, 5)
    grid_world.create_grid_ui(grid_world.m, grid_world.n, (grid_world.start_x, grid_world.start_y),
                          (grid_world.end_x, grid_world.end_y), grid_world.obstacles)
    #tk.mainloop()
    

    for e in range(EPISODES):
        done = False
        score = 0
        state = grid_world.reset()
        #state = np.reshape(state, [1, 171])

        while not done:
            # fresh env
            grid_world.render()
            global_step += 1

            # get action for the current state and go one step in environment
            action = agent.get_action(state)
            next_state, reward, done = grid_world.step(action)
            #next_state = np.reshape(next_state, [1, 171])
            #next_action = agent.get_action(next_state)
            #agent.train_model(state, action, reward, next_state, next_action,
                              #done)
            agent.learn(str(state), action, reward, str(next_state))
            #print ("<state:{0} , action:{1} , reward:{2} , next_state:{3}>".format(str(state), str(action), str(reward), str(next_state)) )

            #print(agent.q_table)

            state = next_state

            #state = next_state
            # every time step we do training
            score += reward
            
            #state = copy.deepcopy(next_state)

            if done:
                scores.append(score)
                episodes.append(e)
                pylab.plot(episodes, scores, 'b')
                pylab.savefig("./save_graph/a_learning_.png")
                print("episode:", e, "  score:", score, "global_step",
                      global_step, "  epsilon:", agent.epsilon)

        