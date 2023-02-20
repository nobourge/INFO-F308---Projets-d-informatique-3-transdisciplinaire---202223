import os
import pickle
import sys
import multiprocessing

import pygad as pygad_

from walkingsim.utils.loguru_log import logger
from walkingsim.utils.auto_indent import AutoIndent
from walkingsim.simulation import ChronoSimulation

# todo from creature.genotype import Genotype


logger.debug("Starting genetic_algorithm.py")
sys.stdout = AutoIndent(sys.stdout)


class GeneticAlgorithm:
    def __init__(
            self,
            population_size,
            num_generations,
            num_parents_mating,
            mutation_percent_genes,
            num_joints,
    ):
        self.population_size = population_size
        self.num_generations = num_generations
        self.num_parents_mating = num_parents_mating
        self.mutation_percent_genes = mutation_percent_genes
        self.num_joints = num_joints
        self.num_steps = ChronoSimulation._GENOME_DISCRETE_INTERVALS

        # Get the number of CPU threads
        num_threads = multiprocessing.cpu_count() * 2
        logger.debug("Number of CPU threads: {}", num_threads)
        print("Number of CPU threads: {}".format(num_threads))

        self.ga = pygad_.GA(
            num_parents_mating=self.num_parents_mating,
            num_generations=self.num_generations,
            sol_per_pop=self.population_size,
            num_genes=self.num_joints * self.num_steps,
            mutation_percent_genes=self.mutation_percent_genes,
            fitness_func=self.fitness_function,
            parallel_processing=num_threads

        )

    @staticmethod
    def fitness_function(individual, solution_idx):
        """
        Calculate the fitness of an individual based on the sensor data
            and the matrix of movements represented by the individual

        ValueError: The fitness function must accept 2 parameters:
            1) A solution to calculate its fitness value.
            2) The solution's index within the population.

        """
        logger.debug("Starting simulation {}", solution_idx)
        logger.debug("Creature genome: {}", individual)
        # Simulate the movement of the quadruped based on the movement matrix
        # and the sensor data

        environment = "default"
        environments_path = "./environments"
        creatures_path = "./creatures"

        simulation = ChronoSimulation(
            environments_path,
            environment,
            creatures_path,
            False,
            individual,
        )
        # simulation.add_creature(creature_name="bipede")
        fitness = simulation.run()
        logger.debug("Simulation {} ended", solution_idx)
        logger.debug("Creature fitness: {}", fitness)
        return fitness

    def save_sol(self, best_sol, best_fitness):
        # read the previous best fitness from file fitness.dat
        with open("fitness.dat", "rb") as fp:
            previous_best_fitness = pickle.load(fp)
        logger.debug("Previous best fitness: {}", previous_best_fitness)
        if previous_best_fitness < best_fitness:
            with open("solution.dat", "wb") as fp:
                pickle.dump(best_sol, fp)
            with open("fitness.dat", "wb") as fp:
                pickle.dump(best_fitness, fp)

            logger.success(
                "Best genome was successfully written in solution.dat")

    def plot(self):
        self.ga.plot_fitness()
        self.ga.plot_genes()
        self.ga.plot_new_solution_rate()

    def run(self):
        # Do not show loguru messages
        os.environ["LOGURU_LEVEL"] = "ERROR"
        self.ga.run()
        best_solution, best_fitness, _ = self.ga.best_solution()
        logger.info("Genetic Algorithm ended")
        logger.info("Best genome: {}", best_solution)
        # print the best solution
        # for i in range(self.num_joints):
        #     print("Joint {}:", i)
        #     for j in range(self.num_steps):
        #         print(
        #             "Step", j,
        #             ":", best_solution[i * self.num_steps + j],
        #         )
        logger.info("Best fitness: {}", best_fitness)
        self.save_sol(best_solution, best_fitness)
