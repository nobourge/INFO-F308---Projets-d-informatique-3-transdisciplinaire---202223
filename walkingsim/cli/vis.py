import pickle
import sys

import gymnasium as gym
import numpy as np
from loguru import logger
from stable_baselines3 import PPO

import walkingsim
from walkingsim.simulation import Simulation


class GA_Vis:
    def __init__(self, sim_data_file: str, ending_delay: int) -> None:

        with open(sim_data_file, "rb") as fp:
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


class GYM_Vis:
    def __init__(self, model_data_file: str, env: dict, creature: str):
        env = gym.make(
            "quadrupede-v0",
            render_mode="human",
            properties=env,
            creature=creature,
        )
        self.__model = PPO.load(model_data_file, env)

    def run(self):
        vec_env = self.__model.get_env()
        obs = vec_env.reset()
        while not vec_env.env_method("closed")[0]:
            action, _state = self.__model.predict(obs, deterministic=True)
            obs, reward, done, info = vec_env.step(action)
