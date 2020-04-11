import math
import random

import Functions
from GridWorld import GridWorld
import tkinter as tk


def randomize_list(new_list, max_tau, min_tau, max_pheromone, min_pheromone):
    den = 0
    if max_pheromone == min_pheromone:
        max_pheromone = 1
        min_pheromone = 0
    if max_tau == min_tau:
        max_tau = 1
        min_tau = 0
    for t in new_list:
        pheromone = (1 + ((t[2] - min_pheromone) / (max_pheromone - min_pheromone)))
        # print(pheromone)
        tau = (1 + ((t[1] - min_tau) / (max_tau - min_tau))) * 100
        # print("tau, pheromone: ", pheromone)
        den += ((pheromone ** beta) * (tau ** alpha))
    prob_check = 0
    temp_list = []
    for t in new_list:
        pheromone = (1 + ((t[2] - min_pheromone) / (max_pheromone - min_pheromone)))
        tau = (1 + ((t[1] - min_tau) / (max_tau - min_tau))) * 100
        prob = ((pheromone ** beta) * (tau ** alpha)) / den
        prob_check += prob
        temp_list.append((t[0], prob))
    ret_list = []

    '''testing code START'''
    # temp_list.sort(key=lambda v: v[1], reverse=True)
    # ret_list = temp_list[:]
    '''END'''

    long_list_of_100_possibilities = random.choices(population=temp_list,
                                                    weights=[i[1] for i in temp_list], k=10)

    '''These 2 for loops can be optimised, by using breaks'''
    for l2 in long_list_of_100_possibilities:
        if l2 not in ret_list:
            ret_list.append(l2)
    random.shuffle(temp_list)
    for t in temp_list:
        if t not in ret_list:
            ret_list.append(t)

    # print(min_pheromone, max_pheromone)
    # print(new_list)
    # print(temp_list)
    # print(ret_list)
    # print()
    # print('PRINT PRINT: ', prob_check)
    return ret_list


def randomize_again(new_list):
    r1 = random.randint(0, 1)
    if r1 == 0:
        return new_list
    else:
        try:
            new_list[0], new_list[1] = new_list[1], new_list[0]
        except IndexError:
            pass
        r2 = random.randint(0, 1)
        if r2 == 0:
            return new_list
        else:
            try:
                new_list[0], new_list[2] = new_list[2], new_list[0]
            except IndexError:
                pass
            r3 = random.randint(0, 1)
            if r3 == 0:
                return new_list
            else:
                try:
                    new_list[0], new_list[3] = new_list[3], new_list[0]
                except IndexError:
                    pass
                return new_list


def sort_by_probabilities(adjacent_nodes, grid_world):
    # init
    new_list = []
    max_tau = float('-inf')
    max_pheromone = float("-inf")
    min_tau = float("inf")
    min_pheromone = float("inf")

    for n in adjacent_nodes:
        node = str(n[0]) + ',' + str(n[1])
        pheromone = pheromone_table[node]
        # if (grid_world.end_x, grid_world.end_y) in adjacent_nodes:
        #     if (n[0], n[1]) == (grid_world.end_x, grid_world.end_y):
        #         tau = 1
        #     else:
        #         tau = 1 / 2
        # else:
        #     tau = 1 / grid_world.get_heuristics(n[0], n[1])
        tau = grid_world.get_reverse_heuristics(n[0], n[1])
        # tau = 1
        max_tau = max(max_tau, tau)
        max_pheromone = max(max_pheromone, pheromone)
        min_tau = min(min_tau, tau)
        min_pheromone = min(min_pheromone, pheromone)
        new_list.append((n, tau, pheromone))

    # random.shuffle(new_list)
    # print(new_list)
    new_list = randomize_list(new_list, max_tau, min_tau, max_pheromone, min_pheromone)
    # new_list = randomize_again(new_list)
    # print(new_list)
    # print()
    return new_list


def iterate_ants(grid_world, key):
    graph = grid_world.graph
    adjacent_nodes = graph.adjacency_map[key]
    x = int(key.split(',')[0])
    y = int(key.split(',')[1])

    if x == grid_world.end_x and y == grid_world.end_y:
        grid_world.aco_current_route.append((x, y))
        return -1

    grid_world.is_visited[x][y] = 1
    adjacent_nodes = sort_by_probabilities(adjacent_nodes, grid_world)
    for l1 in adjacent_nodes:
        l2 = l1[0]
        if grid_world.is_visited[l2[0]][l2[1]] == 0:
            ret_val = iterate_ants(grid_world, str(l2[0]) + "," + str(l2[1]))
            if ret_val == -1:
                grid_world.aco_current_route.append((l2[0], l2[1]))
                return -1


def update_pheromone(paths):
    for p in paths:
        current_len = len(p)
        for node in p:
            pheromone_table[str(node[0]) + ',' + str(node[1])] += (1 / current_len) + 100


def p_table_print():
    for k in pheromone_table:
        print(k + " : " + str(pheromone_table[k]))


def evaporation():
    # note: if (* 0.7) means 70% is retained and 30% is evaporated
    for k in pheromone_table:
        pheromone_table[k] = pheromone_table[k] * 0.9


def get_current_best_path(all_paths):
    current_best_path = []
    for p in all_paths:
        if not current_best_path:
            current_best_path = p
        if len(current_best_path) > len(p):
            current_best_path = p
    return current_best_path


def get_best_path(best_path, current_best_path):
    if not best_path:
        return current_best_path
    if len(best_path) < len(current_best_path):
        return best_path
    else:
        return current_best_path


def init_pheromone(grid_world):
    graph = grid_world.graph
    for k in graph.adjacency_map:
        pheromone_table[k] = 0


def remove_redundancy(route):
    return route


def run_aco(grid_world):
    best_path = []
    for i in range(30):
        all_paths = []
        for j in range(20):
            iterate_ants(grid_world, grid_world.start_key)
            grid_world.aco_current_route.append((grid_world.start_x, grid_world.start_y))
            grid_world.aco_current_route = grid_world.aco_current_route[::-1]
            grid_world.aco_current_route = grid_world.aco_current_route[:-1]
            all_paths.append(grid_world.aco_current_route)
            grid_world.aco_current_route = []
            grid_world.is_visited = [[0] * grid_world.n for temp in range(grid_world.m)]
        current_best_path = get_current_best_path(all_paths)
        update_pheromone(all_paths)
        evaporation()
        best_path = get_best_path(best_path, current_best_path)
        print(i, len(best_path), len(current_best_path))
        if len(best_path) == 0:
            return
        grid_world.aco_best_route = best_path


grid_world = GridWorld(40, 40)
# Functions.create_grid_from_hex(grid_world)
Functions.create_random_obstacles(grid_world, 0.105)
# Functions.create_fixed_obstacles(grid_world, 6)
grid_world.scan_grid_and_generate_graph()
grid_world.print_graph()
grid_world.save_graph()

pheromone_table = dict()
init_pheromone(grid_world)

alpha = 2
beta = 5

run_aco(grid_world)

print(grid_world.aco_best_route)

grid_world.create_grid_ui(grid_world.m, grid_world.n, (grid_world.start_x, grid_world.start_y),
                          (grid_world.end_x, grid_world.end_y), grid_world.obstacles)

grid_world.move_on_given_route_aco(0)

# print_pheromone_table()
tk.mainloop()
