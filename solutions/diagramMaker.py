# class running a batch of either simulations or solutions
# retreiving data and saving it in a diagram file

# Path: walkingsim\utils\diagramMaker.py
# Compare this snippet from walkingsim\cli\vis.py:
# # visualization
import argparse
import logging
import os

import pandas as pd

from walkingsim.cli import parser
import numpy as np
import matplotlib.pyplot as plt


class DiagramMaker:
    def __init__(self):
        pass
    # def __init__(self, args):
    #     if args:
    #         self.args = args

    import pandas as pd
    import matplotlib.pyplot as plt

    def plot_results(self
                     , path
                     , configuration_file
                     , results_file):
        configuration_path = os.path.join(path, configuration_file)
        # Read the configuration file
        config_data = pd.read_csv(configuration_path)

        results_path = os.path.join(path, results_file)
        # Read the results file
        results_data = pd.read_csv(results_path)

        # Extract configuration values
        population_size = config_data['population_size'][0]
        num_generations = config_data['num_generations'][0]
        num_parents_mating = config_data['num_parents_mating'][0]
        mutation_percent_genes = eval(
            config_data['mutation_percent_genes'][0])
        parent_selection_type = config_data['parent_selection_type'][0]
        crossover_type = config_data['crossover_type'][0]
        mutation_type = config_data['mutation_type'][0]
        # gene_space = eval(config_data['gene_space'][0])
        num_joints = config_data['num_joints'][0]
        keep_elitism = config_data['keep_elitism'][0]

        # Extract results values
        generation = results_data['generation']
        total_fitness = results_data['total_fitness']
        alive_bonus = results_data['alive_bonus']
        speed = results_data['speed']
        height_diff = results_data['height_diff']
        forces = results_data['forces']
        distance = results_data['distance']

        # Plotting the results
        # fig, axes = plt.subplots(nrows=5, ncols=1, figsize=(20, 4))
        fig, axes = plt.subplots(nrows=4, ncols=1, figsize=(6,10))
        fig.tight_layout(pad=5.0)

        row = 0

        axes[row].plot(generation, total_fitness)
        axes[row].set_title('Total Fitness')
        axes[row].set_xlabel('Generation')
        axes[row].set_ylabel('Fitness')

        row += 1

        axes[row].plot(generation, alive_bonus)
        axes[row].set_title('Alive Bonus')
        axes[row].set_xlabel('Generation')
        axes[row].set_ylabel('Bonus')

        row += 1

        axes[row].plot(generation, distance)
        axes[row].set_title('Distance')
        axes[row].set_xlabel('Generation')
        axes[row].set_ylabel('Distance')

        row += 1

        axes[row].plot(generation, speed)
        axes[row].set_title('Speed')
        axes[row].set_xlabel('Generation')
        axes[row].set_ylabel('Speed')

        # axes[3].plot(generation, height_diff)
        # axes[3].set_title('Height Difference')
        # axes[3].set_xlabel('Generation')
        # axes[3].set_ylabel('Difference')

        # axes[3].plot(generation, forces)
        # axes[3].set_title('Forces')
        # axes[3].set_xlabel('Generation')
        # axes[3].set_ylabel('Forces')

        # Hide the empty subplot
        # axes[2, 1].axis('off')

        plt.suptitle(
            # ', '
            'Parent Selection: {}'
            # ', '
            # 'Parents Mating: {}'
            # ', '
            # 'Mutation Percent Genes: {}'
            # ', '
            # 'keep_elitism: {}'
            # ', '
            # 'Crossover: {}'
            # ', '
            # 'Mutation: {}'
            # '\n'
            # 'Gene Space: {}'
            # '\n'
            # 'Number of Joints: {}'
            .format(
                parent_selection_type
                # , num_parents_mating
                # , mutation_percent_genes
                # , crossover_type
                # , mutation_type
                # , gene_space
                # , num_joints
                # , keep_elitism
            ))
        plt.savefig('results.png', dpi=300, bbox_inches='tight')

        plt.show()
        # save
        # plt.savefig('results.png')
        # plt.savefig('results.png', dpi=300, bbox_inches='tight')

        return plt

    def run(self):
        # arguments all trough loop in increasing generations and
        # population size and then compare the results and select the
        # best one

        configuration_file = 'pygad_configuration.csv'
        results_file = 'results.csv'
        self.plot_results(configuration_file, results_file)

    def compare_solutions_from(self, algorithm1="ga", algorithm2="ppo"):
        # compare the solutions from two algorithms
        # create a diagram with the results
        # plot initialisation
        import numpy as np
        plot = plt.figure()

        if algorithm1 == "ga" and algorithm2 == "ppo":
            # load data from ga
            path = "solutions/ga/"
            for solution_folder in os.listdir(path):
                # open logs folder
                path = "solutions/ga/" + solution_folder + "/logs/"
                # read pygad_config.csv


                # plot data
                pass

            # load data from ppo
            # plot data

    def plot_fitness_function2d(self, fitness_function, x_min, x_max):
        # plot the fitness function
        # plot initialisation
        import numpy as np
        plot = plt.figure()
        x = np.linspace(x_min, x_max, 1000)
        y = fitness_function(x)
        plt.plot(x, y)
        plt.show()

    def plot_fitness_function3d(self):
        # # plot the fitness function
        # # plot initialisation
        # import numpy as np
        # from mpl_toolkits.mplot3d import Axes3D
        # plot = plt.figure()
        # x = np.linspace(x_min, x_max, 1000)
        # y = np.linspace(y_min, y_max, 1000)
        # X, Y = np.meshgrid(x, y)
        # Z = fitness_function(X, Y)
        # ax = Axes3D(plot)
        # ax.plot_surface(X, Y, Z)
        # plt.show()


        # H_range = np.arange(0, 10, 0.1)
        # D_range = np.arange(0, 10, 0.1)
        H_range = np.arange(0, 10.1,
                            0.1)  # Adjusted to have 101 elements
        D_range = np.arange(0, 10.1,
                            0.1)  # Adjusted to have 101 elements

        # Create a grid of points for height and distance
        H_grid, D_grid = np.meshgrid(H_range, D_range)

        # Evaluate the fitness function for each point on the grid
        fitness_grid = self.fitness_function(H_grid, D_grid)

        # Plot the fitness function as a 3D surface plot
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(H_grid, D_grid, fitness_grid, cmap='viridis')

        # Add labels and title to the plot
        ax.set_xlabel('height')
        ax.set_ylabel('distance')
        ax.set_zlabel('Fitness')
        plt.title('Fitness Function')

        # Show the plot
        plt.show()

        # Define the fitness function
    def fitness_function(self, height, distance):
        alive_bonus = 0  # Set the alive_bonus value
        time = 1  # Set the time value

        # Calculate the fitness value
        # fitness = alive_bonus + (height[1:] - height[:-1]) * 0.1 + (
        #         distance[1:] - distance[:-1]) / time
        fitness = alive_bonus + (height[:-1] - height[1:]) * 0.1 + (
                    distance[:-1] - distance[1:]) / time

        return fitness

        # Define the ranges for height and distance variables



if __name__ == "__main__":

    dm = DiagramMaker()
    # dm.plot_fitness_function3d()

    # compare_solutions_from()
    configuration_file = 'pygad_config.csv'
    results_file = 'results.csv'
    # solution_date = "20230320-112004"
    # solution_date = "20230321-093448"
    # solution_date = "20230526-164912"
    # solution_date = "20230526-174539"
    # solution_date = "20230528-123545"
    # solution_date = "20230528-125245"
    # solution_date = "20230528-140208"
    # solution_date = "20230528-155230"
    # solution_date = "20230528-171518"
    # solution_date = "20230529-Mayeight0954"
    solution_date = "20230529-Mayeight3449"
    # solution_date = "20230529-Mayeight4058"
    # path = "ga/20230320-112004/logs"
    solution_path = "ga/" + solution_date + "/"
    path = "ga/" + solution_date + "/logs/"
    plt = dm.plot_results(path
                    , configuration_file
                    , results_file
                    )
    #save in solution_date folder
    plt.savefig(solution_path + "results.png")
    # save in doc out noe image
    # plt.savefig("doc/out/results.png")
