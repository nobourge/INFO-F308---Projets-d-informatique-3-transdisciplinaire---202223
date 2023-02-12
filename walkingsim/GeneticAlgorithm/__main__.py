"""
genetic algorithm
"""

from genetic_algorithm import GeneticAlgorithm

GA = GeneticAlgorithm(
    population_size=100,
    num_generations=100,
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
    num_steps=1,
    sensor_data=None,
)

GA.run()
