import pickle

import numpy as np

from walkingsim.loader import EnvironmentProps
from walkingsim.simulation import Simulation


def main():
    with open("solutions/last_results.bat", "rb") as fp:
        results = pickle.load(fp)

    forces_list = np.array(results["best_solution"]).reshape(
        (8, Simulation._GENOME_DISCRETE_INTERVALS)
    )

    env_props = EnvironmentProps("./environments").load("default")
    simulation = Simulation(env_props, True)

    while not simulation.is_over():
        for forces in forces_list:
            simulation.step(list(forces))

    fitness = simulation.total_reward
    print(fitness)


if __name__ == "__main__":
    main()
