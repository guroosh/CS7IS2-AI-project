import random

from numpy import sort

import Functions
from GridWorld import GridWorld
import tkinter as tk


def sort_by_probabilities(x, y, adjacent_nodes, grid_world):
    print(x, y, adjacent_nodes)
    den = 0
    new_list = []
    for n in adjacent_nodes:
        move = str(x) + ',' + str(y) + '->' + str(n[0]) + ',' + str(n[1])
        pheromone = pheromone_table[move]
        print("pheromone", pheromone, end=', ')
        if (grid_world.end_x, grid_world.end_y) in adjacent_nodes:
            if (n[0], n[1]) == (grid_world.end_x, grid_world.end_y):
                tau = 1
            else:
                tau = 2
        else:
            tau = 1 / grid_world.get_heuristics(n[0], n[1])
        print("tau", tau)
        # tau = 1
        den += ((tau ** alpha) * (pheromone ** beta))
    for n in adjacent_nodes:
        move = str(x) + ',' + str(y) + '->' + str(n[0]) + ',' + str(n[1])
        pheromone = pheromone_table[move]
        if (grid_world.end_x, grid_world.end_y) in adjacent_nodes:
            if (n[0], n[1]) == (grid_world.end_x, grid_world.end_y):
                tau = 1
            else:
                tau = 2
        else:
            tau = 1 / grid_world.get_heuristics(n[0], n[1])
        # tau = 1
        prob = ((tau ** alpha) * (pheromone ** beta)) / den
        new_list.append((n, prob))
        new_list.sort(key=lambda tup: tup[1], reverse=True)
    print(new_list)
    print()
    return new_list


def iterate_ants(grid_world, key):
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
    adjacent_nodes = sort_by_probabilities(x, y, adjacent_nodes, grid_world)
    # random.shuffle(adjacent_nodes)
    for l1 in adjacent_nodes:
        l = l1[0]
        if grid_world.is_visited[l[0]][l[1]] == 0:
            ret_val = iterate_ants(grid_world, str(l[0]) + "," + str(l[1]))
            if ret_val == -1:
                grid_world.dfs_best_route.append((l[0], l[1]))
                return -1


def update_pheromone(paths):
    pass


def evaportion(paths):
    pass


def get_best_path(best_path, paths):
    return []


def run_aco(grid_world):
    best_path = []
    all_paths = iterate_ants(grid_world, grid_world.start_key)
    update_pheromone(all_paths)
    evaportion(all_paths)
    best_path = get_best_path(best_path, all_paths)


grid_world = GridWorld()
Functions.create_random_obstacles(grid_world, 0.205)
# Functions.create_fixed_obstacles(grid_world, 6)
grid_world.scan_grid_and_generate_graph()
grid_world.print_graph()


def init_pheromone(grid_world):
    graph = grid_world.graph
    for k in graph.adjacency_map:
        for l in graph.adjacency_map[k]:
            pheromone_table[k + '->' + str(l[0]) + "," + str(l[1])] = 1


pheromone_table = dict()
init_pheromone(grid_world)

alpha = 1
beta = 1

run_aco(grid_world)

grid_world.create_grid_ui(grid_world.m, grid_world.n, (grid_world.start_x, grid_world.start_y),
                          (grid_world.end_x, grid_world.end_y), grid_world.obstacles)
grid_world.move_on_given_route()
tk.mainloop()
