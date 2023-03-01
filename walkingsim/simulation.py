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

import abc
import math

import numpy as np
import pychrono as chrono
import pychrono.irrlicht as chronoirr
from loguru import logger

from walkingsim.creature.bipede import Bipede
from walkingsim.creature.quadrupede import Quadrupede
from walkingsim.environment import EnvironmentLoader


class Simulation(abc.ABC):
    """Abstract class used to create simulations. This class is used by
    `ChronoSimulation`.

    This class initiates the `EnvironmentLoader` and the `CreatureGenerator`
    for the given engine. It also loads the given environment.

    :var environment: The environment system specific to the engine
    :var generator: The creature generator specific to the engine
    :var creature: The creature in the simulation
    :var genome: The genome of the creature
    """

    def __init__(
            self,
            __engine: str,
            __env_datapath: str,
            __env: str,
            __creatures_datapath: str,
            __visualize: bool = False,
    ) -> None:
        self.__engine = __engine
        self.__loader = EnvironmentLoader(__env_datapath, self.__engine)
        self.__environment = self.__loader.load_environment(__env)
        self._visualize = __visualize
        self.__creature = None
        self.__total_reward = 0

        if self.__creature is not None:
            logger.error(
                "Cannot add a new creature to the simulation, one already exists !"
            )
            raise RuntimeError("Creature already exists in simulation")

        new_creature = Quadrupede((0, 1, 0))
        new_creature.add_to_env(self.environment)
        self.__creature = new_creature
        logger.debug(
            f"Creature '{new_creature}' added to the simulation")

    @property
    def total_reward(self):
        return self.__total_reward

    @total_reward.setter
    def total_reward(self, value):
        self.__total_reward = value

    @property
    def engine(self):
        return self.__engine

    @property
    def environment(self):
        return self.__environment

    @property
    def generator(self):
        return self.__generator

    @property
    def creature(self):
        return self.__creature

    def run(self):
        raise NotImplementedError


