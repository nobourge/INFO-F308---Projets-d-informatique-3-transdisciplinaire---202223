import abc

from walkingsim.environment import EnvironmentLoader

import pychrono as chrono
import pychrono.irrlicht as chronoirr


class Simulation(abc.ABC):

    def __init__(self, __engine: str, __env_datapath: str, __env: str) -> None:
        self.__engine = __engine
        self.__loader = EnvironmentLoader(__env_datapath, self.__engine)
        self.__environment = self.__loader.load_environment(__env)

    @property
    def environment(self):
        return self.__environment

    def init(self):
        raise NotImplementedError

    def run(self):
        raise NotImplementedError


class ChronoSimulation(Simulation):

    def __init__(self, __env_datapath: str, __env: str) -> None:
        super().__init__('chrono', __env_datapath, __env)
        self.__renderer = chronoirr.ChVisualSystemIrrlicht()

    def init(self):
        self.__renderer.AttachSystem(self.environment)
        self.__renderer.SetWindowSize(1024, 768)
        self.__renderer.SetWindowTitle("3D muscle-based walking sim")
        self.__renderer.Initialize()
        self.__renderer.AddSkyBox()
        self.__renderer.AddCamera(chrono.ChVectorD(2, 10, 3))
        #  self.__renderer.AddLight(chrono.ChVectorD(0, 10, -20), 1000)
        self.__renderer.AddTypicalLights()

    def run(self):
        while self.__renderer.Run():
            self.__renderer.BeginScene()
            self.__renderer.Render()
            self.__renderer.ShowInfoPanel(True)
            #  chronoirr.drawAllCOGs(self.__renderer, 2)  # Draw coord systems
            #  chronoirr.drawAllLinkframes(self.__renderer, 2)
            # chronoirr.drawAllLinks(self.__renderer, 2)
            # chronoirr.drawAllBoundingBoxes(self.__renderer)
            self.__renderer.EndScene()
            self.environment.DoStepDynamics(1e-3)
