import numpy as np

def get_random_initial_population(population_size,
                                  extremum
    ,format="string"):
    if format == "string":
        initial_population = ""
        for i in range(population_size):
            for j in range(8*500):
                initial_population += str(np.random.uniform(
                    low=-extremum,
                                                            high=extremum))
                initial_population += " "
            initial_population += "\n"

    elif format == float:
        initial_population = np.random.uniform(
            low=-extremum, high=extremum, size=(population_size, 8)
        )
    elif format == int:
        initial_population = np.random.randint(
            low=-extremum, high=extremum, size=(population_size, 8)
        )
    else:
        initial_population = np.random.uniform(
            low=-extremum, high=extremum, size=(population_size, 8)
        )
    return initial_population


def create_random_initial_population_file(population_size, extremum):
    # sring
    initial_population = get_random_initial_population(population_size, extremum)
    with open("../cli/random_initial_population.txt", "w") as f:
        f.write(str(initial_population))

if __name__ == "__main__":
    create_random_initial_population_file(100, 2)
