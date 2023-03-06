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
