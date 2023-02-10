"""
genetic algorithm class, of quadrupede learning to walk, that receives sensor data and update steps matrix
"""

import sys

import numpy as np
import pygad as pygad_
from walkingsim.simulation import ChronoSimulation

# from _logging import logger :
from utils._logging import logger
# todo from creature.genotype import Genotype

from utils.auto_indent import AutoIndent

logger.debug("Starting genetic_algorithm.py")
sys.stdout = AutoIndent(sys.stdout)


class GeneticAlgorithm:
    # pygad.set_seed(42)
    def __init__(
            self,
            population_size,
            num_generations,
            num_parents_mating,
            fitness_func,
            num_genes,
            gene_type,
            gene_space,
            init_range_low,
            init_range_high,
            mutation_percent_genes,
            mutation_type,
            mutation_num_genes,
            mutation_by_replacement,
            mutation_range_low,
            mutation_range_high,
            crossover_type,
            crossover_percent_parents,
            on_generation,
            keep_parents,
            num_joints,
            num_steps,
            sensor_data
    ):
        self.population_size = population_size
        self.num_generations = num_generations
        self.num_parents_mating = num_parents_mating
        self.fitness_func = fitness_func
        self.num_genes = num_genes
        self.gene_type = gene_type
        self.gene_space = gene_space
        self.init_range_low = init_range_low
        self.init_range_high = init_range_high
        self.mutation_percent_genes = mutation_percent_genes
        self.mutation_type = mutation_type
        self.mutation_num_genes = mutation_num_genes
        self.mutation_percent_genes = mutation_percent_genes
        self.mutation_by_replacement = mutation_by_replacement
        self.mutation_range_low = mutation_range_low
        self.mutation_range_high = mutation_range_high
        self.crossover_type = crossover_type
        self.crossover_percent_parents = crossover_percent_parents
        self.on_generation = on_generation
        self.keep_parents = keep_parents
        self.num_joints = num_joints
        self.num_steps = num_steps
        self.sensor_data = sensor_data

        self.search_space = [
            {'low': -180, 'high': 180, 'type': 'continuous',
             'name': f'joint_{i}'} for i in
            range(num_joints * num_steps)]

        self.ga = pygad_.GA(num_parents_mating=2,
                            num_generations=100,
                            sol_per_pop=50,
                            num_genes=num_joints * num_steps,
                            mutation_percent_genes=30,
                            fitness_func=self.fitness_function,
                            )

    # def _evaluate(self):
    #     """This function returns wether or not the simulation is done, and the
    #     result (fitness) of this simulation.
    #     """
    #     # FIXME Pseudocode for this method:
    #     # 1) Get observations from creature sensors (position, angles, CoM, etc.)
    #     # 2) Get action from brain/controller based on sensors input
    #     # 3) Apply action to environment
    #     # 4) Compute reward and add it to total reward/fitness
    #     # 5) Do timestep in environment
    #     # 6) Evaluate if simulation is over or not
    #
    #     #  sensor_data = self.creature.sensor_data
    #     #  if len(sensor_data) > 0:
    #     #      print(
    #     #          sensor_data[-1]["position"],
    #     #          sensor_data[-1]["distance"],
    #     #          sensor_data[-1]["total_distance"],
    #     #      )
    #
    #     # TODO: Using those sensor data, we could calculate som fitness value
    #     return False, 0
    def fitness_function(self
                         , individual
                         , solution_idx
                         ):
        # Calculate the fitness of an individual based on the sensor data
        # and the matrix of movements represented by the individual
        """
        ValueError: The fitness function must accept 2 parameters:
            1) A solution to calculate its fitness value.
            2) The solution's index within the population.

        """
        # todo in sim or GA?

        # return fitness

    def walk_learn(self):
        best_solution, best_fitness = self.ga.run()

        self.steps = np.array(best_solution).reshape(self.num_joints,
                                                     self.num_steps)
        print(self.steps)
        logger.debug(f"Best solution: {best_solution}")
        logger.debug(f"Best solution fitness: {best_fitness}")

        plot = self.plot()

        return self.steps

    def plot(self):
        pygad_.plot_fitness()
        pygad_.plot_genes()
        pygad_.plot_new_solution_rate()

    def run(self):
        self.walk_learn()