class ChronoSimulation(Simulation):
    """
    Simulation class for `chrono`.
    The genome used for the simulation is an m*n matrix, where
    m is the number of joints of the creature, and n is the amount of
    intervals chosen to discretise the time space. Each element represents
    a force to be applied on the joint corresponding to its related row.

    Class attributes:
        TIME_STEP - physics engine timestep
        TIME_STEPS_TO_SECOND - # of timesteps in 1 sec
        SIM_DURATION_IN_SECS - length of simulation
        FORCES_DELAY_IN_TIMESTEPS - # of timesteps during we apply
                                    a same force
        GENOME_DISCRETE_INTERVALS - the interval of the discretised
                                    genome matrix
    """

    def __init__(
            self,
            __env_datapath: str,
            __env: str,
            __creatures_datapath: str,
            __visualize: bool = False,
            __movement_gene=None,
            _TIME_STEP=1e-2,
            _SIM_DURATION_IN_SECS=5,
            # applying the same force during set timesteps
            _FORCES_DELAY_IN_TIMESTEPS=4
    ) -> None:
        super().__init__(
            "chrono", __env_datapath, __env, __creatures_datapath,
            __visualize
        )
        self._TIME_STEP = _TIME_STEP
        self._SIM_DURATION_IN_SECS = _SIM_DURATION_IN_SECS
        # applying the same force during set timesteps
        self._FORCES_DELAY_IN_TIMESTEPS = _FORCES_DELAY_IN_TIMESTEPS
        self._TIME_STEPS_TO_SECOND = 60 // _TIME_STEP
        self._GENOME_DISCRETE_INTERVALS = int(
            (
                    self._TIME_STEPS_TO_SECOND
                    * _SIM_DURATION_IN_SECS
                    // _FORCES_DELAY_IN_TIMESTEPS
            )
        )
        logger.debug(
            f"Time step: {_TIME_STEP}, "
        )
        logger.debug(
            f"Time steps to second: {self._TIME_STEPS_TO_SECOND}, "
        )
        logger.debug(
            f"Simulation duration in seconds: {_SIM_DURATION_IN_SECS}, "
        )
        logger.debug(
            f"Forces delay in timesteps: {_FORCES_DELAY_IN_TIMESTEPS}, "
        )
        logger.debug(
            f"Genome discrete intervals: "
            f"{self._GENOME_DISCRETE_INTERVALS}, "
        )

        self.__renderer = None
        if self._visualize is True:
            # FIXME use ChIrrApp to have a GUI and tweak parameters within rendering
            self.__renderer = chronoirr.ChVisualSystemIrrlicht()

        """# FIXME: Pass the creature name
        self.add_creature("")"""

        # Set forces on creature
        nbr = self.creature.joints_nbr()
        movement_matrix = np.array(__movement_gene).reshape(
            nbr, self._GENOME_DISCRETE_INTERVALS
        )
        self.creature.set_forces(movement_matrix, self._TIME_STEP)

    # Visualize
    def _render_setup(self):
        logger.debug("Initializing chrono simulation renderer")
        self.__renderer.AttachSystem(self.environment)
        self.__renderer.SetWindowSize(1024, 768)
        self.__renderer.SetWindowTitle("3D muscle-based walking sim")
        self.__renderer.Initialize()
        self.__renderer.AddSkyBox()
        self.__renderer.AddCamera(chrono.ChVectorD(2, 10, 3))
        self.__renderer.AddTypicalLights()

    def _render_step(self):
        logger.debug("Rendering step in chrono simulation")
        self.__renderer.BeginScene()
        self.__renderer.Render()
        self.__renderer.ShowInfoPanel(True)
        self.__renderer.EndScene()

    # Run Simulation
    def _compute_step_reward(self):
        sensor_data = self.creature.sensor_data
        if len(sensor_data) == 0: return 0
        curr_state = sensor_data[-1]
        # The distance is simply the actual distance
        # from the start point to the current position
        distance = curr_state["distance"]
        if sensor_data[-1]["position"][0] < sensor_data[0]["position"][
            0]:
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
            speed = curr_state["distance"] - sensor_data[-2]["distance"]
        else:
            speed = 0

        joint_limit = 0
        for r in curr_state["link_rotations"].values():
            if abs(r) >= math.pi / 2: joint_limit -= 1500

        reward = distance + walk_straight + speed + joint_limit
        return reward

    def _simulation_step(self):
        # Pseudocode for this method:
        # 1) Apply action to environment
        # 2) Get observations from creature sensors (position, angles, CoM, etc.)
        # 3) Compute reward and add it to total reward/fitness
        # 4) Do timestep in environment
        self.creature.capture_sensor_data()
        self.total_reward += self._compute_step_reward()
        self.environment.DoStepDynamics(self._TIME_STEP)

    def is_over(self):
        """This function returns wether or not the simulation is done"""
        is_over = False

        if self.is_time_limit_reached() or self.is_creature_fallen():
            is_over = True

        if self._visualize:
            device_state = self.__renderer.Run()
            if not device_state:
                is_over = True

        return is_over

    def is_time_limit_reached(self):
        current_sim_time = self.environment.GetChTime()
        return current_sim_time > self._SIM_DURATION_IN_SECS

    def is_creature_fallen(self):
        # FIXME hacky. Is there a way to detect collision between shapes?
        try:
            trunk_y = self.creature.sensor_data[-1]["position"][1]  #
        except IndexError:
            logger.debug("trunk_y = self.creature.sensor_data[-1]["
                         "position][1] IndexError: list index out of range")
            return False
        #
        # height_limit = self.creature.trunk_dim[2] / 2
        # return trunk_y < 1.2 * height_limit

        trunk_y = self.creature.sensor_data[-1]["position"][1]
        front_left_leg_y = self.creature.sensor_data[-1]["front_left_leg_position"][1]
        front_right_leg_y = self.creature.sensor_data[-1]["front_right_leg_position"][1]
        back_left_leg_y = self.creature.sensor_data[-1]["back_left_leg_position"][1]
        back_right_leg_y = self.creature.sensor_data[-1]["back_right_leg_position"][1]

        # if trunk height is less than 80% of the height of a leg
        # , then the creature is fallen
        if trunk_y < 0.8 * front_left_leg_y or \
                trunk_y < 0.8 * front_right_leg_y or \
                trunk_y < 0.8 * back_left_leg_y or \
                trunk_y < 0.8 * back_right_leg_y:
            return True

    def run(self):
        logger.debug("Starting simulation")

        if self._visualize:
            self._render_setup()

        try:
            while not self.is_over():
                self._simulation_step()
                if self._visualize:
                    self._render_step()
                # self.environment.DoStepDynamics(self.__time_step)
        except KeyboardInterrupt:
            logger.debug("Simulation was stopped by user")

        # FIXME: Cette solution n'est pas ideal, peut-etre essayer de creer
        # le visualizer une seul fois et ensuite reset l'environment
        if self.__renderer:
            self.__renderer.GetDevice().closeDevice()

        logger.debug("Simulation is done")
        return self.total_reward
