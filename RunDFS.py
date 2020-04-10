import random

import Functions
from GridWorld import GridWorld
import tkinter as tk


def dfs(grid_world, key):
    graph = grid_world.graph
    adjacent_nodes = graph.adjacency_map[key]
    x = int(key.split(',')[0])
    y = int(key.split(',')[1])
    if x == grid_world.end_x and y == grid_world.end_y:
        grid_world.dfs_route.append((x, y))
        grid_world.dfs_best_route.append((x, y))
        return -1
    grid_world.is_visited[x][y] = 1
    grid_world.dfs_route.append((x, y))
    for l in adjacent_nodes:
        if grid_world.is_visited[l[0]][l[1]] == 0:
            ret_val = dfs(grid_world, str(l[0]) + "," + str(l[1]))
            if ret_val == -1:
                grid_world.dfs_best_route.append((l[0], l[1]))
                return -1


def random_dfs(grid_world, key):
    graph = grid_world.graph
    adjacent_nodes = graph.adjacency_map[key]
    x = int(key.split(',')[0])
    y = int(key.split(',')[1])
    if x == grid_world.end_x and y == grid_world.end_y:
        grid_world.dfs_route.append((x, y))
        grid_world.dfs_best_route.append((x, y))
        return -1
    grid_world.is_visited[x][y] = 1
    grid_world.dfs_route.append((x, y))
    random.shuffle(adjacent_nodes)
    for l in adjacent_nodes:
        if grid_world.is_visited[l[0]][l[1]] == 0:
            ret_val = random_dfs(grid_world, str(l[0]) + "," + str(l[1]))
            if ret_val == -1:
                grid_world.dfs_best_route.append((l[0], l[1]))
                return -1


def run_dfs(grid_world):
    # dfs(grid_world, grid_world.start_key)
    random_dfs(grid_world, grid_world.start_key)
    grid_world.dfs_best_route.append((grid_world.start_x, grid_world.start_y))
    grid_world.dfs_best_route = grid_world.dfs_best_route[::-1]


grid_world = GridWorld()
Functions.create_obstacles_from_hex(grid_world)
# Functions.create_random_obstacles(grid_world, 0.205)
# Functions.create_fixed_obstacles(grid_world, 6)
grid_world.scan_grid_and_generate_graph()
grid_world.print_graph()
grid_world.create_grid_ui(grid_world.m, grid_world.n, (grid_world.start_x, grid_world.start_y),
                          (grid_world.end_x, grid_world.end_y), grid_world.obstacles)
run_dfs(grid_world)
grid_world.move_on_given_route()
tk.mainloop()
