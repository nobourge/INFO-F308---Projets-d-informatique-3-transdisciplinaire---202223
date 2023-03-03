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

from walkingsim.creature.creature import CreatureSuperClass as Creature


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
        super().__init__(pos)

    def _create_legs(self):
        x_trunk = self.pos.x
        x_back_legs = x_trunk - 0.8 * (self.trunk_dim[0] / 2)
        x_front_legs = x_trunk + 0.8 * (self.trunk_dim[0] / 2)

        y_trunk = self.pos.y
        y_legs = y_trunk - 1.8 * (self.trunk_dim[1] / 2)

        z_trunk = self.pos.z
        z_left_legs = z_trunk + (self.trunk_dim[2] / 2)
        z_right_legs = z_trunk - (self.trunk_dim[2] / 2)

        left_front_leg = self._create_single_leg(x_front_legs, y_legs, z_left_legs)
        right_front_leg = self._create_single_leg(x_front_legs, y_legs, z_right_legs)
        left_back_leg = self._create_single_leg(x_back_legs, y_legs, z_left_legs)
        right_back_leg = self._create_single_leg(x_back_legs, y_legs, z_right_legs)

        left_front_leg_shin = self._create_single_leg(x_front_legs, y_legs-0.7, z_left_legs, left_front_leg)
        right_front_leg_shin = self._create_single_leg(x_front_legs, y_legs-0.7, z_right_legs, right_front_leg)
        left_back_leg_shin = self._create_single_leg(x_back_legs, y_legs-0.7, z_left_legs, left_back_leg)
        right_back_leg_shin = self._create_single_leg(x_back_legs, y_legs-0.7, z_right_legs, right_back_leg)

        self._create_foot(x_front_legs, y_legs-1.0, z_left_legs, left_front_leg_shin)
        self._create_foot(x_front_legs, y_legs-1.0, z_right_legs, right_front_leg_shin)
        self._create_foot(x_back_legs, y_legs-1.0, z_left_legs, left_back_leg_shin)
        self._create_foot(x_back_legs, y_legs-1.0, z_right_legs, right_back_leg_shin)
