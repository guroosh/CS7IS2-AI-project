import math
import time
import tkinter as tk
import random
import numpy as np

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
        self.final_route = []
        self.a_star_route = []
        self.a_star_final_route = []
        self.padding = 30
        self.current_estimates = []

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
                    color = 'lawn green'
                if end == (i, j):
                    color = 'orange red'
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

    def dfs(self, key):
        graph = self.graph
        adjacent_nodes = graph.adjacency_map[key]
        x = int(key.split(',')[0])
        y = int(key.split(',')[1])
        if x == end_x and y == end_y:
            self.route.append((x, y))
            self.final_route.append((x, y))
            return -1
        self.is_visited[x][y] = 1
        self.route.append((x, y))
        for l in adjacent_nodes:
            if self.is_visited[l[0]][l[1]] == 0:
                ret_val = self.dfs(str(l[0]) + "," + str(l[1]))
                if ret_val == -1:
                    self.final_route.append((l[0], l[1]))
                    return -1

    def a_star(self):
        def get_final_path(parent, current):
            total_path = [current]
            while parent[current[0]][current[1]] is not None:
                current = parent[current[0]][current[1]]
                # print(current)
                total_path.append(current)
            return total_path[::-1]

        def get_best_node(open_set, f_score):
            min_val = math.inf
            min_node = None
            for node in open_set:
                current_val = f_score[node[0]][node[1]]
                if current_val < min_val:
                    min_val = current_val
                    min_node = node
            return min_node

        open_set = set()
        open_set.add((start_x, start_y))
        parent = [[None] * m for temp in range(n)]
        g_score = [[math.inf] * m for temp in range(n)]
        g_score[start_x][start_y] = 0
        f_score = [[math.inf] * m for temp in range(n)]
        f_score[start_x][start_y] = self.get_heuristics(start_x, start_y)

        while open_set:
            current = get_best_node(open_set, f_score)
            self.a_star_route.append((current, color_visited))
            if current == (end_x, end_y):
                return get_final_path(parent, current)
            # print(open_set)
            # print(current)
            open_set.remove((current[0], current[1]))
            self.a_star_route.append((current, color_final_path2))

            # print(open_set)
            for neighbor in self.graph.adjacency_map[str(current[0]) + "," + str(current[1])]:
                new_g_score = g_score[current[0]][current[1]] + 1
                if new_g_score < g_score[neighbor[0]][neighbor[1]]:
                    parent[neighbor[0]][neighbor[1]] = current
                    g_score[neighbor[0]][neighbor[1]] = new_g_score
                    f_score[neighbor[0]][neighbor[1]] = g_score[neighbor[0]][neighbor[1]] + self.get_heuristics(
                        neighbor[0], neighbor[1])
                    if neighbor not in open_set:
                        open_set.add(neighbor)
                        self.a_star_route.append((neighbor, color_visited))
        return None

    def get_heuristics(self, x, y):
        # manhattan distance
        x1 = abs(x - end_x)
        y1 = abs(y - end_y)
        return x1 + y1
        # return 0, for dijkstra algorithm

    def get_reverse_heuristics(self, x, y):
        # manhattan distance
        x1 = abs(x - start_x)
        y1 = abs(y - start_y)
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
                                            j * length + padding + length, fill=color_final_path2)
            self.update_agent(self.agent)
        for r in self.final_route:
            time.sleep(0.02)
            i = r[0]
            j = r[1]
            if not (i == start_x and j == start_y) and not (i == end_x and j == end_y):
                self.frame.create_rectangle(i * length + padding, j * length + padding, i * length + padding + length,
                                            j * length + padding + length, fill=color_final_path)
            self.frame.update()
        tk.mainloop()

    def move_on_given_route_a_star(self):
        route = self.a_star_route
        length = self.length
        for r in route:
            time.sleep(0.02)
            self.agent = (r[0][0], r[0][1])
            i = r[0][0]
            j = r[0][1]
            if not (i == start_x and j == start_y) and not (i == end_x and j == end_y):
                self.frame.create_rectangle(i * length + padding, j * length + padding, i * length + padding + length,
                                            j * length + padding + length, fill=r[1])
            self.update_agent(self.agent)
        for r in self.a_star_final_route:
            time.sleep(0.02)
            i = r[0]
            j = r[1]
            if not (i == start_x and j == start_y) and not (i == end_x and j == end_y):
                self.frame.create_rectangle(i * length + padding, j * length + padding, i * length + padding + length,
                                            j * length + padding + length, fill=color_final_path)
            self.frame.update()
        tk.mainloop()

    def combine_move(self):
        route = self.route
        length = self.length
        for r in route:
            time.sleep(0.02)
            self.agent = (r[0], r[1])
            i = r[0]
            j = r[1]
            if not (i == start_x and j == start_y) and not (i == end_x and j == end_y):
                self.frame.create_rectangle(i * length + padding, j * length + padding, i * length + padding + length,
                                            j * length + padding + length, fill='LightPink1')
            self.update_agent(self.agent)
        for r in self.final_route:
            time.sleep(0.02)
            i = r[0]
            j = r[1]
            if not (i == start_x and j == start_y) and not (i == end_x and j == end_y):
                self.frame.create_rectangle(i * length + padding, j * length + padding, i * length + padding + length,
                                            j * length + padding + length, fill='maroon1')
            self.frame.update()

        route = self.a_star_route
        length = self.length
        for r in route:
            time.sleep(0.02)
            self.agent = (r[0][0], r[0][1])
            i = r[0][0]
            j = r[0][1]
            if not (i == start_x and j == start_y) and not (i == end_x and j == end_y):
                self.frame.create_rectangle(i * length + padding, j * length + padding, i * length + padding + length,
                                            j * length + padding + length, fill=r[1])
            self.update_agent(self.agent)
        for r in self.a_star_final_route:
            time.sleep(0.02)
            i = r[0]
            j = r[1]
            if not (i == start_x and j == start_y) and not (i == end_x and j == end_y):
                self.frame.create_rectangle(i * length + padding, j * length + padding, i * length + padding + length,
                                            j * length + padding + length, fill=color_final_path)
            self.frame.update()
        tk.mainloop()


color_background = 'snow3'
color_walls = 'black'
color_normal = 'white'
color_visited = 'khaki3'
color_final_path = 'dodger blue'
color_final_path2 = 'khaki1'

m = 30
n = 30

start_x = 7
start_y = 7
end_x = m - 1
end_y = n - 1
start_key = str(start_x) + "," + str(start_y)

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
# data.print_graph()
data.create_grid(m, n, (start_x, start_y), (end_x, end_y), obstacles)
data.dfs(start_key)
data.final_route = data.final_route[::-1]
# data.move_on_given_route()

path = data.a_star()
if path is not None:
    data.a_star_final_route = path
# data.create_grid(m, n, (start_x, start_y), (end_x, end_y), obstacles)
# data.move_on_given_route_a_star()
data.combine_move()
# data.move_agent()
