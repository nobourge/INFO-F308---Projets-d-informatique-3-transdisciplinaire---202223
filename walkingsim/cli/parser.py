"""
# Train a model
walkingsim train
    --creature/-c <creature> # Select which creature to use (default: quadrupede)
    --environment/-e <environment> # Select which environment to use (default: earth)
    --algo <algorithm> # Select which algorithm to use (default: GA)
    --render/--no-render # Render while training
    --target # Select what should the model train for (default: walking)

    # if algo is `GA`
    --generations <number> # Number of generations
    --population <number> # Number of population
    
    # if algo is PPO
    --timesteps <number> # Number of timesteps

# Visualize a model
walkingsim vis <date>
    --algo <algorithm> # Select the algorithm of which to visualize the solution (default: GA)
    --delay <seconds> # Amount of seconds to wait when simulation is done (default: 0)

# Manage envs
walkingsim env create <name> <gravity> <path/to/ground/texture> <path/to/skybox>
walkingsim env remove <name>
walkingsim env list

# Manage creatures
walkingsim creature create <legs>
"""


from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser, Namespace

from walkingsim.cli.train import GA_Train, GYM_Train
from walkingsim.cli.vis import GA_Vis, GYM_Vis
from walkingsim.loader import EnvironmentProps


class WalkingSimArgumentParser:
    def __init__(self):
        self.parser = ArgumentParser(
            formatter_class=ArgumentDefaultsHelpFormatter
        )
        self.ns = Namespace()
        self.available_algorithms = ["ga", "ppo"]

        self.commands = self.parser.add_subparsers(
            title="Command", required=True
        )
        self.setup_train_parser()
        self.setup_vis_parser()

    # Setup Parser
    def setup_train_parser(self):
        self.train_parser = self.commands.add_parser(
            "train",
            help="Train a model",
            aliases=["t"],
            formatter_class=ArgumentDefaultsHelpFormatter,
        )
        self.train_parser.set_defaults(command="train")

        # General Options
        general_options = self.train_parser.add_argument_group(
            "General Options"
        )
        general_options.add_argument(
            "--creature",
            "-c",
            dest="creature",
            default="quadrupede",
            help="Creature to use in simulation",
        )
        general_options.add_argument(
            "--environment",
            "-e",
            dest="environment",
            default="default",
            help="Environment in which the simulation will be executed",
        )
        general_options.add_argument(
            "--algorithm",
            "-a",
            dest="algorithm",
            default="ga",
            choices=self.available_algorithms,
            help="The algorithm to use to train the model",
        )
        render_group = general_options.add_mutually_exclusive_group()
        render_group.add_argument(
            "--render",
            action="store_true",
            dest="render_in_training",
            help="Do render while training",
        )
        render_group.add_argument(
            "--no-render",
            action="store_false",
            dest="render_in_training",
            help="Do not render while training",
        )

        # Genetic Algorithm Options
        ga_algo_options = self.train_parser.add_argument_group(
            "Genetic Algorithm Options"
        )
        ga_algo_options.add_argument(
            "--generations", dest="generations", help="Number of generations"
        )
        ga_algo_options.add_argument(
            "--population", dest="population", help="Size of population"
        )

        # RL Algorithm Options
        rl_algo_options = self.train_parser.add_argument_group(
            "RL Algorithms Options"
        )
        rl_algo_options.add_argument(
            "--timesteps", dest="timesteps", help="Number of timesteps"
        )

    def setup_vis_parser(self):
        self.vis_parser = self.commands.add_parser(
            "visualize",
            help="Visualize a trained model",
            aliases=["vis", "v"],
            formatter_class=ArgumentDefaultsHelpFormatter,
        )
        self.vis_parser.set_defaults(command="visualize")

        self.vis_parser.add_argument(
            "date", nargs="?", help="The date of when the model was trained"
        )

        # General Options
        general_options = self.vis_parser.add_argument_group("General Options")
        general_options.add_argument(
            "--algorithm",
            "-a",
            dest="algorithm",
            default="ga",
            choices=self.available_algorithms,
            help="The algorithm to visualize",
        )
        general_options.add_argument(
            "--delay",
            "-d",
            dest="delay",
            default=0,
            help=" Amount of seconds to wait when simulation is done",
        )

    # Handle Training
    def handle_train_ga(self):
        if self.ns.generations is None or self.ns.population is None:
            self.parser.error(
                "When using GA algorithm, you must pass --generations and --population"
            )

        GA_Train(
            creature=self.ns.creature,
            env=self.ns.env,
            population_size=self.ns.population,
            num_generations=self.ns.generations,
            workers=None,
            use_multiprocessing=False,
            visualize=self.ns.render,
        ).run()

    def handle_train_rl(self):
        if self.ns.timesteps is None:
            self.parser.error(
                "When using any RL algorithms, you must pass --timesteps"
            )

        GYM_Train(
            creature=self.ns.creature,
            env=self.ns.env,
            timesteps=self.timesteps,
            algo=self.ns.algorithm,
            show_progress=True,
            visualize=self.ns.render,
        ).run()

    # Handle Visualize
    def handle_visualize(self):
        if self.ns.algorithm == "ga":
            GA_Vis(self.ns.date, self.ns.delay).run()
        else:
            GYM_Vis(self.ns.date).run()

    # Run
    def run(self):
        self.parser.parse_args(namespace=self.ns)
        if self.ns.command == "train":
            try:
                self.ns.env = EnvironmentProps("./environments").load(
                    self.ns.environment
                )
            except FileNotFoundError:
                self.parser.error(
                    f"Invalid environment '{self.ns.environment}'"
                )

            if self.ns.algorithm == "ga":
                self.handle_train_ga()
            else:
                self.handle_train_rl()
        elif self.ns.command == "visualize":
            self.handle_visualize()
