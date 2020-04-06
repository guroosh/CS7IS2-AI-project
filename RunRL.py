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

    number_of_episodes = 30
    for episode in range(number_of_episodes):
        state = grid_world.reset()
        while True:
            grid_world.render()

            # take action and proceed one step in the environment
            action = QL.get_action(str(state))
            next_state, reward, done = grid_world.step(action)

            # env.print_value_all(QL.q_table)

            # with sample <s,a,r,s'>, agent learns new q function
            # Uncomment this
            QL.learn(str(state), action, reward, str(next_state))
            if reward == 100 or reward == -100:
                pass
            print("<state:{0} , action:{1} , reward:{2} , next_state:{3}>".format(
                str(state), str(action), str(reward), str(next_state)))
            # env.print_value_all(QL.q_table)

            state = next_state
            # Uncomment this
            # env.print_value_all(QL.q_table)

            # if episode ends, then break
            if done:
                break
    print(QL.q_table)