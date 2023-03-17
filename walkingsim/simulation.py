"""
3D PyChrono muscle-based walking simulator
File: simulation.py
Authors:
    BECKER Robin-Gilles
    BOURGEOIS Noé
    HENRY DE FRAHAN Antoine
    PALMISANO Luca
Description:
    Classes for the simulations
"""

from collections import defaultdict

from walkingsim.envs.chrono import ChronoEnvironment
from walkingsim.fitness import AliveBonusFitness


class Simulation:
    _TIME_STEP = 1e-2
    _SIM_DURATION_IN_SECS = 5
    _TIME_STEPS_TO_SECOND = 1 / _TIME_STEP
    _GENOME_DISCRETE_INTERVALS = int(
        (_TIME_STEPS_TO_SECOND * _SIM_DURATION_IN_SECS)
    )

    def __init__(
        self,
        __env_props: dict,
        visualize: bool = False,
        ending_delay: int = 0,
        creature: str = "quadrupede",
    ) -> None:
        self.__environment = ChronoEnvironment(visualize, creature)
        self.__env_props = __env_props
        self.__fitness = AliveBonusFitness(
            self._SIM_DURATION_IN_SECS, self._TIME_STEP
        )
        self.__is_done = False
        self.__current_step = 0

        self.__reward_props = defaultdict(float)
        self.__reward = None

        self.__ending_delay = ending_delay

    @property
    def creature_shape(self):
        return self.__environment.creature_shape

    @property
    def reward_props(self):
        return self.__reward_props

    @property
    def reward(self):
        return self.__reward

    def closed(self):
        return self.__environment.closed

    def step(self, action: list):
        self.__environment.step(action, self._TIME_STEP)
        self.__reward = self._compute_step_reward(action)

    def reset(self):
        self.__environment.reset(self.__env_props)
        self.__is_done = False
        self.__reward = None
        self.__current_step = 0
        self.__reward_props.clear()
        self.__fitness.reset()

    def render(self):
        self.__environment.render()

    def close(self):
        self.__environment.close()

    def _compute_step_reward(self, forces):
        observations = self.__environment.observations
        self.__current_step += 1
        if len(observations) == 0:
            return 0

        last_observations = observations[-1]
        self.__fitness.compute(
            last_observations,
            observations,
            self.__current_step,
            forces,
            self.__environment.time,
        )
        self.__reward_props.clear()
        self.__reward_props.update(self.__fitness.props)
        self.__is_done = self.__fitness.done
        return self.__fitness.fitness

    def _is_time_limit_reached(self):
        return self.__environment.time > self._SIM_DURATION_IN_SECS

    def is_over(self):
        """This function returns wether or not the simulation is done"""
        is_over = False

        if self._is_time_limit_reached() or self.__is_done:
            is_over = True

        # Add additional delay at end of sim
        if self.__ending_delay > 0:
            is_over = False
            self.__ending_delay -= Simulation._TIME_STEP

        return is_over
