import random
import textwrap


def create_fixed_grid(grid_world, matrix):
    for row in matrix:
        for col in row:
            if matrix[row][col] == '1':
                grid_world.obstacles.add((row, col))
            if matrix[row][col] == 'S':
                pass


def create_grid_from_hex(grid_world):
    hex_code = '0x31600140000a2011000060029004000420400e0104e0023c0082908020204000004064320c408404149e0880500b00000108180094400600044220020186300094000540002424042208000480201000004108028004305604024031180006a70200804017210210038c0c143681020000341400d6b80000045076038000488c00240d40a40009020028804084002102408888810800080400201108104001210040640c0480d021804805528410000400001211408a0004522080000c049c05418204000030084'
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
