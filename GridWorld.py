import time
import tkinter as tk
import random
import numpy as np
import bisect

from Graph import Graph


class GridWorld:

    def __init__(self, height, width, m, n):
        self.height = height
        self.width = width
        self.frame = tk.Canvas(bg=color_background, height=height, width=height)
        self.frame.pack()
        self.agent = ()
        self.agent_ui = ()
        self.length = 0
        self.possible_moves = ()
        self.graph = Graph(str(start_x) + ',' + str(start_y))
        self.agent_padding = 0
        self.is_visited = [[0] * m for temp in range(n)]
        self.route = []
        self.padding = 30

    def create_grid(self, m, n, start, end, obstacles):
        l1 = (self.width - (2 * padding)) / m
        l2 = (self.height - (2 * padding)) / n
        length = min(l1, l2)
        self.length = length
        self.agent_padding = 0.1 * length
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
            ((length * agent[0]) + padding + self.agent_padding,
             (length * agent[1]) + padding + self.agent_padding),
            ((length * agent[0]) + length + padding - self.agent_padding,
             (length * agent[1]) + length + padding - self.agent_padding),
            fill='cyan')
        self.frame.update()

    def move_agent(self):
        directions = ['east', 'west', 'north', 'south']
        for i in range(1000):
            time.sleep(0.2)
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

    def scan_grid_and_generate_graph(self):
        self.possible_moves = [[tuple()] * m for temp in range(n)]
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
                    self.possible_moves[i][j] = (east, west, north, south)
                    self.graph.adjacency_map[str(i) + ',' + str(j)] = []
                    if east:
                        self.graph.adjacency_map[str(i) + ',' + str(j)].append((i + 1, j))
                    if west:
                        self.graph.adjacency_map[str(i) + ',' + str(j)].append((i - 1, j))
                    if north:
                        self.graph.adjacency_map[str(i) + ',' + str(j)].append((i, j - 1))
                    if south:
                        self.graph.adjacency_map[str(i) + ',' + str(j)].append((i, j + 1))

    def print_graph(self):
        graph = self.graph
        for k in graph.adjacency_map:
            print(k + " -> ", end='')
            for l in graph.adjacency_map[k]:
                print(str(l[0]) + "," + str(l[1]) + " : ", end='')
            print()

    def dfs(self, this, key):
        graph = self.graph
        adjacent_nodes = graph.adjacency_map[key]
        x = int(key.split(',')[0])
        y = int(key.split(',')[1])
        if x == end_x and y == end_y:
            self.route.append((x, y))
            return -1
        self.is_visited[x][y] = 1
        self.route.append((x, y))
        for l in adjacent_nodes:
            # print('42', self.is_visited[l[0]][l[1]])
            if self.is_visited[l[0]][l[1]] == 0:
                # print('43', str(l[0]) + "," + str(l[1]))
                ret_val = this.dfs(this, str(l[0]) + "," + str(l[1]))
                if ret_val == -1:
                    return -1

    def a_star(self, this, key, current_cost):
        graph = self.graph
        adjacent_nodes = graph.adjacency_map[key]
        x = int(key.split(',')[0])
        y = int(key.split(',')[1])
        if x == end_x and y == end_y:
            self.route.append((x, y))
            return -1
        self.is_visited[x][y] = 1
        self.route.append((x, y))
        estimation_list = []
        for l in adjacent_nodes:
            estimated_cost = self.get_heuristics(l[0], l[1]) + current_cost
            estimation_list.append((l[0], l[1], estimated_cost))
        estimation_list.sort(key=lambda tup: tup[2])
        for tup in estimation_list:
            if self.is_visited[tup[0]][tup[1]] == 0:
                ret_val = this.a_star(this, str(tup[0]) + "," + str(tup[1]), current_cost + 1)
                if ret_val == -1:
                    return -1

    def get_heuristics(self, x, y):
        # manhattan distance
        x1 = abs(x - end_x)
        y1 = abs(y - end_y)
        return x1 + y1

    def move_on_given_route(self):
        route = self.route
        length = self.length
        for r in route:
            time.sleep(0.02)
            self.agent = (r[0], r[1])
            i = r[0]
            j = r[1]
            if not (i == start_x and j == start_y) and not (i == end_x and j == end_y):
                self.frame.create_rectangle(i * length + padding, j * length + padding, i * length + padding + length,
                                            j * length + padding + length, fill=color_visited)
            self.update_agent(self.agent)
        tk.mainloop()


color_background = 'snow3'
color_walls = 'black'
color_normal = 'white'
color_visited = 'gold'

m = 30
n = 30

start_x = 0
start_y = 0
end_x = m - 1
end_y = n - 1

height = 700
width = 700

data = GridWorld(height, width, m, n)

padding = data.padding

total_blocks = m * n
number_of_walls = int(0.3 * total_blocks)
obstacles = set()
for i in range(number_of_walls):
    x = random.randint(0, m - 1)
    y = random.randint(0, n - 1)
    if not ((x == start_x and y == start_y) or (x == end_x and y == end_y)):
        obstacles.add((x, y))

data.scan_grid_and_generate_graph()
data.print_graph()
data.dfs(data, '0,0')
# data.a_star(data, '0,0', 0)
data.create_grid(m, n, (start_x, start_y), (end_x, end_y), obstacles)
data.move_on_given_route()
# data.move_agent()
