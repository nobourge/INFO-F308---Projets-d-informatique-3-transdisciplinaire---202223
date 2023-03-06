import pychrono as chrono
import pychrono.irrlicht as chronoirr


class ChronoVisualizer:
    def __init__(self, system: chrono.ChSystem) -> None:
        self.__visualizer = chronoirr.ChVisualSystemIrrlicht()
        self.__system = system

    def setup(self):
        self.__visualizer.AttachSystem(self.__system)
        self.__visualizer.SetWindowSize(1024, 768)
        self.__visualizer.SetWindowTitle("3D muscle-based walking sim")
        self.__visualizer.Initialize()
        self.__visualizer.AddSkyBox()
        self.__visualizer.AddCamera(chrono.ChVectorD(2, 10, 3))
        self.__visualizer.AddTypicalLights()

    def render(self):
        self.__visualizer.BeginScene()
        self.__visualizer.Render()
        self.__visualizer.ShowInfoPanel(True)
        self.__visualizer.EndScene()

    def check(self):
        return self.__visualizer.Run()
