from walkingsim.loader import EnvironmentProps
from walkingsim.simulation import Simulation

import pickle
import sys

from loguru import logger
import numpy as np


class GA_Vis:
    def __init__(self, sim_data_dat: str) -> None:

        with open(sim_data_dat, "rb") as fp:
            try:
                self.sim_data = pickle.load(fp)
            except IOError:
                logger.error("Could not load the simulation data file")
                sys.exit()

    def run(self):
        forces_list = np.array(self.sim_data["best_solution"]).reshape(
            (Simulation._GENOME_DISCRETE_INTERVALS, 8)
        )

        env_props = self.sim_data["env"]
        simulation = Simulation(env_props, True)
        simulation.reset()

        while not simulation.is_over():
            for forces in forces_list:
                if simulation.is_over():
                    break
                simulation.step(forces)
                simulation.render()
