import time
import tkinter as tk
import random
import numpy as np

from Graph import Graph


class GridWorld:

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.frame = tk.Canvas(bg=color_background, height=height, width=height)
        self.frame.pack()
        self.agent = ()
        self.agent_ui = ()
        self.length = ()
        self.possible_moves = ()
        self.graph = Graph(str(start_x) + ',' + str(start_y))

    def create_grid(self, m, n, start, end, obstacles):
        l1 = (self.width - (2 * padding)) / m
        l2 = (self.height - (2 * padding)) / n
        length = min(l1, l2)
        self.length = length
        for i in range(m):
            for j in range(n):
                color = color_normal
                if (i, j) in obstacles:
                    color = color_walls
                if start == (i, j):
                    color = 'sea green'
                if end == (i, j):
                    color = 'red'
                self.frame.create_rectangle(i * length + padding, j * length + padding, i * length + padding + length,
                                            j * length + padding + length, fill=color)
        self.update_agent((start_x, start_y))
        self.frame.update()

    def update_agent(self, agent):
        length = self.length
        self.frame.delete(self.agent_ui)
        self.agent = agent
        self.agent_ui = self.frame.create_oval(
            ((length * agent[0]) + padding + agent_padding,
             (length * agent[1]) + padding + agent_padding),
            ((length * agent[0]) + length + padding - agent_padding,
             (length * agent[1]) + length + padding - agent_padding),
            fill='cyan')
        self.frame.update()

    def move_agent(self):
        data.create_grid(m, n, (start_x, start_y), (end_x, end_y), obstacles)
        directions = ['east', 'west', 'north', 'south']
        for i in range(100):
            time.sleep(0.4)
            possible_index = np.where(self.possible_moves[self.agent[0]][self.agent[1]])[0]
            if possible_index.size == 0:
                print("No possible move")
                break
            move = random.choice(possible_index)
            move = directions[move]
            if move == 'east':
                if self.possible_moves[self.agent[0]][self.agent[1]][0]:
                    self.agent = (self.agent[0] + 1, self.agent[1])
                    self.update_agent(self.agent)
            if move == 'west':
                if self.possible_moves[self.agent[0]][self.agent[1]][1]:
                    self.agent = (self.agent[0] - 1, self.agent[1])
                    self.update_agent(self.agent)
            if move == 'north':
                if self.possible_moves[self.agent[0]][self.agent[1]][2]:
                    self.agent = (self.agent[0], self.agent[1] - 1)
                    self.update_agent(self.agent)
            if move == 'south':
                if self.possible_moves[self.agent[0]][self.agent[1]][3]:
                    self.agent = (self.agent[0], self.agent[1] + 1)
                    self.update_agent(self.agent)
        tk.mainloop()

    def generate_graph(self):
        for i in range(m):
            for j in range(n):
                if (i, j) not in obstacles:
                    east = True
                    west = True
                    north = True
                    south = True
                    if i == 0:
                        west = False
                    if i == m - 1:
                        east = False
                    if j == 0:
                        north = False
                    if j == n - 1:
                        south = False
                    if (i + 1, j) in obstacles:
                        east = False
                    if (i - 1, j) in obstacles:
                        west = False
                    if (i, j + 1) in obstacles:
                        south = False
                    if (i, j - 1) in obstacles:
                        north = False

                    self.graph.adjacency_map[str(i) + ',' + str(j)] = []
                    if east:
                        self.graph.adjacency_map[str(i) + ',' + str(j)].append((i + 1, j))
                    if west:
                        self.graph.adjacency_map[str(i) + ',' + str(j)].append((i - 1, j))
                    if north:
                        self.graph.adjacency_map[str(i) + ',' + str(j)].append((i, j - 1))
                    if south:
                        self.graph.adjacency_map[str(i) + ',' + str(j)].append((i, j + 1))

    def scan_grid(self):
        self.possible_moves = [[tuple()] * m for temp in range(n)]
        for i in range(m):
            for j in range(n):
                east = True
                west = True
                north = True
                south = True
                if i == 0:
                    west = False
                if i == m - 1:
                    east = False
                if j == 0:
                    north = False
                if j == n - 1:
                    south = False
                if (i + 1, j) in obstacles:
                    east = False
                if (i - 1, j) in obstacles:
                    west = False
                if (i, j + 1) in obstacles:
                    south = False
                if (i, j - 1) in obstacles:
                    north = False
                self.possible_moves[i][j] = (east, west, north, south)

    def print_graph(self):
        graph = self.graph
        for k in graph.adjacency_map:
            print(k + " -> ", end='')
            for l in graph.adjacency_map[k]:
                print(str(l[0]) + "," + str(l[1]) + " : ", end='')
            print()


color_background = 'snow3'
color_walls = 'black'
color_normal = 'white'

padding = 30
agent_padding = 10

m = 10
n = 10
start_x = 0
start_y = 0
end_x = m - 1
end_y = n - 1

height = 700
width = 700
data = GridWorld(height, width)

total_blocks = m * n
number_of_walls = int(0.35 * total_blocks)
obstacles = set()
for i in range(number_of_walls):
    x = random.randint(0, m - 1)
    y = random.randint(0, n - 1)
    if not ((x == start_x and y == start_y) or (x == end_x and y == end_y)):
        obstacles.add((x, y))

data.generate_graph()
data.print_graph()
data.scan_grid()
data.move_agent()
