import os


class GA_Train:
    def __init__(
        self,
        creature: str,
        env: dict,
        population_size: int = None,
        num_generations: int = None,
        workers: int = None,
        use_multiprocessing: bool = False,
        visualize: bool = False,
    ) -> None:
        from walkingsim.algorithms.ga import GeneticAlgorithm
        from walkingsim.utils.pygad_config import PygadConfig

        # FIXME: target (walking, running, etc.)

        parallel_processing = workers
        if use_multiprocessing:
            parallel_processing = ("process", workers)

        config = PygadConfig(
            num_generations=num_generations,
            num_parents_mating=4,  # TODO: Add argument
            mutation_percent_genes=(60, 10),  # TODO: Add argument
            parallel_processing=parallel_processing,
            parent_selection_type="tournament",  # TODO: Add argument
            keep_elitism=5,  # TODO: Add argument
            crossover_type="uniform",  # TODO: Add argument
            mutation_type="adaptive",  # TODO: Add argument
            initial_population=None,  # TODO: Add argument
            population_size=population_size,
            num_joints=8,  # FIXME: Load this from the creature
            save_solutions=False,
            init_range_low=-1500,
            init_range_high=1500,
            random_mutation_min_val=-1500,
            random_mutation_max_val=1500,
        )

        self.ga = GeneticAlgorithm(config, env, visualize, creature)

    def run(self):
        self.ga.run()


class GYM_Train:
    def __init__(
        self,
        creature: str,
        env: dict,
        timesteps: int,
        algo: str = "PPO",
        show_progress: bool = False,
        visualize: bool = False,
    ) -> None:
        self.timesteps = timesteps
        self.show_progress = show_progress
        self.algo = algo
        self.creature = creature

        import gymnasium as gym
        from stable_baselines3 import PPO

        # FIXME: target (walking, running, etc.)
        # FIXME: Use different algorithms

        env = gym.make(
            "quadrupede-v0",
            env_props=env,
            creature=creature,
            visualize=visualize,
        )
        self.model = PPO("MultiInputPolicy", env, verbose=1)

    def run(self):
        from walkingsim.utils.data_manager import DataManager

        self.model.learn(
            total_timesteps=self.timesteps, progress_bar=self.show_progress
        )
        self.model.save(
            os.path.join(
                DataManager().data_dir, f"{self.algo}_{self.creature}"
            )
        )
