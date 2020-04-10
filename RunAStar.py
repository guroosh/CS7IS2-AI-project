import math
import random

import Functions
from GridWorld import GridWorld
import tkinter as tk


def a_star(grid_world):
    def get_final_path(parent, current):
        total_path = [current]
        while parent[current[0]][current[1]] is not None:
            current = parent[current[0]][current[1]]
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
    open_set.add((grid_world.start_x, grid_world.start_y))
    parent = [[None] * grid_world.m for temp in range(grid_world.n)]
    g_score = [[math.inf] * grid_world.m for temp in range(grid_world.n)]
    g_score[grid_world.start_x][grid_world.start_y] = 0
    f_score = [[math.inf] * grid_world.m for temp in range(grid_world.n)]
    f_score[grid_world.start_x][grid_world.start_y] = grid_world.get_heuristics(grid_world.start_x, grid_world.start_y)

    while open_set:
        current = get_best_node(open_set, f_score)
        if current == (grid_world.end_x, grid_world.end_y):
            return get_final_path(parent, current)
        # print(open_set)
        # print(current)
        open_set.remove((current[0], current[1]))
        grid_world.a_star_route.append((current, grid_world.color_final_path2))
        # print(open_set)
        adjacent_nodes = grid_world.graph.adjacency_map[str(current[0]) + "," + str(current[1])]
        random.shuffle(adjacent_nodes)
        for neighbor in adjacent_nodes:
            new_g_score = g_score[current[0]][current[1]] + 1
            if new_g_score < g_score[neighbor[0]][neighbor[1]]:
                parent[neighbor[0]][neighbor[1]] = current
                g_score[neighbor[0]][neighbor[1]] = new_g_score
                f_score[neighbor[0]][neighbor[1]] = g_score[neighbor[0]][neighbor[1]] + grid_world.get_heuristics(
                    neighbor[0], neighbor[1])
                if neighbor not in open_set:
                    open_set.add(neighbor)
                    grid_world.a_star_route.append((neighbor, grid_world.color_visited))
    return None


def run_a_star(grid_world):
    path = a_star(grid_world)
    if path is not None:
        grid_world.a_star_final_route = path
        # print(len(grid_world.a_star_final_route))
        return len(grid_world.a_star_final_route)
    return 0


def main_for_genetic(grid_world):
    return run_a_star(grid_world)


def main_for_a_star():
    grid_world = GridWorld(40, 40)

    Functions.create_obstacles_from_hex(grid_world)
    # Functions.create_random_obstacles(grid_world, 0.205)
    # Functions.create_fixed_obstacles(grid_world, 6)
    grid_world.scan_grid_and_generate_graph()
    grid_world.print_graph()
    graph_hex = grid_world.save_graph()
    grid_world.create_grid_ui(grid_world.m, grid_world.n, (grid_world.start_x, grid_world.start_y),
                              (grid_world.end_x, grid_world.end_y), grid_world.obstacles)
    best_path_length = run_a_star(grid_world)
    for r in grid_world.a_star_route:
        color = r[1]
        if color == grid_world.color_visited:
            grid_world.a_star_visited_count += 1
        if color == grid_world.color_final_path2:
            grid_world.a_star_opened_count += 1
    print(best_path_length,  grid_world.a_star_visited_count, grid_world.a_star_opened_count)
    grid_world.dfs_route = []
    grid_world.move_on_given_route_a_star()
    tk.mainloop()


main_for_a_star()
