Readme File for Optimal Path Finding in a GridWorld:
----------------------------------------------------
Link to github repository: https://github.com/guroosh/CS7IS2-AI-project


Team members Contributions:
-------------------------------------------------------
Ashwin Sundareswaran R:
Implemented SARSA algorithm and integrated with the created Gridworld environment.
Implemented logic to make the agent not to hit the obstacles and make it learn through the environment.
Modified various hyperparameters  like  epsilon value,learning rate to make the agent work efficiently and compared the performance in different simulated grid sizes.
I also compared the working of the SARSA agent with A-star to find the difference between the algorithms in terms of finding the path.
I also tried implementing deep-SARSA but was not able to succeed within the time.

Kavya Bhadre Gowda:
Worked on Genetic Algorithm in the Grid world environment to find the shortest path.
This algorithm involves various stages like Population initialisation, Cross over, Mutation and Population reduction to find the best suitable path for traversal.
Did background research work on similar implementations on Genetic Algorithm. Then worked on functions to achieve individual stages of the algorithm as stated below;
	Generating random paths as chromosomes within a fixed gridworld environment, with fixed obstacles and fixed population count.
	Choose the two child paths from the parent path and crossover at a random point between two paths and get 2 identical child paths.
	Selecting random identical points in each crossover path and again mutate them to get a diversified path.
	Evaluating the paths based on the shortest length of traversal.
	Worked on report as well along with the team.

Shubhangi Kukreti: 
Implemented Q-learning algorithm in a simulated Gridworld environment. 
The algorithm was designed to find the optimal path between two points. 
The agent was trained to avoid obstacles by modifying the code to add penalties for hitting obstacles or straying away from the optimal path. 
Different values for discount factor and learning rate were tested to find the values that helped in the convergence of the algorithm.
	The number of iterations as well as time taken for the algorithm to converge were also observed for grids of varying sizes.
	The time to converge were compared for Q-learning and A* algorithm wherein both algorithms were run on the same grid containing randomly placed obstacles.

Chaudhary Guroosh Gabriel Singh:
Implemented the environment based on a GridWorld using python. 
Basic functions were created which helped in the integration of different algorithms. 
The functions included: Move agent, make obstacles, create UI instance using the ‘tkinter’ library, create graph, get neighbouring nodes, get heuristics, etc.
Implemented A-star (A*) to get the optimal path which would be used by algorithms.
Tried different heuristics for A* to see the effect of heuristics on the performance. 
Integrated different algorithms with the UI. Ran experiments on A-star and genetic algorithm.
