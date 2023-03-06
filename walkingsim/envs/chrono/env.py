import pychrono as chrono

from .utils import _tuple_to_chrono_vector
from .visualizer import Visualizer


class Environment:
    _TIME_STEP = 1e-2

    def __init__(self, visualize: bool=False):
        self.__environment = chrono.ChSystemNSC()

        self.__visualizer = None
        if visualize:
            self.__visualizer = Visualizer(self.__environment)

        # Materials & Colors
        self.__ground_material = chrono.ChMaterialSurfaceNSC()
        self.__ground_color = chrono.ChColor(0.5, 0.7, 0.3)

        # Observations
        self.__observations = None

    @property
    def observations(self):
        return self.__observations

    def _gather_observations(self):
        pass

    def reset(self, properties: dict):
        self.__environment.Clear()
        self.__environment.SetChTime(0) # NOTE: Is this necessary ?

        # Set environment properties
        gravity = properties.get("gravity", (0, -9.81, 0))
        self.__environment.Set_G_acc(_tuple_to_chrono_vector(gravity))
        chrono.ChCollisionModel.SetDefaultSuggestedEnvelope(0.001)
        chrono.ChCollisionModel.SetDefaultSuggestedMargin(0.001)

        # Add ground
        ground_size = (100, 5, 20)
        ground = chrono.ChBodyEasyBox(
            ground_size[0],         # Xsize
            ground_size[1],         # Ysize
            ground_size[2],         # Zsize
            4000,                   # Density
            True,                   # Collide
            True,                   # Visualize
            self.__ground_material  # Material
        )
        ground.SetBodyFixed(True)
        ground.SetPos(chrono.ChVectorD(0, ground_size[1] / 2, 0))
        ground.GetVisualShape(0).SetColor(self.__ground_color)

        # TODO: Add creature

        # Setup visualizer
        if self.__visualizer is not None:
            self.__visualizer.setup()

    def step(self, action: list):
        self._gather_observations()
        self.__environment.DoStepDynamics(self._TIME_STEP)
        if self.__visualizer is not None:
            self.__visualizer.render()
        self._gather_observations()
