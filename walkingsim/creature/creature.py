"""
3D PyChrono muscle-based walking simulator
File: creature.py
Authors:
    BECKER Robin-Gilles
    BOURGEOIS Noé
    HENRY DE FRAHAN Antoine
    PALMISANO Luca
Description:
    Class for basic bipede creature.
"""

import typing as t
import walkingsim.utils.utils as utils

class _CreatureBody:
    def __init__(self, size: tuple, family: int=1, position: tuple=None, parent=None) -> None:
        self.__size = size
        self.__position = (0,0,0) if position is None else position
        self.__family = family

        self.__parent = parent
        self.__childs = []
        self.__body = self._create_body()
        self.__motor = None
        self.__link = None

    def _create_body(self):
        raise NotImplementedError

    # Getters
    @property
    def size(self):
        return self.__size

    @property
    def position(self):
        return self.__position

    @property
    def family(self):
        return self.__family

    @property
    def parent(self):
        return self.__parent

    @property
    def childs(self) -> t.List["_CreatureBody"]:
        return self.__childs

    @property
    def body(self):
        return self.__body

    @property
    def link(self):
        return self.__link

    @property
    def motor(self):
        return self.__motor

    # Methods
    def collision(self, family: t.Optional[int]=None,nocollision: t.Optional[t.Sequence[int]]=None,docollision: t.Optional[t.Sequence[int]]=None) -> '_CreatureBody':
        raise NotImplementedError

    def branch(self, size: tuple, family: int = None, relpos: tuple=None) -> '_CreatureBody':
        raise NotImplementedError

    def join(self, relpos: tuple=None, constraints_z: tuple=None, motor=None) -> '_CreatureBody':
        raise NotImplementedError

