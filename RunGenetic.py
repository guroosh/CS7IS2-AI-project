import random
import Functions
from GridWorld import GridWorld


def crossover(list1, list2):
    return_list = []
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
    return_list.extend(list1)
    return_list.extend(list2)
    print(len(list1))
    print(len(list2))
    print(len(return_list))
    return return_list

def get_random_path(grid_world, start_node, end_node, graph):
    def recursive_function(key):
        adjacent_nodes = graph.adjacency_map[key]
        x = int(key.split(',')[0])
        y = int(key.split(',')[1])
        if x == end_x and y == end_y:
            return -1
        grid_world.is_visited[x][y] = 1
        random.shuffle(adjacent_nodes)
        for l in adjacent_nodes:
            if grid_world.is_visited[l[0]][l[1]] == 0:
                ret_val = recursive_function(str(l[0]) + "," + str(l[1]))
                if ret_val == -1:
                    inner_final_route.append((l[0], l[1]))
                    return -1

    # inner_route = []
    end_x = end_node[0]
    end_y = end_node[1]
    inner_final_route = []
    grid_world.is_visited = [[0] * grid_world.n for temp in range(grid_world.m)]
    start_key = str(start_node[0]) + ',' + str(start_node[1])
    recursive_function(start_key)
    return inner_final_route


class Genetic(object):
    def __init__(self):
        self.m = 5
        self.n = 5

    def run(self, grid_world):
        path = []
        i = 1
        iteration = 20
        for i in range(iteration):
            paths = get_random_path(grid_world, [0, 0], [4, 4], grid_world.graph)
            path.append(paths)
        return path


grid_world = GridWorld()
Functions.create_random_obstacles(grid_world, 0.05)
Functions.create_fixed_obstacles(grid_world, 6)
grid_world.scan_grid_and_generate_graph()
grid_world.print_graph()
grid_world.create_grid_ui(grid_world.m, grid_world.n, (grid_world.start_x, grid_world.start_y),
                          (grid_world.end_x, grid_world.end_y), grid_world.obstacles)

# Population paths list
path = Genetic().run(grid_world)
# print(path)
first_list = []
second_list = []
while path:
    count = len(path)
    first_pop = path[count - 1]
    first_list.append(first_pop)
    path.pop(-1)
    sec_pop = path[0]
    second_list.append(sec_pop)
    path.pop(0)
    count = count + 1

crossover(first_list, second_list)

for i in first_list:
    i_count = len(i)
    j_count = 0
    rand_idx = random.sample(i, 1)
    for j in second_list:
        while j_count < len(j):
            for k in j:
                if tuple(rand_idx) == k:
                    print(rand_idx)
                    break
                j_count = j_count + 1
        if j_count > len(j):
            rand_idx = random.sample(i, 1)
            j_count = 0

    # for j in second_list:
    #     j_count=0
    #     rand_idx = random.sample(i[0], 6)
    # rand_idx = random.choice(i[0])
    # rand_idx = random.randrange(i_count)
    # print(rand_idx)
    # if rand_idx in chain(*j[j_count]):
    #     print("rand", rand_idx)
    # while i[i_count-1]:
    #     if i[i_count-1] == j[j_count-1]:
    #         print("i equal")
    #         break;
    #     # i_count=i_count-1
    #     # j_count=j_count-1

# lst = []
# for index,letter in enumerate(path):
#     lst.append(letter) # add 'a' to your empty list
#     path.pop(index) # remove 'a' from the original string
#     print(lst)
