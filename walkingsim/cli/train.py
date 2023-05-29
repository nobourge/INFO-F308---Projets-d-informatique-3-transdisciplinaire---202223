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

    config = PygadConfig(
        num_generations=num_generations,
        # num_parents_mating=(population_size//2)+1,  # TODO: Add
        num_parents_mating=(population_size // 4) + 2,  # TODO: Add
        # num_parents_mating=(population_size//10)+1,  # TODO: Add
        # num_parents_mating=2,  # TODO: Add
        # num_parents_mating=4,  # TODO: Add
        # argument
        mutation_percent_genes=(60, 10),
        parallel_processing=None,
        parent_selection_type="tournament",
        # parent_selection_type="sss",
        # k_tournament=population_size//10 +2,
        # k_tournament=population_size//10 +2,
        k_tournament=population_size // 4 + 2,
        keep_elitism=2,  # 2 because minimum to preserve best sol
        # lineage TODO:
        # Add argument
        crossover_type="uniform",
        mutation_type="adaptive",
        # initial_population=None,
        initial_population=initial_population,
        # population_size=population_size,
        population_size=None,
        num_joints=8,  # FIXME: Load this from the creature
        save_solutions=False,
        gene_space={"low": -5, "high": 5},
        # gene_space={"low": -2, "high": 2},
        # gene_space={"low": -5, "high": 5, "step": 0.1},
        # gene_space={"low": -2, "high": 2, "step": 0.01},
        # init_range_low=-1,
        # init_range_low=-2,
        init_range_low=-2,

        # init_range_high=1,
        # init_range_high=2,
        init_range_high=2,
        # random_mutation_min_val=-0.01,
        random_mutation_min_val=-1,
        # random_mutation_min_val=-3,
        # random_mutation_max_val=0.01,
        random_mutation_max_val=1,
        # random_mutation_max_val=3,
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
