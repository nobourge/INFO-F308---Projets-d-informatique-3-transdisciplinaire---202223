from typing import NamedTuple


class PygadConfig(NamedTuple):
    num_generations: int
    num_parents_mating: int
    mutation_percent_genes: tuple
    parallel_processing: bool
    parent_selection_type: str
    keep_elitism: int
    crossover_type: str
    mutation_type: str
    initial_population: list
    population_size: int
    num_joints: int
