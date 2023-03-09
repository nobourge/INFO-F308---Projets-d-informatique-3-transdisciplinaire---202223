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
        self.__total_reward = defaultdict(float)
        self.__step_reward = None
        self.__is_creature_fallen = False
        self.__current_step = 0

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
        self.__current_step += 1

        if len(observations) == 0:
            return 0

        last_observations = observations[-1]
        # If the trunk touches the ground, alive_bonus is negative and stops sim
        if (
            not last_observations["trunk_hit_ground"]
            and not last_observations["legs_hit_ground"]
        ):
            _alive_bonus = +1
        else:
            _alive_bonus = -1

        if _alive_bonus < 0:
            self.__is_creature_fallen = True

        # Penalties for discouraging the joints to be stuck at their limit
        nb_joints_at_limit = last_observations["joints_at_limits"]

        reward = {
            "joints_at_limits": (-0.01 * nb_joints_at_limit),
            "alive_bonus": _alive_bonus,
        }

        return reward

    def _update_total_reward(self):
        for key in self.__step_reward:
            self.__total_reward[key] += self.__step_reward[key]

        # End of sim computations
        if self.is_over():
            self._make_ending_computations()

    def _make_ending_computations(self):
        """
        Compute the reward components that are calculated at the end
        of the simulation.

        Current components:
            total distance
            speed over whole sim
            height difference between start and end (y-axis)
            straight walk error (z-axis)
        """
        obs = self.__environment.observations
        self.__total_reward["distance"] = obs[-1]["distance"] * 100
        self.__total_reward["speed"] = (
            self.__total_reward["distance"]
            / Simulation._GENOME_DISCRETE_INTERVALS
        )
        self.__total_reward["height_diff"] = (
            -50 * (obs[-1]["position"][1] - obs[0]["position"][1]) ** 2
        )
        self.__total_reward["walk_straight"] = -3 * (
            obs[-1]["position"][2] ** 2
        )

    def _is_time_limit_reached(self):
        return self.__environment.time > self._SIM_DURATION_IN_SECS

    def is_over(self):
        """This function returns wether or not the simulation is done"""
        is_over = False

        if self._is_time_limit_reached() or self.__is_creature_fallen:
            is_over = True

        return is_over
