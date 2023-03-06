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
import math
import numpy as np
from loguru import logger

from walkingsim.environment import EnvironmentLoader
from walkingsim.envs.chrono import ChronoEnvironment

# class ChronoSimulation:
#     """
#     Simulation class for `chrono`.
#     The genome used for the simulation is an m*n matrix, where
#     m is the number of joints of the creature, and n is the amount of
#     intervals chosen to discretise the time space. Each element represents
#     a force to be applied on the joint corresponding to its related row.

#     Class attributes:
#         TIME_STEP - physics engine timestep
#         TIME_STEPS_TO_SECOND - # of timesteps in 1 sec
#         SIM_DURATION_IN_SECS - length of simulation
#         FORCES_DELAY_IN_TIMESTEPS - # of timesteps during we apply
#                                     a same force
#         GENOME_DISCRETE_INTERVALS - the interval of the discretised
#                                     genome matrix
#     """

#     def __init__(
#         self,
#         __env_datapath: str,
#         __env: str,
#         __creatures_datapath: str,
#         __visualize: bool = False,
#         __movement_gene=None,
#         _TIME_STEP=1e-2,
#         _SIM_DURATION_IN_SECS=5,
#         # applying the same force during set timesteps
#         _FORCES_DELAY_IN_TIMESTEPS=4,
#     ) -> None:
#         super().__init__(
#             "chrono", __env_datapath, __env, __creatures_datapath, __visualize
#         )
#         self._TIME_STEP = _TIME_STEP
#         self._SIM_DURATION_IN_SECS = _SIM_DURATION_IN_SECS
#         # applying the same force during set timesteps
#         self._FORCES_DELAY_IN_TIMESTEPS = _FORCES_DELAY_IN_TIMESTEPS
#         self._TIME_STEPS_TO_SECOND = 60 // _TIME_STEP
#         self._GENOME_DISCRETE_INTERVALS = int(
#             (
#                 self._TIME_STEPS_TO_SECOND
#                 * _SIM_DURATION_IN_SECS
#                 // _FORCES_DELAY_IN_TIMESTEPS
#             )
#         )


    # Run Simulation
    # def run(self):
    #     logger.debug("Starting simulation")

    #     if self._visualize:
    #         self._render_setup()

    #     try:
    #         while not self.is_over():
    #             self._simulation_step()
    #             if self._visualize:
    #                 self._render_step()
    #             # self.environment.DoStepDynamics(self.__time_step)
    #     except KeyboardInterrupt:
    #         logger.debug("Simulation was stopped by user")

    #     # FIXME: Cette solution n'est pas ideal, peut-etre essayer de creer
    #     # le visualizer une seul fois et ensuite reset l'environment
    #     if self.__renderer:
    #         self.__renderer.GetDevice().closeDevice()

    #     logger.debug("Simulation is done")
    #     return self.total_reward



class Simulation:
    def __init__(self) -> None:
        self.__environment = ChronoEnvironment(False)
        self.__total_reward = 0
        self.__step_reward = 0
        self.__is_creature_fallen = False

    @property
    def total_reward(self):
        return self.__total_reward

    @property
    def step_reward(self):
        return self.__step_reward

    def step(self, action: list):
        self.__environment.step(action)
        self.__step_reward = self._compute_step_reward()
        self.__total_reward += self.__step_reward

    def _compute_step_reward(self):
        # If the trunk touches the ground, alive_bonus is negative and stops sim
        _alive_bonus = (
            +1 if self.creature.get_trunk_contact_force() == 0 else -1
        )
        if _alive_bonus > 0:
            self.__is_creature_fallen = True

        sensor_data = self.creature.sensor_data
        if len(sensor_data) == 0:
            return 0
        curr_state = sensor_data[-1]
        # The distance is simply the actual distance
        # from the start point to the current position
        distance = curr_state["distance"]
        if sensor_data[-1]["position"][0] < sensor_data[0]["position"][0]:
            distance *= -1

        # The walk straight reward is a value that tells
        # if the creature is walking straight or not. If the
        # creature is walking straight the value will be close to 0
        # FIXME: Why 3 ?
        walk_straight = -3 * (curr_state["position"][2] ** 2)

        # The speed is how much distance the creature did in one step
        # If the creature went backwards, the speed is negative
        # this has a negative impact on the fitness value
        if len(sensor_data) >= 2:
            speed = (
                curr_state["distance"] - sensor_data[-2]["distance"]
            ) / self._TIME_STEP
        else:
            speed = 0

        # Penalties for discouraging the joints to be stuck at their limit
        nb_joints_at_limit = self.creature.get_nb_joints_at_limit()

        # Penalties for going lower than their current height
        try:
            height_diff = (
                curr_state["position"][1] - sensor_data[-2]["position"][1]
            )
        except IndexError:
            height_diff = 0

        reward = (
            distance * 10
            + walk_straight
            + 2 * speed
            + (-10 * nb_joints_at_limit)
            + _alive_bonus * 100
            - 50 * (height_diff**2)
        )
        return reward

    def _is_time_limit_reached(self):
        return self.__environment.time > self._SIM_DURATION_IN_SECS

    def is_over(self):
        """This function returns wether or not the simulation is done"""
        is_over = False

        if self._is_time_limit_reached() or self.__is_creature_fallen:
            is_over = True

        # FIXME: How do i do this ?
        # if self._visualize:
        #     device_state = self.__renderer.Run()
        #     if not device_state:
        #         is_over = True

        return is_over
