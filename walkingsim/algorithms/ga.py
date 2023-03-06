import csv
import os
import pickle
import numpy as np

import pygad as pygad_
import tqdm
from loguru import logger

from walkingsim.loader import EnvironmentProps
from walkingsim.simulation import Simulation


class GeneticAlgorithm:
    def __init__(
        self,
        initial_population,
        population_size,
        sol_per_pop,
        num_steps,
        num_generations,
        num_parents_mating,
        mutation_percent_genes,
        num_joints,
        parallel_processing,
        init_range_low,
        init_range_high,
        parent_selection_type,
        keep_elitism,
        crossover_type,
        save_solutions,
        mutation_type,
    ):
        self.initial_population = initial_population
        self.population_size = population_size
        self.num_generations = num_generations
        self.sol_per_pop = sol_per_pop
        self.num_steps = num_steps

        self.num_parents_mating = num_parents_mating
        self.mutation_percent_genes = mutation_percent_genes
        self.num_joints = num_joints
        self.data_log = []
        self.parallel_processing = parallel_processing
        self.init_range_low = init_range_low
        self.init_range_high = init_range_high
        self.mutation_type = mutation_type
        self.parent_selection_type = parent_selection_type
        self.keep_elitism = keep_elitism
        self.crossover_type = crossover_type
        self.save_solutions = save_solutions

        print("GeneticAlgorithm.__init__")
        print("self.initial_population", self.initial_population)
        print("self.population_size", self.population_size)
        print("self.num_generations", self.num_generations)
        print("sol_per_pop", self.sol_per_pop)
        print("self.num_parents_mating", self.num_parents_mating)
        print("self.mutation_percent_genes", self.mutation_percent_genes)
        print("self.num_joints", self.num_joints)
        print("self.num_steps", self.num_steps)
        print("self.parallel_processing", self.parallel_processing)
        print("self.mutation_type", self.mutation_type)
        print("self.parent_selection_type", self.parent_selection_type)
        print("self.keep_elitism", self.keep_elitism)
        print("self.crossover_type", self.crossover_type)
        print("self.save_solutions", self.save_solutions)

        self.ga = pygad_.GA(
            initial_population=self.initial_population,
            num_generations=self.num_generations,
            sol_per_pop=self.sol_per_pop,
            num_genes=self.num_joints * self.num_steps,
            num_parents_mating=self.num_parents_mating,
            mutation_percent_genes=self.mutation_percent_genes,
            fitness_func=self.fitness_function,
            on_generation=self._on_generation,
            on_mutation=self._on_mutation,
            on_stop=self._on_stop,
            parallel_processing=self.parallel_processing,
            init_range_low=self.init_range_low,
            init_range_high=self.init_range_high,
            parent_selection_type=self.parent_selection_type,
            keep_elitism=self.keep_elitism,
            crossover_type=self.crossover_type,
            save_solutions=self.save_solutions,
            mutation_type="adaptive",
        )

        self.progress_sims = tqdm.tqdm(
            total=self.ga.sol_per_pop,
            desc="Generation X",
            leave=False,
        )
        self.progress_gens = tqdm.tqdm(
            total=self.num_generations,
            desc="Generations",
            leave=False,
        )

    def _on_mutation(self, ga_instance, offspring_mutation):
        self.progress_sims.reset(ga_instance.sol_per_pop)
        self.progress_sims.set_description(
            f"Generation {ga_instance.generations_completed}"
        )

    def _on_generation(self, ga_instance):
        self.progress_gens.update(1)

    def _on_stop(self, ga_instance, last_population_fitness):
        self.progress_sims.reset(ga_instance.sol_per_pop)

    def fitness_function(self, individual, solution_idx):
        """
        Calculate the fitness of an individual based on the sensor data
            and the matrix of movements represented by the individual

        ValueError: The fitness function must accept 2 parameters:
            1) A solution to calculate its fitness value.
            2) The solution's index within the population.

        """
        logger.debug("Simulation {}".format(solution_idx))
        logger.debug("Creature genome: {}".format(individual))
        # Simulate the movement of the quadruped based on the movement matrix
        # and the sensor data
        
        forces_list = np.array(individual).reshape(
            (self.num_joints, Simulation._GENOME_DISCRETE_INTERVALS)
        )

        env_props = EnvironmentProps("./environments").load("default")
        simulation = Simulation(env_props)
        
        while not simulation.is_over():
            for forces in forces_list:
                simulation.step(list(forces))
        
        fitness = simulation.total_reward

        logger.debug("Creature fitness: {}".format(fitness))
        self.progress_sims.update(1)
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
        solutions = self.ga.solutions()  #

        best_solution, best_fitness, _ = self.ga.best_solution()
        logger.info("Genetic Algorithm ended")
        logger.info("Best genome: {}".format(best_solution))
        print("Best genome: {}".format(best_solution))

        logger.info("Best fitness: {}".format(best_fitness))
        print("Best fitness: {}".format(best_fitness))
        self.save_sol(solutions, best_solution, best_fitness)

        self.save_data_log()
        self.progress_sims.close()
        self.progress_gens.close()

        self.plot()
