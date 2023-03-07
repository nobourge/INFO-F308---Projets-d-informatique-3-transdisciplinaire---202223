import multiprocessing
import pickle

import walkingsim.utils._logging  # Configure logging
from walkingsim.algorithms.ga import GeneticAlgorithm

from loguru import logger

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
    # threads_quantity = multiprocessing.cpu_count() * 2
    # logger.info("Number of CPU threads: {}", threads_quantity)
    # print("Number of CPU threads: {}", threads_quantity)

    with open("solutions/previous_results.dat", "rb") as fp:
        try:
            previous_results = pickle.load(fp)
        except EOFError:
            logger.warning("previous_results.dat not found")

    with open("solutions/best_results.dat", "rb") as fp:
        try:
            best_results = pickle.load(fp)
        except EOFError:
            logger.warning("best_results.dat not found")

    population_size = 10
    GA = GeneticAlgorithm(
        num_generations=2,
        num_parents_mating=4,
        mutation_percent_genes=(40, 10),
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
