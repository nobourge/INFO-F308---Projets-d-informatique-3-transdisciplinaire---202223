import csv
import os
import pickle

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

    def __init__(
        self,
        num_generations,
        num_parents_mating,
        mutation_percent_genes,
        parallel_processing,
        parent_selection_type,
        keep_elitism,
        crossover_type,
        mutation_type,
        initial_population=None,
        population_size=None,
        num_joints=None,
    ):
        self.data_log = []

        self.ga = pygad_.GA(
            # Population & Generations settings
            initial_population=initial_population,
            sol_per_pop=population_size,
            num_generations=num_generations,
            num_genes=num_joints * Simulation._GENOME_DISCRETE_INTERVALS,
            # Other Settings
            num_parents_mating=num_parents_mating,
            mutation_percent_genes=mutation_percent_genes,
            parallel_processing=parallel_processing,
            parent_selection_type=parent_selection_type,
            crossover_type=crossover_type,
            mutation_type=mutation_type,
            keep_elitism=keep_elitism,
            save_solutions=False,
            # Space
            init_range_low=-1000,
            init_range_high=1000,
            random_mutation_min_val=-1000,
            random_mutation_max_val=1000,
            # Callbacks
            fitness_func=self.fitness_function,
            on_generation=self._on_generation,
        )

        self.progress_gens = tqdm.tqdm(
            total=num_generations,
            desc="Generations",
            leave=False,
        )

    def _on_generation(self, ga_instance):
        self.progress_gens.update(1)

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

        return fitness

    def save_sol(self, solutions, best_sol, best_fitness):
        # from solutions
        #   save best if better than previous
        #       read the previous best fitness from file fitness.dat
        with open("fitness_best.dat", "rb") as fp:
            if os.path.getsize("fitness_best.dat") > 0:
                previous_best_fitness = pickle.load(fp)
            else:
                previous_best_fitness = 0
            logger.info("Previous best fitness: {}", previous_best_fitness)

        if previous_best_fitness < best_fitness:
            print(
                "previous best fitness: ",
                previous_best_fitness,
                "< best fitness: ",
                best_fitness,
            )

            # save all solutions best
            with open("solutions_all_best.dat", "wb") as fp:
                pickle.dump(solutions, fp)
            print(
                "Best genomes was successfully written in "
                "solutions_all_best.dat"
            )

            with open("solution_best.dat", "wb") as fp:
                pickle.dump(best_sol, fp)
            print(
                "Best genome was successfully written in " "solution_best.dat"
            )

            with open("fitness_best.dat", "wb") as fp:
                pickle.dump(best_fitness, fp)

        # current
        with open("previous_run_solution.dat", "wb") as fp:
            pickle.dump(best_sol, fp)
        print(
            "Best current genome was successfully written as "
            "current in "
            "previous_run_solution.dat"
        )

        with open("previous_run_solutions.dat", "wb") as fp:
            pickle.dump(solutions, fp)
        print(
            "All current genomes were successfully written as "
            "current in "
            "previous_run_solutions.dat"
        )

        with open("fitness.dat", "wb") as fp:
            pickle.dump(best_fitness, fp)
        print(
            "Current fitness was successfully written as current in "
            "previous_run_solution.dat"
        )

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
        # # rate. The new solution rate is the number of new solutions
        # # created in the current generation divided by the population size.

    def run(self):
        logger.info("run()")
        logger.info("Genetic Algorithm started")
        self.ga.run()
        # get all the solutions
        solutions = self.ga.solutions  #

        best_solution, best_fitness, _ = self.ga.best_solution()
        logger.info("Genetic Algorithm ended")
        logger.info("Best genome: {}".format(best_solution))
        print("Best genome: {}".format(best_solution))

        logger.info("Best fitness: {}".format(best_fitness))
        print("Best fitness: {}".format(best_fitness))
        self.save_sol(solutions, best_solution, best_fitness)

        self.save_data_log()
        self.progress_gens.close()

        # self.plot()
