import random
import FunctionsGenetic
from GridWorldGenetic import GridWorld
import tkinter as tk


def get_random_path(self, start_node, end_node, graph):
    def recursive_function(key):
        adjacent_nodes = graph.adjacency_map[key]
        x = int(key.split(',')[0])
        y = int(key.split(',')[1])
        if x == end_x and y == end_y:
            return -1
        self.is_visited[x][y] = 1
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
    self.is_visited = [[0] * self.m for temp in range(self.n)]
    start_key = str(start_node[0]) + ',' + str(start_node[1])
    recursive_function(start_key)
    return inner_final_route


class Genetic(object):
    def __init__(self):
        self.m = 5
        self.n = 5

    def run(self, graph):
        path=[]
        i=1
        iteration=21
        for i in range(iteration):
            paths=get_random_path(self, [0,0], [4,4], graph)
            path.append(paths)
        return path


grid_world = GridWorld()
FunctionsGenetic.create_random_obstacles(grid_world, 0.05)
FunctionsGenetic.create_fixed_obstacles(grid_world, 6)
grid_world.scan_grid_and_generate_graph()
graph = grid_world.print_graph()
grid_world.create_grid_ui(grid_world.m, grid_world.n, (grid_world.start_x, grid_world.start_y),
                          (grid_world.end_x, grid_world.end_y), grid_world.obstacles)


#Population paths list
path = Genetic().run(graph)
