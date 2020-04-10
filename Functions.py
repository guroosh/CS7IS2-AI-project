import random
import textwrap


def create_fixed_grid(grid_world, matrix):
    for row in matrix:
        for col in row:
            if matrix[row][col] == '1':
                grid_world.obstacles.add((row, col))
            if matrix[row][col] == 'S':
                pass


def create_obstacles_from_hex(grid_world):
    hex_code = '0xc00409454010010842905a4880282852d21055081414900154d0028100300120a040890000a982c1c70914a00840485002041d000008980212510b831600001020810f401010508784d4140310135900a993c255c81201001022d5862080064460a811b2e08082102c0060a100000037478a0e0290a002a126811b002034a4005fa04800b30094010807986850461421e60080104ddc0900618a03c8348a0190649129100fa114001a142040a010095104744272239400441006018f1545a4100404114180ec028'
    binary_code = bin(int(hex_code, 16))[2:]
    binary_code = binary_code.zfill(grid_world.m * grid_world.n)
    print(len(binary_code))
    rows = textwrap.wrap(binary_code, grid_world.n)
    print(rows)
    for row_index in range(len(rows)):
        for c_index in range(len(rows[row_index])):
            number = rows[row_index][c_index]
            # print(number)
            if number == '1':
                grid_world.obstacles.add((row_index, c_index))
    # exit()
    # for s in binary_code:


# density: float between 0 and 1, defines the percentage of obstacles in the grid
def create_random_obstacles(grid_world, density):
    total_blocks = grid_world.m * grid_world.n
    number_of_walls = int(density * total_blocks)
    for i in range(number_of_walls):
        x = random.randint(0, grid_world.m - 1)
        y = random.randint(0, grid_world.n - 1)
        if not ((x == grid_world.start_x and y == grid_world.start_y) or (
                x == grid_world.end_x and y == grid_world.end_y)):
            grid_world.obstacles.add((x, y))


# distance_between_walls: defines distance between 2 fixed walls
def create_fixed_obstacles(grid_world, distance_between_walls):
    for i in range(1, grid_world.m - 1):
        for j in range(grid_world.n - 1):
            if j % distance_between_walls == 0:
                if not ((i == grid_world.start_x and j == grid_world.start_y) or (
                        i == grid_world.end_x and j == grid_world.end_y)):
                    grid_world.obstacles.add((i, j))
                if j % (2 * distance_between_walls) != 0:
                    if not ((0 == grid_world.start_x and j == grid_world.start_y) or (
                            0 == grid_world.end_x and j == grid_world.end_y)):
                        grid_world.obstacles.add((0, j))
            if j % (2 * distance_between_walls) == 0:
                if not ((grid_world.m - 1 == grid_world.start_x and j == grid_world.start_y) or (
                        grid_world.m - 1 == grid_world.end_x and j == grid_world.end_y)):
                    grid_world.obstacles.add((grid_world.m - 1, j))


def is_same(x1, y1, x2, y2):
    if x1 == x2 and y1 == y2:
        return True
    return False
