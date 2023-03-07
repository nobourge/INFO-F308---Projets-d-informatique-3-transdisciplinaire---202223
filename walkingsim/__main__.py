import multiprocessing
import os
import pickle

import walkingsim.utils._logging  # Configure logging
from walkingsim.algorithms.ga import GeneticAlgorithm

# from loguru import logger


# The programs has 2 steps:
# 1. Training our models and get the results
# 2. Visualize those results

# Training (with PyGad)
# Each creature has a genome, in our case
# this genome defines the force to apply on a joint
# at a certain moment in time.
# For each solution proposed by PyGad, we are going to
# modify the base genome of this creature. Then this
# creature is going to be put in the simulation environment
# and the fitness of this solution will be calculated.
# Sensor data should be gathered for each step of the simulation
# giving us more possibility on how to compute the fitness value


def main():

    # # initial_population_origin = "previous"
    # initial_population_origin = "all time"
    # # initial_population_sample = "best"
    # initial_population_sample = "all"
    # population_size = 500

    # threads_quantity = multiprocessing.cpu_count() * 2
    # # logger.info("Number of CPU threads: {}", threads_quantity)
    # print("Number of CPU threads: {}", threads_quantity)

    # file = ""

    # if initial_population_origin == "previous":
    #     if initial_population_sample == "best":
    #         file = "previous_run_solution.dat"
    #     elif initial_population_sample == "all":
    #         file = "previous_run_solutions.dat"
    # elif initial_population_origin == "all time":
    #     if initial_population_sample == "best":
    #         file = "solution_best.dat"
    #     elif initial_population_sample == "all":
    #         file = "solutions_all_best.dat"

    # with open(file, "rb") as fp:
    #     if os.path.getsize(file) > 0:
    #         initial_population = pickle.load(fp)
    #     else:
    #         initial_population = 0

    population_size = 10
    GA = GeneticAlgorithm(
        num_generations=2,
        num_parents_mating=4,
        mutation_percent_genes=(40,10),
        parallel_processing=None,
        parent_selection_type="tournament",
        keep_elitism=population_size // 100,
        crossover_type="uniform",
        mutation_type="adaptive",
        initial_population=None,
        population_size=population_size,
        num_joints=8,
    )
    GA.run()


if __name__ == "__main__":
    main()
