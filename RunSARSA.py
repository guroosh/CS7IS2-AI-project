import Functions
from GridWorld import GridWorld
from sarsa_agent import SARSAgent
from matplotlib import pylab
from pylab import *

if __name__ == "__main__":
    grid_world = GridWorld(5,5)
    # Functions.create_grid_from_hex(grid_world)
    Functions.create_random_obstacles(grid_world, 0.105)
    grid_world.scan_grid_and_generate_graph()
    grid_world.print_graph()
    grid_world.create_grid_ui(grid_world.m, grid_world.n, (grid_world.start_x, grid_world.start_y),
                              (grid_world.end_x, grid_world.end_y), grid_world.obstacles)

    SA = SARSAgent(list(range(4)))
    scores, episodes = [], []

    number_of_episodes = 1000
    for episode in range(number_of_episodes):
        score =0
        state = grid_world.reset()
        grid_world.is_visited = [[0] * grid_world.m for temp in range(grid_world.n)]
        while True:
            grid_world.render()

            action = SA.get_action(str(state))
            next_state, reward, done = grid_world.step(action)
            next_action = SA.get_action(str(next_state))

            SA.learn(str(state), action, reward, str(next_state),next_action)
            print("<state:{0} , action:{1} , reward:{2} , next_state:{3}>".format(
                str(state), str(action), str(reward), str(next_state)))
            # grid_world.is_visited[state[0]][state[1]] += 1
            state = next_state
            action = next_action
            score += reward

            if done:
                scores.append(score)
                episodes.append(episode)
                pylab.plot(episodes, scores, 'b')
                pylab.savefig("./SARSA_learning10.png")
                break
    print(SA.q_table)
