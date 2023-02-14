from walkingsim.algorithms.ga import GeneticAlgorithm
from walkingsim.simulation import ChronoSimulation

# from GeneticAlgorithm
# Import before everything else, this module configures the loguru logger

# todo : for each creature generation group : parallelize the creation
#  of each creature
#  - graph pygad
#  - simulation pychrono

# The programs has 2 steps:
# 1. Training our models and get the results
# 2. Visualize those results

# Training (with PyGad)
# Each creature has a genome, in our case
# this genome defines the force to apply on a joint
# at a certain moment in time.
# For each solution proposed by PyGad, we are going to
# modify the base genome of this creature. Then this
# creature is going to be put in the simulation environment
# and the fitness of this solution will be calculated.
# Sensor data should be gathered for each step of the simulation
# giving us more possibility on how to compute the fitness value


# def main():

#     environment, creature_name = "default", "bipede"
#     if len(sys.argv) >= 2:
#         environment = sys.argv[1]
#     if len(sys.argv) >= 3:
#         creature_name = sys.argv[2]

#     environments_path = "./environments"
#     creatures_path = "./creatures"

#     sim = ChronoSimulation(environments_path
#                            , environment
#                            , creatures_path
#                            , True
#                            , None
#     )
#     sim.environment.Add(ground.Ground())
#     # sim.add_creature(creature_name)

#     sim.run()


if __name__ == "__main__":
    # main()

    GA = GeneticAlgorithm(
        population_size=10,
        num_generations=10,
        num_parents_mating=10,
        fitness_func=None,
        num_genes=10,
        gene_type=int,
        gene_space=[0, 1],
        init_range_low=0,
        init_range_high=1,
        mutation_percent_genes=10,
        mutation_type="random",
        mutation_num_genes=2,
        mutation_by_replacement=True,
        mutation_range_low=0,
        mutation_range_high=1,
        crossover_type="single_point",
        crossover_percent_parents=0.5,
        on_generation=None,
        keep_parents=1,
        num_joints=4,
        num_steps=5,
        sensor_data=None,
    )

    GA.run()
