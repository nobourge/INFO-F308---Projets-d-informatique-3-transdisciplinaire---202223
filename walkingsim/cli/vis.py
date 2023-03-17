import pickle
import sys

import numpy as np
from loguru import logger

from walkingsim.loader import EnvironmentProps
from walkingsim.simulation import Simulation


class GA_Vis:
    def __init__(self, sim_data_dat: str, ending_delay: int) -> None:

        with open(sim_data_dat, "rb") as fp:
            try:
                self.sim_data = pickle.load(fp)
            except IOError:
                logger.error("Could not load the simulation data file")
                sys.exit()

        self.__forces_list = np.array(self.sim_data["best_solution"]).reshape(
            (Simulation._GENOME_DISCRETE_INTERVALS, 8)
        )

        env_props = self.sim_data["env"]
        self.__simulation = Simulation(env_props, True, ending_delay)
        self.__simulation.reset()

    def run(self):

        while not self.__simulation.is_over():
            for forces in self.__forces_list:
                if self.__simulation.is_over():
                    break
                self.__simulation.step(forces)
                self.__simulation.render()
