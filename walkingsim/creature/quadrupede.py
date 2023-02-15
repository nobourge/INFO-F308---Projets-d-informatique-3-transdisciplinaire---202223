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

import creature as Creature

class Quadrupede(Creature):
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
    def __init__(self, pos: tuple) -> None:
        super().__init__(self, pos)

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
