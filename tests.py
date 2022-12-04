"""
3D PyChrono muscle-based walking simulator
File: test_genotype_to_phenotype.py
Authors:
    BECKER Robin-Gilles
    BOURGEOIS Noé
    HENRY DE FRAHAN Antoine
    PALMISANO Luca
Description:
    Manual tests for spawning a creature (its phenotype) based on a
    genotype.
"""

import pychrono as chrono

import walkingsim.environment as environment
import walkingsim.visualiser as visualiser
import walkingsim.creature.genotype as genotype
import walkingsim.creature.phenotype.bone as bone


class TestsGenotypeToPhenotype:
    def __init__(self):
        self.env = environment.Environment()

    def run_tests(self):
        self.visuals = visualiser.Visualiser(self.env)
        self.visuals.run()

    def build_creature_with_one_part(self):
        #  g = genotype.Genotype()
        #  g.add_node(genotype.GenotypeNode((20, 20, 40)))
        b = bone.Bone((0.3, 1.80, 0.7))
        #  b.SetMass(80)
        self.env.Add(b)

    def build_creature_with_two_legs(self):
        # TODO make a class/struct for nodes and connetions
        nodes = [
            (
                1,
                {
                    "dimensions": (0.3, 1.0, 1.0),
                    "joint_type": None,
                    "joint_limits": None,
                    "recursive_limit": 0,
                    "neurons": None,
                    "connections": [],
                },
            ),
            (
                2,
                {
                    "dimensions": (0.3, 1.4, 0.2),
                    "joint_type": "revolute",
                    "joint_limits": None,
                    "recursive_limit": 0,
                    "neurons": None,
                    "connections": [],
                },
            ),
        ]

        connections = [
            (
                1,
                2,
                {
                    "position": (0, 1.4, -0.2),
                    "orientation": None,
                    "scale": None,
                    "reflection": None,
                    "terminal_only": True,
                },
            ),
            (
                1,
                2,
                {
                    "position": (0, 1.4, 0.2),
                    "orientation": None,
                    "scale": None,
                    "reflection": None,
                    "terminal_only": True,
                },
            ),
        ]
        gen = genotype.Genotype(nodes, connections)
        # TODO establish rules for joint placement
        # and collision box reductions in procedural generation
        trunk = bone.Bone((0.3, 1.0, 1.0), chrono.ChVectorD(0, 1.9, 0))
        trunk.SetBodyFixed(True)
        self.env.Add(trunk)
        # left leg
        leg1 = bone.Bone((0.3, 1.4, 0.2), chrono.ChVectorD(0, 0.7, -0.2))
        leg1.GetCollisionModel().ClearModel()
        leg1.GetCollisionModel().AddBox(
            bone.Bone.bone_material,
            0.15,
            0.35,
            0.1,
            chrono.ChVectorD(0, -0.35, 0),
        )
        leg1.GetCollisionModel().BuildModel()
        self.env.Add(leg1)
        link = chrono.ChLinkMotorRotationTorque()
        frame = chrono.ChFrameD(chrono.ChVectorD(0, 1.4, -0.2))
        link.Initialize(trunk, leg1, frame)
        self.env.Add(link)
        # The torque(time) function:
        torquetime = chrono.ChFunction_Sine(
            0, 2, 90  # phase [rad]  # frequency [Hz]
        )  # amplitude [Nm]
        link.SetTorqueFunction(torquetime)

        # right leg
        leg2 = bone.Bone((0.3, 1.4, 0.2), chrono.ChVectorD(0, 0.7, 0.2))
        leg2.GetCollisionModel().ClearModel()
        leg2.GetCollisionModel().AddBox(
            bone.Bone.bone_material,
            0.15,
            0.35,
            0.1,
            chrono.ChVectorD(0, -0.35, 0),
        )
        leg2.GetCollisionModel().BuildModel()
        self.env.Add(leg2)
        link2 = chrono.ChLinkMotorRotationTorque()
        frame2 = chrono.ChFrameD(chrono.ChVectorD(0, 1.4, 0.2))
        link2.Initialize(trunk, leg2, frame2)
        self.env.Add(link2)
        action_b = chrono.ChFunction_Const(-30)
        link2.SetTorqueFunction(action_b)


if __name__ == "__main__":
    t = TestsGenotypeToPhenotype()
    #  t.build_creature_with_one_part()
    t.build_creature_with_two_legs()
    t.run_tests()
