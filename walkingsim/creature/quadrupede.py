"""
3D PyChrono muscle-based walking simulator
File: quadrupede.py
Authors:
    BECKER Robin-Gilles
    BOURGEOIS Noé
    HENRY DE FRAHAN Antoine
    PALMISANO Luca
Description:
    Class for basic quadruped creature.
"""

import walkingsim.utils as utils

from copy import deepcopy
import functools
import pychrono as chrono


class CustomTorqueFunction(chrono.ChFunction):
    def __init__(self, forces: list):
        super().__init__()
        self.__forces = forces

    def Clone(self):
        return deepcopy(self)

    def Get_y(self, x):
        # We want to keep x between 0 and len(self.__forces) - 1 => run a cycle multiple times
        x = int(x) % len(self.__forces)
        return self.__forces[x]


class Quadrupede:
    """
    Class for a basic quadrupede.

    Class attributes:
        collision_family
        trunk_dimensions
        legs_dimensions

    Attributes:
        joints
        bodies
        sensor_data
    """
    _collision_family = 2
    _trunk_dimensions = (1.0, 0.5, 0.5)
    _legs_dimensions = (0.3, 0.7, 0.15)

    def __init__(self, pos: tuple) -> None:
        self.__pos = chrono.ChVectorD(pos[0], pos[1], pos[2])

        # first elem 0 is the trunk, the rest are the legs
        self.__bodies = []
        self.__joints = []
        self.__sensor_data = []
        self.__joints_forces = []

        self.__x_distance_target = 100

        self._create_trunk()
        self._create_legs()
        # XXX debug purposes
        # TODO: Remove following line, replaced by set_forces
        # self.apply_forces()

    def set_forces(self, forces: list):
        if len(forces) < len(self.__joints):
            raise RuntimeError('Forces for joints are not enough')

        # Store the forces for later use
        self.__joints_forces = forces
        
        # NOTE: Important to store the function otherwise they are destroyed
        # when function is terminated, so chrono cannot access them anymore
        self.__joints_funcs = []

        for i, joint in enumerate(self.__joints):
            self.__joints_funcs.append(CustomTorqueFunction(forces[i]))
            joint.SetTorqueFunction(self.__joints_funcs[i])

    def _create_trunk(self):
        trunk_part = self._create_bone(self._trunk_dimensions)
        trunk_part.GetCollisionModel().SetFamily(self._collision_family)
        trunk_part.GetCollisionModel().SetFamilyMaskNoCollisionWithFamily(
            self._collision_family
        )
        trunk_part.SetPos(self.__pos)
        self.__bodies.append(trunk_part)

        # XXX: For debug purposes
        #  trunk_part.SetBodyFixed(True)

    def _create_legs(self):
        x_trunk = self.__pos.x
        x_back_legs = x_trunk - 0.8 * (self._trunk_dimensions[0] / 2)
        x_front_legs = x_trunk + 0.8 * (self._trunk_dimensions[0] / 2)

        y_trunk = self.__pos.y
        y_legs = y_trunk - 1.8 * (self._trunk_dimensions[1] / 2)

        z_trunk = self.__pos.z
        z_left_legs = z_trunk + (self._trunk_dimensions[2] / 2)
        z_right_legs = z_trunk - (self._trunk_dimensions[2] / 2)

        self._create_single_leg(x_front_legs, y_legs, z_left_legs)
        self._create_single_leg(x_front_legs, y_legs, z_right_legs)
        self._create_single_leg(x_back_legs, y_legs, z_left_legs)
        self._create_single_leg(x_back_legs, y_legs, z_right_legs)

    def _create_single_leg(self, *pos):
        leg_part = self._create_bone(self._legs_dimensions)
        leg_part.GetCollisionModel().SetFamily(self._collision_family)
        leg_part.GetCollisionModel().SetFamilyMaskNoCollisionWithFamily(
            self._collision_family
        )
        leg_part.SetPos(chrono.ChVectorD(*pos))
        self.__bodies.append(leg_part)

        # TODO: Add constraints on the joints
        joint = chrono.ChLinkMotorRotationTorque()
        joint_frame = chrono.ChFrameD(chrono.ChVectorD(*pos))
        joint.Initialize(self.__bodies[0], leg_part, joint_frame)
        self.__joints.append(joint)

    def _create_bone(self, size: tuple):
        bone_material = chrono.ChMaterialSurfaceNSC()
        bone_material.SetFriction(0.5)
        bone_material.SetDampingF(0.2)
        #  bone_material.SetCompliance(0.0005)
        #  bone_material.SetComplianceT(0.0005)

        bone = chrono.ChBodyEasyBox(
            size[0], size[1], size[2], 1000, True, True, bone_material
        )
        bone.SetBodyFixed(False)
        bone.GetVisualShape(0).SetColor(chrono.ChColor(0.5, 0.7, 0.5))

        return bone

    def apply_forces(self, forces: list = []):
        for i, joint in enumerate(self.__joints):
            # XXX debug, periodic torque function
            #  mod = 1 if i % 2 == 0 else -1
            #  sin_torque = chrono.ChFunction_Sine(
            #      0, 1, mod * 90  # phase [rad]  # frequency [Hz]
            #  )  # amplitude [Nm]
            #  joint.SetTorqueFunction(sin_torque)

            # FIXME not the proper way, check chrono docs about motors
            current_torque = chrono.ChFunction_Const(1.0)
            joint.SetTorqueFunction(current_torque)

    def add_to_env(self, __env):
        for body in self.__bodies:
            __env.Add(body)
        for joint in self.__joints:
            __env.Add(joint)

    def capture_sensor_data(self):
        # We capture the information from basic sensors (position, rotation, etc.)
        pos = self.__bodies[0].GetPos()
        self.__sensor_data.append({"position": (pos.x, pos.y, pos.z)})

        # We compute additional information (distance, total distance, etc.)
        step_distance = 0
        total_distance = 0
        if len(self.__sensor_data) > 1:
            step_distance = utils.distance(
                self.__sensor_data[-1]["position"],
                self.__sensor_data[0]["position"],
            )

            # FIXME: Total distance is not calculated correctly
            for i, data in enumerate(self.__sensor_data[1:]):
                prev_pos = self.__sensor_data[i]
                distance_from_prev_pos = utils.distance(
                    data['position'],
                    prev_pos['position']
                )
                total_distance += distance_from_prev_pos

        # We update the last sensor data added with those additional information
        self.__sensor_data[-1].update(
            {"distance": step_distance, "total_distance": total_distance}
        )

    @property
    def sensor_data(self):
        return self.__sensor_data
