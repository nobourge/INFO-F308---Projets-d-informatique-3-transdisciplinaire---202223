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

import numpy as np
import pychrono as chrono
import pychrono.irrlicht as chronoirr
from loguru import logger

from walkingsim.creature.quadrupede import Quadrupede
from walkingsim.environment import EnvironmentLoader


#  class Simulation(abc.ABC):
#      """Abstract class used to create simulations. This class is used by
#      `ChronoSimulation`.
#
#      This class initiates the `EnvironmentLoader` and the `CreatureGenerator`
#      for the given engine. It also loads the given environment.
#
#      :var environment: The environment system specific to the engine
#      :var generator: The creature generator specific to the engine
#      :var creature: The creature in the simulation
#      :var genome: The genome of the creature
#      """
#
#      def __init__(
#          self,
#          __engine: str,
#          __env_datapath: str,
#          __env: str,
#          __creatures_datapath: str,
#          __visualize: bool = False,
#      ) -> None:
#          self.__engine = __engine
#          self.__loader = EnvironmentLoader(__env_datapath, self.__engine)
#          self._visualize = __visualize
#          self.__environment = self.__loader.load_environment(__env)
#
#          self.__creature = None
#          self.__genome = None
#
#      def add_creature(self, creature_name: str, genome: dict = None):
#          # FIXME: This function can be removed and done in the __init__ method
#          if self.__creature is not None:
#              logger.error(
#                  "Cannot add a new creature to the simulation, one already exists !"
#              )
#              raise RuntimeError("Creature already exists in simulation")
#
#          # FIXME: Pass the genome when creating the creature
#          creature = Quadrupede((0, 1.9, 0))
#          creature.add_to_env(self.environment)
#          self.__creature = creature
#          self.__genome = genome
#          logger.debug(f"Creature '{creature}' added to the simulation")
#
#      @property
#      def environment(self):
#          return self.__environment
#
#      @property
#      def generator(self):
#          return self.__generator
#
#      @property
#      def creature(self):
#          return self.__creature
#
#      @property
#      def genome(self):
#          return self.__genome
#
#      def run(self):
#          raise NotImplementedError


class ChronoSimulation:
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

    _TIME_STEP = 1e-2
    _TIME_STEPS_TO_SECOND = 60 // _TIME_STEP
    _SIM_DURATION_IN_SECS = 5
    # applying the same force during set timesteps
    _FORCES_DELAY_IN_TIMESTEPS = 4
    _GENOME_DISCRETE_INTERVALS = int((
        _TIME_STEPS_TO_SECOND
        * _SIM_DURATION_IN_SECS
        // _FORCES_DELAY_IN_TIMESTEPS
    ))

    def __init__(
        self,
        __env_datapath: str,
        __env: str,
        __creatures_datapath: str,
        __visualize: bool = False,
    ) -> None:
        # Environment params
        self.__loader = EnvironmentLoader(__env_datapath, "chrono")
        self.__environment = self.__loader.load_environment(__env)
        self.__renderer = None
        self._visualize = __visualize
        if self._visualize is True:
            # FIXME use ChIrrApp to have a GUI and tweak parameters within rendering
            self.__renderer = chronoirr.ChVisualSystemIrrlicht()
        # Creature attributes
        self.__creature = Quadrupede((0, 1.9, 0))
        self.__creature.add_to_env(self.environment)
        self.__genome = np.zeros((4, self._GENOME_DISCRETE_INTERVALS))
        self.__total_reward = 0

    # Visualize
    def _render_setup(self):
        logger.info("Initializing chrono simulation renderer")
        self.__renderer.AttachSystem(self.environment)
        self.__renderer.SetWindowSize(1024, 768)
        self.__renderer.SetWindowTitle("3D muscle-based walking sim")
        self.__renderer.Initialize()
        self.__renderer.AddSkyBox()
        self.__renderer.AddCamera(chrono.ChVectorD(2, 10, 3))
        self.__renderer.AddTypicalLights()

    def _render_step(self):
        self.__renderer.BeginScene()
        self.__renderer.Render()
        self.__renderer.ShowInfoPanel(True)
        self.__renderer.EndScene()

    # Run Simulation
    def _compute_step_reward(self):
        # FIXME do calculation for current step and return
        sensor_data = self.creature.sensor_data
        if len(sensor_data) > 0:
            print(
                sensor_data[-1]["position"],
                sensor_data[-1]["distance"],
                sensor_data[-1]["total_distance"],
            )

        return 0

    def _simulation_step(self):
        """This function returns wether or not the simulation is done"""
        # Pseudocode for this method:
        # 1) Apply action to environment
        # 2) Get observations from creature sensors (position, angles, CoM, etc.)
        # 3) Compute reward and add it to total reward/fitness
        # 4) Do timestep in environment

        # FIXME here we must apply forces in our genome matrix that correspond with
        # the current timestep
        self.creature.apply_forces([])
        self.__total_reward += self._compute_step_reward()
        self.environment.DoStepDynamics(self._TIME_STEP)

    def is_over(self):
        # FIXME set rules for deciding if sim is over or not
        is_over = False
        if self._visualize:
            device_state = self.__renderer.Run()
            if not device_state:
                is_over = True

        return is_over

    def run(self):
        logger.info("Starting simulation")
        if self._visualize:
            self._render_setup()

        try:
            while not self.is_over():
                self._simulation_step()
                if self._visualize:
                    self._render_step()
        except KeyboardInterrupt:
            logger.info("Simulation was stopped by user")

        return self.__total_reward

    @property
    def environment(self):
        return self.__environment

    @property
    def creature(self):
        return self.__creature

    @property
    def genome(self):
        return self.__genome
