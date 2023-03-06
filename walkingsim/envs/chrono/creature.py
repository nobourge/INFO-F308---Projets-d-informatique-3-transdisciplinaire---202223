import typing as t
import pychrono as chrono

from .utils import _tuple_to_chrono_vector

class CreatureBody:
    _DENSITY = 1000
    _MATERIAL = chrono.ChMaterialSurfaceNSC()
    _MATERIAL.SetFriction(0.5)
    _MATERIAL.SetDampingF(0.2)
    _BODY_COLOR = chrono.ChColor(0.5, 0.7, 0.5)

    def __init__(self, size: tuple, family: int=1, position: tuple=None, parent=None):
        self.__size = size
        self.__position = (0,0,0) if position is None else position
        self.__family = family

        self.__parent = parent
        self.__childs = []
        self.__body = self._create_body()
        self.__motor = None
        self.__link = None

    def _create_body(self):
        body = chrono.ChBodyEasyBox(
            self.__size[0],
            self.__size[1],
            self.__size[2],
            self._DENSITY,
            True,
            True,
            self._MATERIAL,
        )
        body.SetBodyFixed(False)
        body.GetVisualShape(0).SetColor(self._BODY_COLOR)
        self.collision(family=self.__family,nocollision=[self.__family])
        chrono_pos = _tuple_to_chrono_vector(self.__position)
        body.SetPos(chrono_pos)

        return body

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
    def childs(self) -> t.List["CreatureBody"]:
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
    def collision(
        self,
        family: t.Optional[int]=None,
        nocollision: t.Optional[t.Sequence[int]]=None,
        docollision: t.Optional[t.Sequence[int]]=None
    ):
        if family is not None:
            self.__body.GetCollisionModel().SetFamily(family)
            self.__body.GetCollisionModel().SetFamilyMaskNoCollisionWithFamily(family)
            for i in range(15):
                if i != family:
                    self.__body.GetCollisionModel().SetFamilyMaskDoCollisionWithFamily(i)
            self.__family = family

        if nocollision is not None:
            for fam in nocollision:
                self.__body.GetCollisionModel().SetFamilyMaskNoCollisionWithFamily(fam)

        if docollision is not None:
            for fam in docollision:
                self.__body.GetCollisionModel().SetFamilyMaskDoCollisionWithFamily(fam)

        return self

    def branch(self, size: tuple, family: int = None, relpos: tuple=None):
        if family is None:
            family = self.__family

        if relpos is None:
            relpos = (0,0,0)

        _position = (
            self.__position[0] + relpos[0],
            self.__position[1] + relpos[1],
            self.__position[2] + relpos[2]
        )

        _child = CreatureBody(size, family, position=_position, parent=self)
        self.__childs.append(_child)
        return _child

    def join(
        self,
        relpos: tuple = None,
        constraints_z: tuple = None,
        motor=None,
    ):
        if not isinstance(self.__parent, CreatureBody):
            raise RuntimeError("Cannot create joint, body has not parent")

        if relpos is None:
            relpos = (0,0,0)

        joint_pos = _tuple_to_chrono_vector((
            self.__position[0] + relpos[0],
            self.__position[1] + relpos[1],
            self.__position[2] + relpos[2]
        ))

        if motor == "torque":
            self.__motor = chrono.ChLinkMotorRotationTorque()
            _motor_frame = chrono.ChFrameD(joint_pos)
            self.__motor.Initialize(
                self.__parent.body, self.__body, _motor_frame
            )

        if constraints_z is not None:
            self.__link = chrono.ChLinkLockRevolute()
            self.__link.GetLimit_Rz().SetActive(True)
            self.__link.GetLimit_Rz().SetMin(constraints_z[0])
            self.__link.GetLimit_Rz().SetMax(constraints_z[1])
            self.__link.Initialize(
                self.__parent.body,
                self.__body,
                chrono.ChCoordsysD(joint_pos, chrono.QUNIT),
            )

        # If no link was set yet, use a fix link
        if self.__link is None:
            self.__link = chrono.ChLinkLockLock()
            self.__link.Initialize(
                self.__parent.body,
                self.__body,
                chrono.ChCoordsysD(joint_pos, chrono.QUNIT),
            )

        return self
