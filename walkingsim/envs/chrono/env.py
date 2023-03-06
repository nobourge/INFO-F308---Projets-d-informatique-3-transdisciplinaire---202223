import pychrono as chrono

def _tuple_to_chrono_vector(_tuple: tuple):
    if len(_tuple) != 3:
        raise RuntimeError(f"Cannot convert tuple[{len(_tuple)}] to chrono.ChVectorD")

    return chrono.ChVectorD(_tuple[0], _tuple[1], _tuple[2])

class Environment:
    def __init__(self):
        self.__environment = chrono.ChSystemNSC()

        # Materials & Colors
        self.__ground_material = chrono.ChMaterialSurfaceNSC()
        self.__ground_color = chrono.ChColor(0.5, 0.7, 0.3)

    def reset(self, properties: dict):
        self.__environment.Clear()

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

    def step(self, action: list):
        pass
