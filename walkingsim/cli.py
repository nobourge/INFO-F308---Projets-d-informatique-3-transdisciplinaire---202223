from argparse import ArgumentParser


def setup_train_parser(parser: ArgumentParser):
    parser.set_defaults(func=_train)
    parser.add_argument("creature", type=str)

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

    ga_options = parser.add_argument_group("Genetic Algorithm Options")
    ga_options.add_argument(
        "--process", action="store_true", dest="use_multiprocessing"
    )
    ga_options.add_argument(
        "--workers", "-w", default=None, type=str, dest="workers"
    )
    ga_options.add_argument("--generations", type=int, dest="num_generations")
    ga_options.add_argument("--population", type=int, dest="population_size")

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
    print("Train", args)


def _visualize(args):
    print("Vis", args)


def main():
    parser = get_parser()
    args = parser.parse_args()
    if args.func is None:
        raise RuntimeError("An error occured !")

    return args.func(args)
