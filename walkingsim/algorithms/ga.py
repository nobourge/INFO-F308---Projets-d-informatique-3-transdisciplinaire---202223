import csv
import datetime
import pickle
import os
import re

import numpy as np
import pygad as pygad_
import tqdm
from loguru import logger

from walkingsim.loader import EnvironmentProps
from walkingsim.simulation import Simulation

# All of the following will be done in a folder named with the date and time
# TODO: Dump PyGAD paramters in one file (JSON or Pickle)
# TODO: For each generations dump
#       - all the solutions in one file (~= the population)
#       - all the fitnesses in one file
#       - the best solution
#       - the best fitness
# TODO: At the end, dump the best solution in one file


class GeneticAlgorithm:
    """
    crossover_type: uniform | single_point | two_points | random
    mutation_type: adaptive | random
    """

    def __init__(self, config):

        self.data_log = []
        self.__data_dir = "solutions/" + self._generate_data_dirname()
        self._create_data_dir()
        self._save_pygad_config(config)

        self.final_results = {
            "best_fitness": 0,
            "best_solution": None,
            "solutions": None,
        }

        self.ga = pygad_.GA(
            # Population & generations settings
            initial_population=config.initial_population,
            sol_per_pop=config.population_size,
            num_generations=config.num_generations,
            num_genes=config.num_joints
            * Simulation._GENOME_DISCRETE_INTERVALS,
            # Evolution settings
            num_parents_mating=config.num_parents_mating,
            mutation_percent_genes=config.mutation_percent_genes,
            parent_selection_type=config.parent_selection_type,
            crossover_type=config.crossover_type,
            mutation_type=config.mutation_type,
            keep_elitism=config.keep_elitism,
            # Execution settings
            parallel_processing=config.parallel_processing,
            save_solutions=config.save_solutions,
            # Space
            init_range_low=config.init_range_low,
            init_range_high=config.init_range_high,
            random_mutation_min_val=config.random_mutation_min_val,
            random_mutation_max_val=config.random_mutation_max_val,
            # Callbacks
            fitness_func=self.fitness_function,
            on_generation=self._on_generation,
        )

        self.progress_gens = tqdm.tqdm(
            total=config.num_generations,
            desc="Generations",
            leave=False,
        )

    def _on_generation(self, ga_instance):
        self.progress_gens.update(1)

    @staticmethod
    def _generate_data_dirname():
        """
        Format: YYYYMMDD-HHMMSS
        """
        date_now = str(datetime.datetime.now())
        date_now = re.sub("-|:", "", date_now)
        date_now = re.sub(" ", "-", date_now)
        date_now = re.sub("\..*", "", date_now)

        return date_now + "/"

    def _create_data_dir(self):
        try:
            os.mkdir(self.__data_dir)
        except FileExistsError:
            logger.error(f"The directory {self.__data_dir} already exists")
        except FileNotFoundError:
            logger.error(f"The parent directory for {self.__data_dir} doesn't exist")
        else:
            os.mkdir(self.__data_dir + "logs/")

    def _save_pygad_config(self, config):
        with open(self.__data_dir + "pygad_config.bat", "wb") as fp:
            pickle.dump(config, fp)
            logger.info(f"Saved pygad config in {self.__data_dir}/pygad_config.bat")

    def fitness_function(self, individual, solution_idx):
        """
        Calculate the fitness of an individual based on the sensor data
            and the matrix of movements represented by the individual

        ValueError: The fitness function must accept 2 parameters:
            1) A solution to calculate its fitness value.
            2) The solution's index within the population.

        """
        self.progress_gens.refresh()
        logger.debug("Simulation {}".format(solution_idx))
        logger.debug("Creature genome: {}".format(individual))
        # Simulate the movement of the quadruped based on the movement matrix
        # and the sensor data

        forces_list = np.array(individual).reshape(
            (
                self.ga.num_genes // Simulation._GENOME_DISCRETE_INTERVALS,
                Simulation._GENOME_DISCRETE_INTERVALS,
            )
        )

        env_props = EnvironmentProps("./environments").load("default")
        simulation = Simulation(env_props)

        while not simulation.is_over():
            for forces in forces_list:
                simulation.step(list(forces))

        fitness = simulation.total_reward

        logger.debug("Creature fitness: {}".format(fitness))
        self.progress_gens.refresh()

        # Add entry in data log
        self.data_log.append(
            [self.ga.generations_completed, solution_idx, fitness]
        )

        return sum(fitness.values())

    def save_results(self):
        """
        Saves the final results dictionary in a .dat file.
        Saves it as best if applicable.
        """
        with open("solutions/previous_results.dat", "wb") as fp:
            pickle.dump(self.final_results, fp)
            logger.info("Current results written to previous_results.dat")

        with open("solutions/best_results.dat", "r+b") as fp:
            try:
                best_results = pickle.load(fp)
                if (
                    best_results["best_fitness"]
                    < self.final_results["best_fitness"]
                ):
                    pickle.dump(self.final_results, fp)
                    logger.info("New best results written to best_results.dat")
            except EOFError:
                pickle.dump(self.final_results, fp)

    def save_data_log(self):
        with open("data_log.csv", "w") as fp:
            writer = csv.writer(fp)
            writer.writerow(["generation", "solution", "fitness"])
            writer.writerows(self.data_log)

    def plot(self):
        logger.info("Plotting results")
        print("Plotting results")
        self.ga.plot_fitness()
        # self.ga.plot_genes()
        # self.ga.plot_new_solution_rate()    # Plot the new solution
        # rate. The new solution rate is the number of new solutions
        # created in the current generation divided by the population size.

    def run(self):
        logger.info("run()")
        logger.info("Genetic Algorithm started")
        self.ga.run()
        logger.info("Genetic Algorithm ended")

        solutions = self.ga.solutions  #
        best_solution, best_fitness, _ = self.ga.best_solution()
        self.final_results["best_fitness"] = best_fitness
        self.final_results["best_solution"] = best_solution
        self.final_results["solutions"] = solutions

        logger.info("Best genome: {}".format(best_solution))
        print("Best genome: {}".format(best_solution))
        logger.info("Best fitness: {}".format(best_fitness))
        print("Best fitness: {}".format(best_fitness))

        self.save_results()

        self.save_data_log()
        self.progress_gens.close()

        # self.plot()
