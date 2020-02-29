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
        self.initial_population = []

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

    # generic function
    def get_random_path(self, start_node, end_node):
        def recursive_function(key):
            graph = self.graph
            adjacent_nodes = graph.adjacency_map[key]
            x = int(key.split(',')[0])
            y = int(key.split(',')[1])
            if x == end_x and y == end_y:
                # inner_route.append((x, y))
                inner_final_route.append((x, y))
                return -1
            self.is_visited[x][y] = 1
            # inner_route.append((x, y))
            random.shuffle(adjacent_nodes)
            for l in adjacent_nodes:
                if self.is_visited[l[0]][l[1]] == 0:
                    ret_val = recursive_function(str(l[0]) + "," + str(l[1]))
                    if ret_val == -1:
                        inner_final_route.append((l[0], l[1]))
                        return -1

        # inner_route = []
        end_x = end_node[0]
        end_y = end_node[1]
        inner_final_route = []
        self.is_visited = [[0] * m for temp in range(n)]
        start_key = str(start_node[0]) + ',' + str(start_node[1])
        recursive_function(start_key)
        return inner_final_route

    def random_dfs(self, key):
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
        random.shuffle(adjacent_nodes)
        for l in adjacent_nodes:
            if self.is_visited[l[0]][l[1]] == 0:
                ret_val = self.random_dfs(str(l[0]) + "," + str(l[1]))
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
        # return -x1 + y1
        # return (x1 + y1) + 2
        # return x1 * x1
        # return (x1 * x1) + (y1 * y1)
        # return 0  # for dijkstra algorithm

    def get_reverse_heuristics(self, x, y):
        # manhattan distance
        x1 = abs(x - start_x)
        y1 = abs(y - start_y)
        return x1 + y1

    def move_on_given_route(self):
        route = self.route
        length = self.length
        color_random = random.choice(COLORS)
        for r in route:
            # time.sleep(0.02)
            self.agent = (r[0], r[1])
            i = r[0]
            j = r[1]
            if not (i == start_x and j == start_y) and not (i == end_x and j == end_y):
                self.frame.create_rectangle(i * length + padding, j * length + padding, i * length + padding + length,
                                            j * length + padding + length, fill='purple')  # color_final_path2)
            self.update_agent(self.agent)
        color_random = random.choice(COLORS)
        for r in self.final_route:
            time.sleep(0.01)
            i = r[0]
            j = r[1]
            if not (i == start_x and j == start_y) and not (i == end_x and j == end_y):
                self.frame.create_rectangle(i * length + padding, j * length + padding, i * length + padding + length,
                                            j * length + padding + length, fill='purple',
                                            stipple="gray50")  # color_final_path)
            self.frame.update()
        # tk.mainloop()

    def move_on_given_route_a_star(self):
        route = self.a_star_route
        length = self.length
        for r in route:
            time.sleep(0.005)
            self.agent = (r[0][0], r[0][1])
            i = r[0][0]
            j = r[0][1]
            if not (i == start_x and j == start_y) and not (i == end_x and j == end_y):
                self.frame.create_rectangle(i * length + padding, j * length + padding, i * length + padding + length,
                                            j * length + padding + length, fill=r[1])
            self.update_agent(self.agent)
        for r in self.a_star_final_route:
            time.sleep(0.01)
            i = r[0]
            j = r[1]
            if not (i == start_x and j == start_y) and not (i == end_x and j == end_y):
                self.frame.create_rectangle(i * length + padding, j * length + padding, i * length + padding + length,
                                            j * length + padding + length, fill=color_final_path)
            self.frame.update()

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
            # time.sleep(0.02)
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

    def crossover(self, population):
        return_list = []
        random.shuffle(population)
        mid = int(len(population) / 2)
        list1 = population[:mid]
        list2 = population[mid:]
        for i in range(min(len(list1), len(list2))):
            path1 = list1[i]
            path2 = list2[i]
            common_nodes = []
            for node in path1:
                if node in path2:
                    common_nodes.append(node)
            if len(common_nodes) > 0:
                random_common_node = random.choice(common_nodes)
                index1 = path1.index(random_common_node)
                index2 = path2.index(random_common_node)
                child1 = path1[:index1]
                child1.extend(path2[index2:])
                child2 = path2[:index2]
                child2.extend(path1[index1:])
                # print(len(common_nodes))
                # print(random_common_node)
                return_list.append(child1)
                return_list.append(child2)
                # print(path1)
                # print(path2)
                # print(child1)
                # print(child2)
                # print()
        return_list.extend(population)
        return return_list

    def mutation(self, population):
        count = len(population)
        mutation_count = 0.3 * count
        sample = random.sample(population, int(mutation_count))
        for list1 in sample:
            random_node = random.choice(list1)
            mutated1 = self.get_random_path((start_x, start_y), random_node)
            mutated2 = self.get_random_path(random_node, (end_x, end_y))
            mutated1.append((start_x, start_y))
            mutated1 = mutated1[::-1]
            mutated1 = mutated1[:-1]
            mutated2 = mutated2[::-1]
            mutated2 = mutated2[:-1]

            mutated1.extend(mutated2)
            population.append(mutated1)
        return population

    def evaluation_function(self, route):
        return len(route)

    def reduce_population(self, population):
        ret_list = []
        freq = {}
        unique_population = set()
        for path in population:
            unique_population.add(tuple(path))
        population = list(unique_population)
        for i in range(len(population)):
            freq[i] = len(population[i])
        for k, v in sorted(freq.items(), key=lambda f: f[1]):
            ret_list.append(list(population[k]))
        ret_list = ret_list[:starting_population]
        return ret_list


