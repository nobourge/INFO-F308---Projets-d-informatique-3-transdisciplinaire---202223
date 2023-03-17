from argparse import ArgumentParser

import gymnasium as gym
from loguru import logger
from stable_baselines3 import PPO

from walkingsim.algorithms.ga import GeneticAlgorithm
from walkingsim.utils.pygad_config import PygadConfig


def setup_train_parser(parser: ArgumentParser):
    parser.set_defaults(func=_train)
    parser.add_argument("creature", type=str)

    # General Options
    general_options = parser.add_argument_group("General Options")
    general_options.add_argument(
        "--environment", "-e", default="default", type=str, dest="environment"
    )
    general_options.add_argument(
        "--target", "-t", default="walk", type=str, dest="target"
    )
    general_options.add_argument(
        "--render", action="store_true", default=False, dest="do_render"
    )
    general_options.add_argument(
        "--use-gym", action="store_true", default=False, dest="use_gym"
    )

    # Genetic Algorithm options
    ga_options = parser.add_argument_group("Genetic Algorithm Options")
    ga_options.add_argument(
        "--process", action="store_true", dest="use_multiprocessing"
    )
    ga_options.add_argument(
        "--workers", "-w", default=None, type=str, dest="workers"
    )
    ga_options.add_argument("--generations", type=int, dest="num_generations")
    ga_options.add_argument("--population", type=int, dest="population_size")

    # Gym Options
    gym_options = parser.add_argument_group("Gym Options")
    gym_options.add_argument(
        "--algo", default="PPO", type=str, dest="gym_algo"
    )
    gym_options.add_argument("--timesteps", type=int, dest="gym_timesteps")
    gym_options.add_argument(
        "--progress", action="store_true", dest="gym_progress_bar"
    )


def setup_vis_parser(parser: ArgumentParser):
    parser.set_defaults(func=_visualize)
    parser.add_argument("solution_file", type=str)


def get_parser():
    parser = ArgumentParser()
    commands = parser.add_subparsers()
    setup_train_parser(commands.add_parser("train"))
    setup_vis_parser(commands.add_parser("vis"))
    return parser


def _train(args):
    if not args.use_gym:
        if args.population_size is None or args.num_generations is None:
            logger.error(
                "When using the genetic algorithm, you must pass the --population and --generations argument"
            )
            return -1

        return _train_with_pygad(
            population_size=args.population_size,
            num_generations=args.num_generations,
            workers=args.workers,
            use_multiprocessing=args.use_multiprocessing,
        )
    else:
        if args.gym_timesteps is None:
            logger.error(
                "When using gym, you must pass the --timesteps argument"
            )
            return -1

        return _train_with_gym(
            timesteps=args.gym_timesteps,
            algo=args.gym_algo,
            show_progress=args.gym_progress_bar,
        )


def _train_with_pygad(
    population_size: int = None,
    num_generations: int = None,
    workers: int = None,
    use_multiprocessing: bool = False,
):
    # FIXME: Pass environment, creature & target (walking, running, etc.)
    # FIXME: Pass the render while training options

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

    GA = GeneticAlgorithm(config)
    GA.run()


def _train_with_gym(
    timesteps: int, algo: str = "PPO", show_progress: bool = False
):
    # FIXME: Pass environment, creature & target (walking, running, etc.)
    # FIXME: Pass the render while training options
    # FIXME: Use different algorithmes

    env = gym.make(
        "quadrupede-v0",
        render_mode="human",
        properties={"gravity": [0, -9.81, 0]},
    )
    model = PPO("MultiInputPolicy", env, verbose=1)
    model.learn(total_timesteps=2e5, progress_bar=show_progress)


def _visualize(args):
    print("Vis", args)


def main():
    parser = get_parser()
    args = parser.parse_args()
    if args.func is None:
        raise RuntimeError("An error occured !")

    return args.func(args)
