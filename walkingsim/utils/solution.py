# solution manager class
from walkingsim.utils.data_manager import DataManager
from walkingsim.utils.pygad_config import PygadConfig


class SolutionManager:
    def __init__(self, config: PygadConfig, env_props: dict):
        self._config = config
        self._env_props = env_props
        self._dm = DataManager("ga")

        self._best_fitness = 0
        self._best_solution = None
        self._solutions = None

    def save(self, solutions: np.ndarray, best_solution: np.ndarray):
        self._solutions = solutions
        self._best_solution = best_solution

        self._dm.save(
            {
                "config": self._config,
                "best_fitness": self._best_fitness,
                "best_solution": self._best_solution,
                "solutions": self._solutions,
                "creature": self._env_props["creature"],
                "env": self._env_props,
            }
        )

    def load(self):
        data = self._dm.load()
        self._config = data["config"]
        self._best_fitness = data["best_fitness"]
        self._best_solution = data["best_solution"]
        self._solutions = data["solutions"]
        self._env_props = data["env"]

        return self._config, self._best_fitness, self._best_solution, self._solutions

    def get_best_fitness(self):
        return self._best_fitness

    def get_best_solution(self):
        return self._best_solution

    def get_solutions(self):
        return self._solutions

    def update_best_fitness(self, best_fitness):
        self._best_fitness = best_fitness

    def update_best_solution(self, best_solution):
        self._best_solution = best_solution