color_background = 'snow3'
color_walls = 'black'
color_normal = 'white'
color_visited = 'khaki3'
color_final_path = 'dodger blue'
color_final_path2 = 'khaki1'
COLORS = ['snow', 'ghost white', 'white smoke', 'gainsboro', 'floral white', 'old lace',
          'linen', 'antique white', 'papaya whip', 'blanched almond', 'bisque', 'peach puff',
          'navajo white', 'lemon chiffon', 'mint cream', 'azure', 'alice blue', 'lavender',
          'lavender blush', 'misty rose', 'dark slate gray', 'dim gray', 'slate gray',
          'light slate gray', 'gray', 'light grey', 'midnight blue', 'navy', 'cornflower blue', 'dark slate blue',
          'slate blue', 'medium slate blue', 'light slate blue', 'medium blue', 'royal blue', 'blue',
          'dodger blue', 'deep sky blue', 'sky blue', 'light sky blue', 'steel blue', 'light steel blue',
          'light blue', 'powder blue', 'pale turquoise', 'dark turquoise', 'medium turquoise', 'turquoise',
          'cyan', 'light cyan', 'cadet blue', 'medium aquamarine', 'aquamarine', 'dark green', 'dark olive green',
          'dark sea green', 'sea green', 'medium sea green', 'light sea green', 'pale green', 'spring green',
          'lawn green', 'medium spring green', 'green yellow', 'lime green', 'yellow green',
          'forest green', 'olive drab', 'dark khaki', 'khaki', 'pale goldenrod', 'light goldenrod yellow',
          'light yellow', 'yellow', 'gold', 'light goldenrod', 'goldenrod', 'dark goldenrod', 'rosy brown',
          'indian red', 'saddle brown', 'sandy brown',
          'dark salmon', 'salmon', 'light salmon', 'orange', 'dark orange',
          'coral', 'light coral', 'tomato', 'orange red', 'red', 'hot pink', 'deep pink', 'pink', 'light pink',
          'pale violet red', 'maroon', 'medium violet red', 'violet red',
          'medium orchid', 'dark orchid', 'dark violet', 'blue violet', 'purple', 'medium purple',
          'thistle', 'snow2', 'snow3',
          'snow4', 'seashell2', 'seashell3', 'seashell4', 'AntiqueWhite1', 'AntiqueWhite2',
          'AntiqueWhite3', 'AntiqueWhite4', 'bisque2', 'bisque3', 'bisque4', 'PeachPuff2',
          'PeachPuff3', 'PeachPuff4', 'NavajoWhite2', 'NavajoWhite3', 'NavajoWhite4',
          'LemonChiffon2', 'LemonChiffon3', 'LemonChiffon4', 'cornsilk2', 'cornsilk3',
          'cornsilk4', 'ivory2', 'ivory3', 'ivory4', 'honeydew2', 'honeydew3', 'honeydew4',
          'LavenderBlush2', 'LavenderBlush3', 'LavenderBlush4', 'MistyRose2', 'MistyRose3',
          'MistyRose4', 'azure2', 'azure3', 'azure4', 'SlateBlue1', 'SlateBlue2', 'SlateBlue3',
          'SlateBlue4', 'RoyalBlue1', 'RoyalBlue2', 'RoyalBlue3', 'RoyalBlue4', 'blue2', 'blue4',
          'DodgerBlue2', 'DodgerBlue3', 'DodgerBlue4', 'SteelBlue1', 'SteelBlue2',
          'SteelBlue3', 'SteelBlue4', 'DeepSkyBlue2', 'DeepSkyBlue3', 'DeepSkyBlue4',
          'SkyBlue1', 'SkyBlue2', 'SkyBlue3', 'SkyBlue4', 'LightSkyBlue1', 'LightSkyBlue2',
          'LightSkyBlue3', 'LightSkyBlue4', 'SlateGray1', 'SlateGray2', 'SlateGray3',
          'SlateGray4', 'LightSteelBlue1', 'LightSteelBlue2', 'LightSteelBlue3',
          'LightSteelBlue4', 'LightBlue1', 'LightBlue2', 'LightBlue3', 'LightBlue4',
          'LightCyan2', 'LightCyan3', 'LightCyan4', 'PaleTurquoise1', 'PaleTurquoise2',
          'PaleTurquoise3', 'PaleTurquoise4', 'CadetBlue1', 'CadetBlue2', 'CadetBlue3',
          'CadetBlue4', 'turquoise1', 'turquoise2', 'turquoise3', 'turquoise4', 'cyan2', 'cyan3',
          'cyan4', 'DarkSlateGray1', 'DarkSlateGray2', 'DarkSlateGray3', 'DarkSlateGray4',
          'aquamarine2', 'aquamarine4', 'DarkSeaGreen1', 'DarkSeaGreen2', 'DarkSeaGreen3',
          'DarkSeaGreen4', 'SeaGreen1', 'SeaGreen2', 'SeaGreen3', 'PaleGreen1', 'PaleGreen2',
          'PaleGreen3', 'PaleGreen4', 'SpringGreen2', 'SpringGreen3', 'SpringGreen4',
          'green2', 'green3', 'green4', 'chartreuse2', 'chartreuse3', 'chartreuse4',
          'OliveDrab1', 'OliveDrab2', 'OliveDrab4', 'DarkOliveGreen1', 'DarkOliveGreen2',
          'DarkOliveGreen3', 'DarkOliveGreen4', 'khaki1', 'khaki2', 'khaki3', 'khaki4',
          'LightGoldenrod1', 'LightGoldenrod2', 'LightGoldenrod3', 'LightGoldenrod4',
          'LightYellow2', 'LightYellow3', 'LightYellow4', 'yellow2', 'yellow3', 'yellow4',
          'gold2', 'gold3', 'gold4', 'goldenrod1', 'goldenrod2', 'goldenrod3', 'goldenrod4',
          'DarkGoldenrod1', 'DarkGoldenrod2', 'DarkGoldenrod3', 'DarkGoldenrod4',
          'RosyBrown1', 'RosyBrown2', 'RosyBrown3', 'RosyBrown4', 'IndianRed1', 'IndianRed2',
          'IndianRed3', 'IndianRed4', 'sienna1', 'sienna2', 'sienna3', 'sienna4', 'burlywood1',
          'burlywood2', 'burlywood3', 'burlywood4', 'wheat1', 'wheat2', 'wheat3', 'wheat4', 'tan1',
          'tan2', 'tan4', 'chocolate1', 'chocolate2', 'chocolate3', 'firebrick1', 'firebrick2',
          'firebrick3', 'firebrick4', 'brown1', 'brown2', 'brown3', 'brown4', 'salmon1', 'salmon2',
          'salmon3', 'salmon4', 'LightSalmon2', 'LightSalmon3', 'LightSalmon4', 'orange2',
          'orange3', 'orange4', 'DarkOrange1', 'DarkOrange2', 'DarkOrange3', 'DarkOrange4',
          'coral1', 'coral2', 'coral3', 'coral4', 'tomato2', 'tomato3', 'tomato4', 'OrangeRed2',
          'OrangeRed3', 'OrangeRed4', 'red2', 'red3', 'red4', 'DeepPink2', 'DeepPink3', 'DeepPink4',
          'HotPink1', 'HotPink2', 'HotPink3', 'HotPink4', 'pink1', 'pink2', 'pink3', 'pink4',
          'LightPink1', 'LightPink2', 'LightPink3', 'LightPink4', 'PaleVioletRed1',
          'PaleVioletRed2', 'PaleVioletRed3', 'PaleVioletRed4', 'maroon1', 'maroon2',
          'maroon3', 'maroon4', 'VioletRed1', 'VioletRed2', 'VioletRed3', 'VioletRed4',
          'magenta2', 'magenta3', 'magenta4', 'orchid1', 'orchid2', 'orchid3', 'orchid4', 'plum1',
          'plum2', 'plum3', 'plum4', 'MediumOrchid1', 'MediumOrchid2', 'MediumOrchid3',
          'MediumOrchid4', 'DarkOrchid1', 'DarkOrchid2', 'DarkOrchid3', 'DarkOrchid4',
          'purple1', 'purple2', 'purple3', 'purple4', 'MediumPurple1', 'MediumPurple2',
          'MediumPurple3', 'MediumPurple4', 'thistle1', 'thistle2', 'thistle3', 'thistle4',
          'gray1', 'gray2', 'gray3', 'gray4', 'gray5', 'gray6', 'gray7', 'gray8', 'gray9', 'gray10',
          'gray11', 'gray12', 'gray13', 'gray14', 'gray15', 'gray16', 'gray17', 'gray18', 'gray19',
          'gray20', 'gray21', 'gray22', 'gray23', 'gray24', 'gray25', 'gray26', 'gray27', 'gray28',
          'gray29', 'gray30', 'gray31', 'gray32', 'gray33', 'gray34', 'gray35', 'gray36', 'gray37',
          'gray38', 'gray39', 'gray40', 'gray42', 'gray43', 'gray44', 'gray45', 'gray46', 'gray47',
          'gray48', 'gray49', 'gray50', 'gray51', 'gray52', 'gray53', 'gray54', 'gray55', 'gray56',
          'gray57', 'gray58', 'gray59', 'gray60', 'gray61', 'gray62', 'gray63', 'gray64', 'gray65',
          'gray66', 'gray67', 'gray68', 'gray69', 'gray70', 'gray71', 'gray72', 'gray73', 'gray74',
          'gray75', 'gray76', 'gray77', 'gray78', 'gray79', 'gray80', 'gray81', 'gray82', 'gray83',
          'gray84', 'gray85', 'gray86', 'gray87', 'gray88', 'gray89', 'gray90', 'gray91', 'gray92',
          'gray93', 'gray94', 'gray95', 'gray97', 'gray98', 'gray99']

