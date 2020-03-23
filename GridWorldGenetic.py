import time
import tkinter as tk
import random
import numpy as np

from Graph import Graph


class GridWorld:

    def __init__(self):
        self.height = 700
        self.width = 700
        self.agent = ()
        self.agent_ui = ()
        self.length = 0
        self.possible_moves = ()
        self.agent_padding = 0
        self.dfs_route = []
        self.dfs_best_route = []
        self.final_route_genetic = []
        self.a_star_route = []
        self.a_star_final_route = []
        self.padding = 30
        self.current_estimates = []

        self.m = 5
        self.n = 5
        self.is_visited = [[0] * self.m for temp in range(self.n)]

        self.start_x = 0
        self.start_y = 0
        self.end_x = self.m - 1
        self.end_y = self.n - 1

        # self.start_x = random.randint(0, self.m - 1)
        # self.start_y = random.randint(0, self.n - 1)
        # self.end_x = random.randint(0, self.m - 1)
        # self.end_y = random.randint(0, self.n - 1)

        self.start_key = str(self.start_x) + "," + str(self.start_y)
        self.graph = Graph(self.start_key)

        self.obstacles = set()

        self.color_background = 'snow3'
        self.color_walls = 'black'
        self.color_normal = 'white'
        self.color_visited = 'khaki3'
        self.color_final_path = 'dodger blue'
        self.color_final_path2 = 'khaki1'
        self.COLORS = ['snow', 'ghost white', 'white smoke', 'gainsboro', 'floral white', 'old lace',
                       'linen', 'antique white', 'papaya whip', 'blanched almond', 'bisque', 'peach puff',
                       'navajo white', 'lemon chiffon', 'mint cream', 'azure', 'alice blue', 'lavender',
                       'lavender blush', 'misty rose', 'dark slate gray', 'dim gray', 'slate gray',
                       'light slate gray', 'gray', 'light grey', 'midnight blue', 'navy', 'cornflower blue',
                       'dark slate blue',
                       'slate blue', 'medium slate blue', 'light slate blue', 'medium blue', 'royal blue', 'blue',
                       'dodger blue', 'deep sky blue', 'sky blue', 'light sky blue', 'steel blue', 'light steel blue',
                       'light blue', 'powder blue', 'pale turquoise', 'dark turquoise', 'medium turquoise', 'turquoise',
                       'cyan', 'light cyan', 'cadet blue', 'medium aquamarine', 'aquamarine', 'dark green',
                       'dark olive green',
                       'dark sea green', 'sea green', 'medium sea green', 'light sea green', 'pale green',
                       'spring green',
                       'lawn green', 'medium spring green', 'green yellow', 'lime green', 'yellow green',
                       'forest green', 'olive drab', 'dark khaki', 'khaki', 'pale goldenrod', 'light goldenrod yellow',
                       'light yellow', 'yellow', 'gold', 'light goldenrod', 'goldenrod', 'dark goldenrod', 'rosy brown',
                       'indian red', 'saddle brown', 'sandy brown',
                       'dark salmon', 'salmon', 'light salmon', 'orange', 'dark orange',
                       'coral', 'light coral', 'tomato', 'orange red', 'red', 'hot pink', 'deep pink', 'pink',
                       'light pink',
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
        self.frame = tk.Canvas(bg=self.color_background, height=self.height, width=self.height)
        self.frame.pack()

    def create_grid_ui(self, m, n, start, end, obstacles):
        l1 = (self.width - (2 * self.padding)) / m
        l2 = (self.height - (2 * self.padding)) / n
        length = min(l1, l2)
        self.length = length
        self.agent_padding = 0.1 * length
        for i in range(m):
            for j in range(n):
                color = self.color_normal
                if (i, j) in self.obstacles:
                    color = self.color_walls
                if start == (i, j):
                    color = 'lawn green'
                if end == (i, j):
                    color = 'orange red'
                self.frame.create_rectangle(i * length + self.padding, j * length + self.padding,
                                            i * length + self.padding + length,
                                            j * length + self.padding + length, fill=color)
        self.update_agent_ui((self.start_x, self.start_y))
        self.frame.update()

    def update_agent_ui(self, agent):
        length = self.length
        self.frame.delete(self.agent_ui)
        self.agent = agent
        self.agent_ui = self.frame.create_oval(
            ((length * agent[0]) + self.padding + self.agent_padding,
             (length * agent[1]) + self.padding + self.agent_padding),
            ((length * agent[0]) + length + self.padding - self.agent_padding,
             (length * agent[1]) + length + self.padding - self.agent_padding),
            fill='cyan')
        self.frame.update()

    def move_agent_random_moves(self):
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
                    self.update_agent_ui(self.agent)
            if move == 'west':
                if self.possible_moves[self.agent[0]][self.agent[1]][1]:
                    self.agent = (self.agent[0] - 1, self.agent[1])
                    self.update_agent_ui(self.agent)
            if move == 'north':
                if self.possible_moves[self.agent[0]][self.agent[1]][2]:
                    self.agent = (self.agent[0], self.agent[1] - 1)
                    self.update_agent_ui(self.agent)
            if move == 'south':
                if self.possible_moves[self.agent[0]][self.agent[1]][3]:
                    self.agent = (self.agent[0], self.agent[1] + 1)
                    self.update_agent_ui(self.agent)
        tk.mainloop()

    def scan_grid_and_generate_graph(self):
        self.possible_moves = [[tuple()] * self.m for temp in range(self.n)]
        for i in range(self.m):
            for j in range(self.n):
                if (i, j) not in self.obstacles:
                    east = True
                    west = True
                    north = True
                    south = True
                    if i == 0:
                        west = False
                    if i == self.m - 1:
                        east = False
                    if j == 0:
                        north = False
                    if j == self.n - 1:
                        south = False
                    if (i + 1, j) in self.obstacles:
                        east = False
                    if (i - 1, j) in self.obstacles:
                        west = False
                    if (i, j + 1) in self.obstacles:
                        south = False
                    if (i, j - 1) in self.obstacles:
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
        return graph
        #for k in graph.adjacency_map:
           # print(k + " -> ", end='')
           # for l in graph.adjacency_map[k]:
             #   print(str(l[0]) + "," + str(l[1]) + " : ", end='')


    def get_heuristics(self, x, y):
        # manhattan distance
        x1 = abs(x - self.end_x)
        y1 = abs(y - self.end_y)
        return x1 + y1
        # return -x1 + y1
        # return (x1 + y1) + 2
        # return x1 * x1
        # return (x1 * x1) + (y1 * y1)
        # return 0  # for dijkstra algorithm

    def get_reverse_heuristics(self, x, y):
        # manhattan distance
        x1 = abs(x - self.start_x)
        y1 = abs(y - self.start_y)
        return x1 + y1

    def move_on_given_route(self):
        route = self.dfs_route
        length = self.length
        color_random = random.choice(self.COLORS)
        for r in route:
            time.sleep(0.02)
            self.agent = (r[0], r[1])
            i = r[0]
            j = r[1]
            if not (i == self.start_x and j == self.start_y) and not (i == self.end_x and j == self.end_y):
                self.frame.create_rectangle(i * length + self.padding, j * length + self.padding,
                                            i * length + self.padding + length,
                                            j * length + self.padding + length, fill='purple')  # color_final_path2)
            self.update_agent_ui(self.agent)
        color_random = random.choice(self.COLORS)
        for r in self.dfs_best_route:
            time.sleep(0.01)
            i = r[0]
            j = r[1]
            if not (i == self.start_x and j == self.start_y) and not (i == self.end_x and j == self.end_y):
                self.frame.create_rectangle(i * length + self.padding, j * length + self.padding,
                                            i * length + self.padding + length,
                                            j * length + self.padding + length, fill='orange')
            self.frame.update()

    def move_on_given_route_a_star(self):
        route = self.a_star_route
        length = self.length
        for r in route:
            time.sleep(0.005)
            self.agent = (r[0][0], r[0][1])
            i = r[0][0]
            j = r[0][1]
            if not (i == self.start_x and j == self.start_y) and not (i == self.end_x and j == self.end_y):
                self.frame.create_rectangle(i * length + self.padding, j * length + self.padding,
                                            i * length + self.padding + length,
                                            j * length + self.padding + length, fill=r[1])
            self.update_agent_ui(self.agent)
        for r in self.a_star_final_route:
            time.sleep(0.01)
            i = r[0]
            j = r[1]
            if not (i == self.start_x and j == self.start_y) and not (i == self.end_x and j == self.end_y):
                self.frame.create_rectangle(i * length + self.padding, j * length + self.padding,
                                            i * length + self.padding + length,
                                            j * length + self.padding + length, fill=self.color_final_path)
            self.frame.update()
