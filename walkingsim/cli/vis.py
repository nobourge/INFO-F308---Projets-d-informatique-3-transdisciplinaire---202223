import pickle
import sys

import gymnasium as gym
import numpy as np
from loguru import logger
from stable_baselines3 import PPO

import walkingsim
from walkingsim.simulation.ga import GA_Simulation


class GA_Vis:
    def __init__(self, sim_data_file: str, ending_delay: int) -> None:

        with open(sim_data_file, "rb") as fp:
            try:
                self.sim_data = pickle.load(fp)
            except IOError:
                logger.error("Could not load the simulation data file")
                sys.exit()

        env_props = self.sim_data["env"]
        self.__simulation = GA_Simulation(
            env_props=env_props,
            # creature=creature,
            visualize=True,
            ending_delay=ending_delay,
        )
        self.__forces_list = np.array(self.sim_data["best_solution"]).reshape(
            (
                self.__simulation.genome_discrete_intervals,
                self.__simulation.creature_shape,
            )
        )
        self.__simulation.reset()

    def run(self):
        while not self.__simulation.is_over():
            for forces in self.__forces_list:
                if self.__simulation.is_over():
                    break
                self.__simulation.step(forces)


class GYM_Vis:
    def __init__(self, model_data_file: str, env: dict, creature: str):
        env = gym.make(
            "quadrupede-v0", env_props=env, creature=creature, visualize=True
        )
        self.__model = PPO.load(model_data_file, env)

    def run(self):
        vec_env = self.__model.get_env()
        obs = vec_env.reset()
        while not vec_env.env_method("closed")[0]:
            action, _state = self.__model.predict(obs, deterministic=True)
            obs, reward, done, info = vec_env.step(action)
