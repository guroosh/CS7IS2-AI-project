import Functions
from GridWorld import GridWorld
from QLearning import QLearning
from matplotlib import pylab
from pylab import *

if __name__ == "__main__":
    grid_world = GridWorld(10,10)
    # Functions.create_grid_from_hex(grid_world)
    Functions.create_random_obstacles(grid_world, 0.105)
    grid_world.scan_grid_and_generate_graph()
    grid_world.print_graph()
    grid_world.create_grid_ui(grid_world.m, grid_world.n, (grid_world.start_x, grid_world.start_y),
                              (grid_world.end_x, grid_world.end_y), grid_world.obstacles)

    QL = QLearning(list(range(4)))

    scores, episodes = [], []

    number_of_episodes = 10
    for episode in range(number_of_episodes):
        score = 0
        state = grid_world.reset()
        grid_world.is_visited = [[0] * grid_world.m for temp in range(grid_world.n)]
        while True:
            grid_world.render()

            action = QL.get_action(str(state))
            next_state, reward, done = grid_world.step(action)

            QL.learn(str(state), action, reward, str(next_state))
            if reward != 0:
                print("<state:{0} , action:{1} , reward:{2} , next_state:{3}>".format(
                    str(state), str(action), str(reward), str(next_state)))
            grid_world.is_visited[state[0]][state[1]] += 1
            state = next_state
            score += reward

            if done:
                scores.append(score)
                episodes.append(episode)
                pylab.plot(episodes, scores, 'b')
                pylab.savefig("./q_learning10.png")
                break
    print(QL.q_table)
