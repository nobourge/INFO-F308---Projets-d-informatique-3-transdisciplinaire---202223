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

from loguru import logger

from walkingsim.envs.chrono import ChronoEnvironment


class Simulation:
    _TIME_STEP = 1e-2
    _SIM_DURATION_IN_SECS = 5
    _TIME_STEPS_TO_SECOND = 1 / _TIME_STEP
    _GENOME_DISCRETE_INTERVALS = int(
        (_TIME_STEPS_TO_SECOND * _SIM_DURATION_IN_SECS)
    )

    def __init__(self, __env_props: dict, visualize: bool = False) -> None:
        self.__environment = ChronoEnvironment(visualize)
        self.__environment.reset(__env_props)
        self.__total_reward = {
            key: 0
            for key in [
                "distance",
                "walk_straight",
                "speed",
                "joints_at_limits",
                "alive_bonus",
                "height_diff",
            ]
        }

        self.__step_reward = None
        self.__is_creature_fallen = False

    @property
    def total_reward(self):
        return self.__total_reward

    @property
    def step_reward(self):
        return self.__step_reward

    def step(self, action: list):
        self.__environment.step(action, self._TIME_STEP)
        self.__step_reward = self._compute_step_reward()
        self._update_total_reward()
        self.__environment.check()

    def _compute_step_reward(self):
        observations = self.__environment.observations
        if len(observations) == 0:
            return 0

        last_observations = observations[-1]
        # If the trunk touches the ground, alive_bonus is negative and stops sim
        _alive_bonus = (
            +1 if last_observations["trunk_hit_ground"] == False else -1
        )
        if _alive_bonus < 0:
            self.__is_creature_fallen = True

        # The distance is simply the actual distance
        # from the start point to the current position
        distance = last_observations["distance"]
        if observations[-1]["position"][0] < observations[0]["position"][0]:
            distance *= -1

        # The walk straight reward is a value that tells
        # if the creature is walking straight or not. If the
        # creature is walking straight the value will be close to 0
        walk_straight = -3 * (last_observations["position"][2] ** 2)

        # The speed is how much distance the creature did in one step
        # If the creature went backwards, the speed is negative
        # this has a negative impact on the fitness value
        if len(observations) >= 2:
            speed = (
                last_observations["distance"] - observations[-2]["distance"]
            ) / self._TIME_STEP
            if (
                observations[-1]["position"][0]
                < observations[0]["position"][0]
            ):
                speed *= -1
        else:
            speed = 0

        # Penalties for discouraging the joints to be stuck at their limit
        nb_joints_at_limit = last_observations["joints_at_limits"]

        # Penalties for going lower than their current height
        try:
            height_diff = (
                last_observations["position"][1]
                - observations[-2]["position"][1]
            )
        except IndexError:
            height_diff = 0

        reward = {
            "distance": distance,
            "walk_straight": walk_straight,
            "speed": speed,
            "joints_at_limits": (-0.1 * nb_joints_at_limit),
            "alive_bonus": _alive_bonus,
            "height_diff": (50 * (height_diff)),
        }

        return reward

    def _update_total_reward(self):
        for key in self.__step_reward:
            self.__total_reward[key] += self.__step_reward[key]

    def _is_time_limit_reached(self):
        return self.__environment.time > self._SIM_DURATION_IN_SECS

    def is_over(self):
        """This function returns wether or not the simulation is done"""
        is_over = False

        if self._is_time_limit_reached() or self.__is_creature_fallen:
            is_over = True

        return is_over
