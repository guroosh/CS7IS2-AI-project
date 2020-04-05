import math
import random

import tkinter as tk

import Functions
from GridWorld import GridWorld


def generate_random_route(grid_world, key):
    graph = grid_world.graph
    adjacent_nodes = graph.adjacency_map[key]
    x = int(key.split(',')[0])
    y = int(key.split(',')[1])
    if x == grid_world.end_x and y == grid_world.end_y:
        grid_world.route.append((x, y))
        grid_world.final_route_genetic.append((x, y))
        return -1
    grid_world.is_visited[x][y] = 1
    grid_world.route.append((x, y))
    random.shuffle(adjacent_nodes)
    for l in adjacent_nodes:
        if grid_world.is_visited[l[0]][l[1]] == 0:
            ret_val = generate_random_route(grid_world, str(l[0]) + "," + str(l[1]))
            if ret_val == -1:
                grid_world.final_route_genetic.append((l[0], l[1]))
                return -1


def crossover2(population):
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
            return_list.append(child1)
            return_list.append(child2)
    return_list.extend(population)
    return return_list


def crossover(population):
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
            subpart1 = path1[:index1]
            subpart2 = path2[:index2]
            subpart3 = path1[index1:]
            subpart4 = path2[index2:]
            if len(subpart1) < len(subpart2):
                child1 = subpart1
            else:
                child1 = subpart2
            if len(subpart3) < len(subpart4):
                child1.extend(subpart3)
            else:
                child1.extend(subpart4)
            return_list.append(child1)
    return_list.extend(population)
    return return_list


def remove_duplicates(path):
    reverse_path = path[::-1]
    duplicate = None
    for p in path:
        count = path.count(p)
        if count > 1:
            duplicate = p
    indices = [i for i, x in enumerate(path) if x == duplicate]
    ret_path = path[:indices[0]]
    ret_path = path[indices[-1]:]
    return ret_path


def mutation2(grid_world, population):
    mutated_list = []
    for i in range(len(population)):
        mutated_path = []
        path1 = population[i]
        # print(path1)
        random_nodes = random.sample(path1, 2)
        # print(random_nodes)
        index1 = path1.index(random_nodes[0])
        index2 = path1.index(random_nodes[1])
        if index1 < index2:
            child1 = path1[:index1]
            rand_path = grid_world.get_random_path(random_nodes[1], random_nodes[0])
            child1.extend(rand_path)
            child2 = path1[index2:]
            child1.extend(child2)
            mutated_path.extend(child1)
        if index1 > index2:
            child1 = path1[:index2]
            rand_path = grid_world.get_random_path(random_nodes[0], random_nodes[1])
            child1.extend(rand_path)
            child2 = path1[index1:]
            child1.extend(child2)
            mutated_path.extend(child1)
        # print(mutated_path)
        # print()
        mutated_path = remove_duplicates(mutated_path[:])
        mutated_list.append(mutated_path)
    # print(len(mutated_list))
    return mutated_list


def mutation(grid_world, population):
    count = len(population)
    mutation_count = 0.3 * count
    sample = random.sample(population, int(mutation_count))
    for list1 in sample:
        random_node = random.choice(list1)
        mutated1 = grid_world.get_random_path((grid_world.start_x, grid_world.start_y), random_node)
        mutated2 = grid_world.get_random_path(random_node, (grid_world.end_x, grid_world.end_y))
        mutated1.append((grid_world.start_x, grid_world.start_y))
        mutated1 = mutated1[::-1]
        mutated1 = mutated1[:-1]
        mutated2 = mutated2[::-1]
        mutated2 = mutated2[:-1]
        mutated1.extend(mutated2)
        population.append(mutated1)
    return population


def evaluation_function(grid_world, route):
    return len(route)


def reduce_population(population, starting_population_count):
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
    ret_list = ret_list[:starting_population_count]
    return ret_list


def genetic_iterations(grid_world):
    starting_population_count = 50
    population = []
    for i in range(starting_population_count):
        grid_world.route = []
        grid_world.final_route_genetic = []
        grid_world.is_visited = [[0] * grid_world.m for temp in range(grid_world.n)]
        generate_random_route(grid_world, grid_world.start_key)
        grid_world.final_route_genetic.append((grid_world.start_x, grid_world.start_y))
        grid_world.final_route_genetic = grid_world.final_route_genetic[::-1]
        population.append(grid_world.final_route_genetic[:-1])
        if len(grid_world.final_route_genetic[:-1]) == 0:
            print("No possible route")
            exit()

    grid_world.is_visited = [[0] * grid_world.m for temp in range(grid_world.n)]
    best_path = []
    best_score = math.inf
    for i in range(100):  # iterations
        # print('#', len(population))
        population = crossover(population)
        # print('#', len(population))
        population = reduce_population(population, starting_population_count)
        # print('#', len(population))
        population = mutation(grid_world, population)
        # print('#', len(population))
        avg = 0
        for path in population:
            avg += len(path)
        if len(population[0]) < best_score:
            best_score = len(population[0])
            best_path = population[0]
        print(i, ':', len(population[0]))
    print('Genetic:', best_score, best_path)
    grid_world.final_route_genetic = best_path


def run_genetic(grid_world):
    genetic_iterations(grid_world)
    grid_world.final_route_genetic.append((grid_world.start_x, grid_world.start_y))


grid_world = GridWorld()
Functions.create_grid_from_hex(grid_world)
# Functions.create_random_obstacles(grid_world, 0.205)
# Functions.create_fixed_obstacles(grid_world, 6)
grid_world.scan_grid_and_generate_graph()
grid_world.print_graph()
run_genetic(grid_world)
grid_world.create_grid_ui(grid_world.m, grid_world.n, (grid_world.start_x, grid_world.start_y),
                          (grid_world.end_x, grid_world.end_y), grid_world.obstacles)
grid_world.move_on_given_route_genetic()
tk.mainloop()
