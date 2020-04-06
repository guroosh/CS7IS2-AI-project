import Functions
from GridWorld import GridWorld
from QLearning import QLearning

if __name__ == "__main__":
    grid_world = GridWorld()
    # Functions.create_grid_from_hex(grid_world)
    Functions.create_random_obstacles(grid_world, 0.305)
    grid_world.scan_grid_and_generate_graph()
    grid_world.print_graph()
    grid_world.create_grid_ui(grid_world.m, grid_world.n, (grid_world.start_x, grid_world.start_y),
                              (grid_world.end_x, grid_world.end_y), grid_world.obstacles)

    QL = QLearning(list(range(4)))

    number_of_episodes = 3000
    for episode in range(number_of_episodes):
        state = grid_world.reset()
        grid_world.is_visited = [[0] * grid_world.m for temp in range(grid_world.n)]
        while True:
            grid_world.render()

            action = QL.get_action(str(state))
            next_state, reward, done = grid_world.step(action)

            QL.learn(str(state), action, reward, str(next_state))
            print("<state:{0} , action:{1} , reward:{2} , next_state:{3}>".format(
                str(state), str(action), str(reward), str(next_state)))
            # grid_world.is_visited[state[0]][state[1]] += 1
            state = next_state

            if done:
                break
    print(QL.q_table)
