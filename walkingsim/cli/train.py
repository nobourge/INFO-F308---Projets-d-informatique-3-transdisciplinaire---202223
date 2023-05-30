import datetime
import os

import numpy as np


def train_ga(
        *,
        creature: str,
        env: dict,
        visualize: bool = False,
        duration: int = 5,
        timestep: float = 1e-2,
        timesteps: int = 500,
        population_size: int,
        num_generations: int,
):
    # from walkingsim.algorithms.ga import GeneticAlgorithm
    # from walkingsim.utils.pygad_config import PygadConfig

    from algorithms.ga import GeneticAlgorithm
    from utils.pygad_config import PygadConfig

    print("current dir", os.getcwd())
    path_to_random_initial_population = "walkingsim/cli/random_initial_population.txt"
    initial_population = np.loadtxt(path_to_random_initial_population)
    # with open(path_to_random_initial_population, "r") as f:

    print("initial_population", initial_population)

    gen_space_low = -2
    gen_space_high = 2
    gen_space_span = gen_space_high - gen_space_low
    gen_space_step = 1 / num_generations

    print("gen_space_low", gen_space_low)
    print("gen_space_high", gen_space_high)
    print("gen_space_span", gen_space_span)
    print("gen_space_step", gen_space_step)

    random_mutation_min_val = -gen_space_span / num_generations
    random_mutation_max_val = gen_space_span / num_generations

    print("random_mutation_min_val", random_mutation_min_val)
    print("random_mutation_max_val", random_mutation_max_val)


    config = PygadConfig(
        num_generations=num_generations,
        num_parents_mating=(population_size//2)+2,  # TODO: Add
        # num_parents_mating=(population_size // 4) + 2,  # TODO: Add
        # num_parents_mating=(population_size//10)+1,  # TODO: Add
        # num_parents_mating=2,  # TODO: Add
        # num_parents_mating=4,  # TODO: Add
        # argument
        mutation_percent_genes=(30, 10),
        parallel_processing=None,
        parent_selection_type="tournament",
        # parent_selection_type="sss",
        # k_tournament=population_size//10 +2,
        # k_tournament=population_size//10 +2,
        K_tournament=population_size // 2 + 2,
        # keep_elitism=population_size//2,
        # keep_elitism=population_size//3, # todo elit must be
        #  maximal but < mutating pop
        keep_elitism=2,  # 2 because minimum to preserve best sol
        # lineage TODO:
        # Add argument
        crossover_type="uniform",
        mutation_type="adaptive",
        # initial_population=None,
        initial_population=initial_population,
        population_size=population_size,
        # population_size=None,
        num_joints=8,  # FIXME: Load this from the creature
        save_solutions=False,
        gene_space={"low": gen_space_low, "high": gen_space_high, "step":
            gen_space_step},
        init_range_low=gen_space_low,
        init_range_high=gen_space_high,
        random_mutation_min_val=random_mutation_min_val,
        random_mutation_max_val=random_mutation_max_val,
        timesteps=timesteps,
    )
    model = GeneticAlgorithm(
        config=config,
        env_props=env,
        creature=creature,
        visualize=visualize,
        duration=duration,
        timestep=timestep,
    )
    model.train()
    print(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))

    model.save()
    # print datetime.datetime.now().strftime("%Y-%m-%d %height:%M:%S"
    print(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))


def train_ppo(
        *,
        creature: str,
        env: dict,
        visualize: bool = False,
        duration: int = 5,
        timestep: float = 1e-2,
        timesteps: int,
):
    from walkingsim.algorithms.ppo import PPO_Algo
    from walkingsim.utils.baselines_config import BaselinesConfig

    config = BaselinesConfig(timesteps=timesteps, show_progress=True)
    model = PPO_Algo(
        config=config,
        env_props=env,
        creature=creature,
        visualize=visualize,
        duration=duration,
        timestep=timestep,
    )
    model.train()
    model.save()
