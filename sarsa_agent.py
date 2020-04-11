import numpy as np
import random
from collections import defaultdict
from GridWorld import GridWorld
import Functions
import tkinter as tk


# SARSA agent learns every time step from the sample <s, a, r, s', a'>
class SARSAgent:
    def __init__(self, actions):
        self.actions = actions
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.epsilon = 0.1
        self.q_table = defaultdict(lambda: [0.0, 0.0, 0.0, 0.0])

    # with sample <s, a, r, s', a'>, learns new q function
    def learn(self, state, action, reward, next_state, next_action):
        current_q = self.q_table[state][action]
        next_state_q = self.q_table[next_state][next_action]
        new_q = (current_q + self.learning_rate *
                (reward + self.discount_factor * next_state_q - current_q))
        self.q_table[state][action] = new_q

    # get action for the state according to the q function table
    # agent pick action of epsilon-greedy policy
    def get_action(self, state):
        if np.random.rand() < self.epsilon:
            # take random action
            action = np.random.choice(self.actions)
        else:
            # take action according to the q function table
            state_action = self.q_table[state]
            action = self.arg_max(state_action)
        return action

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
    #env = Env()
    grid_world = GridWorld()
    grid_world.set_obstacle_reward()
    #Functions.create_random_obstacles(grid_world, 0.05)
    Functions.create_fixed_obstacles(grid_world, 5)
    grid_world.create_grid_ui(grid_world.m, grid_world.n, (grid_world.start_x, grid_world.start_y),
                          (grid_world.end_x, grid_world.end_y), grid_world.obstacles)

    agent = SARSAgent(actions=list(range(grid_world.action_size)))
    number_of_episodes = 10
    for episode in range(number_of_episodes):
        # reset environment and initialize state

        state = grid_world.reset()
        # get action of state from agent
        action = agent.get_action(str(state))

        while True:
            grid_world.render()

            # take action and proceed one step in the environment
            next_state, reward, done = grid_world.step(action)
            next_action = agent.get_action(str(next_state))

            # with sample <s,a,r,s',a'>, agent learns new q function
            agent.learn(str(state), action, reward, str(next_state), next_action)

            state = next_state
            action = next_action

            # print q function of all states at screen
            #env.print_value_all(agent.q_table)

            # if episode ends, then break
            if done:
                break

