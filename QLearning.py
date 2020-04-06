import numpy as np
from collections import defaultdict


class QLearning:
    # To Do: Fill in from here !
    def __init__(self, actions):
        self.actions = actions
        self.alpha = 0.1  # Facteur d'apprentissage
        self.gamma = 0.85
        self.actions = actions
        self.epsilon = 0.01
        self.q_table = defaultdict(lambda: [0.0, 0.0, 0.0, 0.0])

    def get_action(self, state):
        # next_action = np.random.choice(self.actions)
        if np.random.uniform() > self.epsilon:
            # choisir la meilleure action
            action_values = self.q_table[state]
            argmax_actions = []  # La meilleure action peut ne pas exister donc on elle est choisie aléatoirement
            for i in range(len(action_values)):
                if action_values[i] == np.max(action_values):
                    argmax_actions.append(i)
            next_action = np.random.choice(argmax_actions)
        else:
            next_action = np.random.choice(self.actions)
        if self.epsilon > 0:
            self.epsilon -= 0.00001  # Décrementer espsilon pour Arreter l'exploration aléatoire qu'on aura un politique optimale
        if self.epsilon < 0:
            self.epsilon = 0

        return next_action

    def learn(self, current_state, current_action, reward, next_state):
        next_action = np.argmax(self.q_table[next_state])
        new_q = reward + self.gamma * self.q_table[next_state][int(next_action)]
        self.q_table[current_state][current_action] = (1 - self.alpha) * self.q_table[current_state][
            current_action] + self.alpha * new_q
