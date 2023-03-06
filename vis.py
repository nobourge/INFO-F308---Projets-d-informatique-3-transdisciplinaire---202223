import os
import pickle
import sys

import numpy as np
from loguru import logger

from walkingsim.loader import EnvironmentProps
from walkingsim.simulation import Simulation


def main():
    with open("previous_run_solution.dat", "rb") as fp:
        mv_matrice = pickle.load(fp)

    with open("fitness.dat", "rb") as fp:
        if os.path.getsize("fitness.dat") > 0:
            previous_best_fitness = pickle.load(fp)
        else:
            previous_best_fitness = 0
        logger.info("Fitness: {}", previous_best_fitness)

    environment, creature_name = "default", "bipede"
    if len(sys.argv) >= 2:
        environment = sys.argv[1]
    if len(sys.argv) >= 3:
        creature_name = sys.argv[2]

    forces_list = np.array(mv_matrice).reshape(
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