m = 30
n = 30

start_x = 0
start_y = 0
end_x = m - 1
end_y = n - 1

# start_x = random.randint(0, m - 1)
# start_y = random.randint(0, n - 1)
# end_x = random.randint(0, m - 1)
# end_y = random.randint(0, n - 1)


start_key = str(start_x) + "," + str(start_y)

height = 700
width = 700

data = GridWorld(height, width, m, n)

padding = data.padding

obstacles = set()

'''Random obstacles'''
total_blocks = m * n
number_of_walls = int(0.05 * total_blocks)
for i in range(number_of_walls):
    x = random.randint(0, m - 1)
    y = random.randint(0, n - 1)
    if not ((x == start_x and y == start_y) or (x == end_x and y == end_y)):
        obstacles.add((x, y))

'''Specific obstacles'''
distance_between_walls = 6
for i in range(1, m - 1):
    for j in range(n - 1):
        if j % distance_between_walls == 0:
            obstacles.add((i, j))
            if j % (2 * distance_between_walls) != 0:
                obstacles.add((0, j))
        if j % (2 * distance_between_walls) == 0:
            obstacles.add((m - 1, j))

# data.create_grid(m, n, (start_x, start_y), (end_x, end_y), obstacles)
# tk.mainloop()
# exit()

'''START essential for grid creation'''
data.scan_grid_and_generate_graph()
# data.print_graph()
# data.create_grid(m, n, (start_x, start_y), (end_x, end_y), obstacles)
'''END'''