class Creature:
    """
    Parent class for all creatures.

    Attributes:
        root
        sensor_data

    Methods:
        bodies: retrieve a list of all the bodies in the creature
        links: retrieve a list of all the links in the creature
        motors: retrieve a list of all the motors in the creature
    """

    def __init__(self, body_cls: t.Type[_CreatureBody], root_size: tuple, root_pos: tuple = None) -> None:
        self.__sensor_data = []

        self.__root = body_cls(
            root_size, family=1, position=root_pos, parent=None
        )
        self.create()

    def create(self):
        raise NotImplementedError

    @property
    def root(self):
        return self.__root

    def bodies(self, root=None):
        if root is None:
            root = self.root

        _bodies = [root.body]
        for child in root.childs:
            _bodies.extend(self.bodies(root=child))
        return _bodies

    def links(self, root=None):
        if root is None:
            root = self.root

        _links = []
        if root.link is not None:
            _links.append(root.link)

        for child in root.childs:
            _links.extend(self.links(root=child))
        return _links

    def motors(self, root=None):
        if root is None:
            root = self.root

        _motors = []
        if root.motor is not None:
            _motors.append(root.motor)

        for child in root.childs:
            _motors.extend(self.motors(root=child))
        return _motors

    @property
    def position(self):
        return self.root.position


    # def joints_nbr(self) -> int:
    #     return len(self.motors())

    # def get_nb_joints_at_limit(self):
    #     """
    #     Returns the nb of joints that are closer to their limit angles
    #     """
    #     nb_joints_at_limit = 0
    #     for link in self.links():
    #         max_angle = link.GetLimit_Rz().GetMax()
    #         min_angle = link.GetLimit_Rz().GetMin()
    #         current_angle = link.GetRelAngle()
    #         treshold = 0.99
    #         if current_angle >= (treshold * max_angle) or current_angle <= (
    #             treshold * min_angle
    #         ):
    #             nb_joints_at_limit += 1

    #     return nb_joints_at_limit

    # @property
    # def trunk_dim(self):
    #     return self.root.size

    # def get_trunk_contact_force(self):
    #     # The contact force of the trunk is 0 when not touching anything,
    #     # and != 0 when touching something (e.g. the ground)
    #     return self.root.body.GetContactForce().Length()

    # def set_forces(self, forces: list, timestep: float):
    #     if len(forces) < len(self.motors()):
    #         raise RuntimeError("Forces for joints are not enough")

    #     # Store the forces for later use
    #     self.__joints_forces = forces

    #     # NOTE: Important to store the function otherwise they are destroyed
    #     # when function is terminated, so chrono cannot access them anymore
    #     self.__joints_funcs = []

    #     for i, joint in enumerate(self.motors()):
    #         # print(forces[i])
    #         self.__joints_funcs.append(
    #             utils.ChCustomTorqueFunction(timestep, forces[i])
    #         )
    #         joint.SetTorqueFunction(self.__joints_funcs[i])

    # def add_to_env(self, __env):
    #     for body in self.bodies():
    #         __env.Add(body)
    #     for joint in self.motors():
    #         __env.Add(joint)
    #     for link in self.links():
    #         __env.AddLink(link)

    # def capture_sensor_data(self):
    #     self._capture_legs_sensors_data()

    #     # Distance calculation
    #     step_distance = 0
    #     total_distance = 0
    #     if len(self.__sensor_data) > 1:
    #         step_distance = utils.distance(
    #             self.__sensor_data[-1]["position"],
    #             self.__sensor_data[0]["position"],
    #         )

    #         # FIXME : Total distance is not calculated correctly
    #         for i, data in enumerate(self.__sensor_data[1:]):
    #             prev_pos = self.__sensor_data[i]
    #             distance_from_prev_pos = utils.distance(
    #                 data["position"], prev_pos["position"]
    #             )
    #             total_distance += distance_from_prev_pos

    #     # We update the last sensor data added with those additional information
    #     self.__sensor_data[-1].update(
    #         {"distance": step_distance, "total_distance": total_distance}
    #     )

    # def _capture_legs_sensors_data(self):
    #     trunk_pos = self.root.body.GetPos()
    #     self.__sensor_data.append(
    #         {
    #             "position": (trunk_pos.x, trunk_pos.y, trunk_pos.z),
    #             "link_rotations": {},
    #         }
    #     )
    #     for b in range(len(self.motors())):
    #         rot = self.motors()[b].GetMotorRot()
    #         self.__sensor_data[-1]["link_rotations"].update({str(b): rot})

    #     front_left_leg_pos = self.root.childs[0].body.GetPos()
    #     self.__sensor_data[-1].update(
    #         {
    #             "front_left_leg_position": (
    #                 front_left_leg_pos.x,
    #                 front_left_leg_pos.y,
    #                 front_left_leg_pos.z,
    #             ),
    #             "link_rotations": {},
    #         }
    #     )

    #     front_right_leg_pos = self.root.childs[1].body.GetPos()
    #     self.__sensor_data[-1].update(
    #         {
    #             "front_right_leg_position": (
    #                 front_right_leg_pos.x,
    #                 front_right_leg_pos.y,
    #                 front_right_leg_pos.z,
    #             ),
    #             "link_rotations": {},
    #         }
    #     )

    #     back_left_leg_pos = self.root.childs[2].body.GetPos()
    #     self.__sensor_data[-1].update(
    #         {
    #             "back_left_leg_position": (
    #                 back_left_leg_pos.x,
    #                 back_left_leg_pos.y,
    #                 back_left_leg_pos.z,
    #             ),
    #             "link_rotations": {},
    #         }
    #     )

    #     back_right_leg_pos = self.root.childs[3].body.GetPos()
    #     self.__sensor_data[-1].update(
    #         {
    #             "back_right_leg_position": (
    #                 back_right_leg_pos.x,
    #                 back_right_leg_pos.y,
    #                 back_right_leg_pos.z,
    #             ),
    #             "link_rotations": {},
    #         }
    #     )

    # @property
    # def sensor_data(self):
    #     return self.__sensor_data
