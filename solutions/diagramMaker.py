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
from matplotlib import pyplot as plt


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

        # Plotting the results
        fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(12, 8))
        fig.tight_layout(pad=5.0)

        axes[0, 0].plot(generation, total_fitness)
        axes[0, 0].set_title('Total Fitness')
        axes[0, 0].set_xlabel('Generation')
        axes[0, 0].set_ylabel('Fitness')

        axes[0, 1].plot(generation, alive_bonus)
        axes[0, 1].set_title('Alive Bonus')
        axes[0, 1].set_xlabel('Generation')
        axes[0, 1].set_ylabel('Bonus')

        axes[1, 0].plot(generation, speed)
        axes[1, 0].set_title('Speed')
        axes[1, 0].set_xlabel('Generation')
        axes[1, 0].set_ylabel('Speed')

        axes[1, 1].plot(generation, height_diff)
        axes[1, 1].set_title('Height Difference')
        axes[1, 1].set_xlabel('Generation')
        axes[1, 1].set_ylabel('Difference')

        axes[2, 0].plot(generation, forces)
        axes[2, 0].set_title('Forces')
        axes[2, 0].set_xlabel('Generation')
        axes[2, 0].set_ylabel('Forces')

        # Hide the empty subplot
        axes[2, 1].axis('off')

        plt.suptitle(
            'Population Size: {}'
            ', Generations: {}'
            ', Parent Selection: {}'
            ', Parents Mating: {}'
            ', Mutation Percent Genes: {}'
            ', keep_elitism: {}'
            # ', Crossover: {}'
            # ', Mutation: {}'
            # '\nGene Space: {}'
            # '\nNumber of Joints: {}'
            .format(
                population_size
                , num_generations
                , parent_selection_type
                , num_parents_mating
                , mutation_percent_genes
                # , crossover_type
                # , mutation_type
                # , gene_space
                # , num_joints
                , keep_elitism
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

if __name__ == "__main__":
    # run()
    # compare_solutions_from()
    configuration_file = 'pygad_config.csv'
    results_file = 'results.csv'
    # solution_date = "20230320-112004"
    # solution_date = "20230321-093448"
    # solution_date = "20230526-174539"
    # solution_date = "20230528-123545"
    # solution_date = "20230528-125245"
    # solution_date = "20230528-140208"
    # solution_date = "20230528-155230"
    solution_date = "20230528-171518"
    # path = "ga/20230320-112004/logs"
    solution_path = "ga/" + solution_date + "/"
    path = "ga/" + solution_date + "/logs/"
    dm = DiagramMaker()
    plt = dm.plot_results(path
                    , configuration_file
                    , results_file
                    )
    #save in solution_date folder
    plt.savefig(solution_path + "results.png")
    # save in doc out noe image
    # plt.savefig("doc/out/results.png")