# below code for dfs and a-star #
'''
data.random_dfs(start_key)
data.final_route.append((start_x, start_y))
data.final_route = data.final_route[::-1]
'''

path = data.a_star()
if path is not None:
    data.a_star_final_route = path

# data.create_grid(m, n, (start_x, start_y), (end_x, end_y), obstacles)
# data.move_on_given_route_a_star()
# data.combine_move()
# data.move_agent()

''' genetic below this line '''
starting_population = 50
# for i in range(starting_population):
#     data.route = []
#     data.final_route = []
#     data.is_visited = [[0] * m for temp in range(n)]
#     data.random_dfs(start_key)
#     data.final_route.append((start_x, start_y))
#     data.final_route = data.final_route[::-1]
#     print(data.final_route[:-1])
#     data.initial_population.append(data.final_route[:-1])
#     if len(data.final_route[:-1]) == 0:
#         exit()
#
# population = data.initial_population
# data.is_visited = [[0] * m for temp in range(n)]
# print()
# best_path = []
# best_score = math.inf
# for i in range(100):  # iterations
#     # print('#', len(population))
#     population = data.crossover(population)
#     # print('#', len(population))
#     population = data.reduce_population(population)
#     # print('#', len(population))
#     population = data.mutation(population)
#     # print('#', len(population))
#     avg = 0
#     for path in population:
#         avg += len(path)
#     if len(population[0]) < best_score:
#         best_score = len(population[0])
#         best_path = population[0]
#     print(i, '>', len(population[0]))
#
# print()
# print('A*     :', len(data.a_star_final_route), data.a_star_final_route[0], data.a_star_final_route[-1])
# print('Genetic:', best_score, best_path[0], best_path[-1])

data.create_grid(m, n, (start_x, start_y), (end_x, end_y), obstacles)
data.route = []
# data.final_route = best_path
data.move_on_given_route_a_star()
data.move_on_given_route()
tk.mainloop()
