import pychrono as chrono

from .utils import _tuple_to_chrono_vector
from .visualizer import Visualizer
from .creature import CreatureBody
from walkingsim.creature.quadrupede import Quadrupede
from walkingsim.utils import utils

class ChCustomTorqueFunction(chrono.ChFunction_SetpointCallback):
    def __init__(self, value: float):
        super().__init__()
        self.__value = value

    def SetpointCallback(self, t: float):
        return self.__value


class Environment:
    _TIME_STEP = 1e-2

    def __init__(self, visualize: bool=False):
        self.__environment = chrono.ChSystemNSC()
        self.__creature = None

        self.__visualizer = None
        if visualize:
            self.__visualizer = Visualizer(self.__environment)

        # Materials & Colors
        self.__ground_material = chrono.ChMaterialSurfaceNSC()
        self.__ground_color = chrono.ChColor(0.5, 0.7, 0.3)

        # Observations
        self.__observations = []

    @property
    def observations(self):
        return self.__observations

    @property
    def creature_shape(self):
        return len(self.__creature.motors())

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

        # Add creature
        self.__creature = Quadrupede(CreatureBody, (0, 1.65, 0))
        for body in self.__creature.bodies():
            self.__environment.Add(body)
        for joint in self.__creature.motors():
            self.__environment.Add(joint)
        for link in self.__creature.links():
            self.__environment.AddLink(link)

        # Setup visualizer
        if self.__visualizer is not None:
            self.__visualizer.setup()

    def step(self, action: list):
        self._apply_forces(action)
        self.__environment.DoStepDynamics(self._TIME_STEP)
        if self.__visualizer is not None:
            self.__visualizer.render()
        self._gather_observations()

    # private methods
    def _apply_forces(self, action: list):
        if len(action) < len(self.__creature.motors()):
            raise RuntimeError("Forces for joints are not enough")

        # NOTE: Important to store the function otherwise they are destroyed
        # when function is terminated, so chrono cannot access them anymore
        self.__joints_funcs = []

        for i, joint in enumerate(self.__creature.motors()):
            # print(forces[i])
            self.__joints_funcs.append(
                ChCustomTorqueFunction(action[i])
            )
            if isinstance(joint, chrono.ChLinkMotorRotationTorque):
                joint.SetTorqueFunction(self.__joints_funcs[i])
            elif isinstance(joint, chrono.ChLinkMotorRotationAngle):
                joint.SetAngleFunction(self.__joints_funcs[i])

    def _get_nb_joints_at_limit(self):
        """
        Returns the nb of joints that are closer to their limit angles
        """
        nb_joints_at_limit = 0
        for link in self.__creature.links():
            max_angle = link.GetLimit_Rz().GetMax()
            min_angle = link.GetLimit_Rz().GetMin()
            current_angle = link.GetRelAngle()
            treshold = 0.99
            if current_angle >= (treshold * max_angle) or current_angle <= (
                treshold * min_angle
            ):
                nb_joints_at_limit += 1

        return nb_joints_at_limit

    def _gather_observations(self):
        nb_joints_at_limit = self._get_nb_joints_at_limit()

        # The contact force of the trunk is 0 when not touching anything,
        # and != 0 when touching something (e.g. the ground)
        trunk_hit_ground = self.__creature.root.body.GetContactForce().Length() != 0

        # Get position and rotation of trunk
        trunk_pos = self.__creature.root.body.GetPos()
        self.__observations.append(
            {
                "position": (trunk_pos.x, trunk_pos.y, trunk_pos.z),
                "link_rotations": {},
            }
        )
        for i, motor in enumerate(self.__creature.motors()):
            rot = motor.GetMotorRot()
            self.__observations[-1]["link_rotations"].update({str(i): rot})

        # Distance calculation
        step_distance = 0
        total_distance = 0
        if len(self.__observations) > 1:
            step_distance = utils.distance(
                self.__observations[-1]["position"],
                self.__observations[0]["position"],
            )

            # FIXME : Total distance is not calculated correctly
            for i, data in enumerate(self.__observations[1:]):
                prev_pos = self.__observations[i]
                distance_from_prev_pos = utils.distance(
                    data["position"], prev_pos["position"]
                )
                total_distance += distance_from_prev_pos

        # We update the last sensor data added with those additional information
        self.__observations[-1].update({
            "distance": step_distance, 
            "total_distance": total_distance,
            "joints_at_limits": nb_joints_at_limit,
            "trunk_hit_ground": trunk_hit_ground
        })
