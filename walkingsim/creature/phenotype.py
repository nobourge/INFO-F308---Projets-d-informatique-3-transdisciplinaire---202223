"""
3D PyChrono muscle-based walking simulator
File: phenotype.py
Authors:
    BECKER Robin-Gilles
    BOURGEOIS Noé
    HENRY DE FRAHAN Antoine
    PALMISANO Luca
Description:
    Class for a walking creature.
"""

import walkingsim.creature.bone as bone

import pychrono as chrono


class Phenotype:
    def __init__(self, genotype, env):
        self.genotype = genotype
        self.env = env
        self.bones = []
        self.joints = []
        self._create_morphology()

    def _create_morphology(self):
        # TODO how to choose automatically position of spawned creature wrt
        # the position of the ground?
        # TODO establish rules for joint placement
        # and collision box reductions in procedural generation
        for node in self.genotype.nodes():
            parent_part = None
            if node == 1:  # Root node
                parent_part = bone.Bone(
                    self.genotype.nodes[node]["dimensions"], chrono.ChVectorD(0, 1.9, 0)
                )
                #  parent_part.SetBodyFixed(True)
                parent_part.GetCollisionModel().SetFamily(1)
                self.bones.append(parent_part)
                self.env.Add(parent_part)
            for edge in self.genotype.edges(nbunch=node, data=True):
                new_node = edge[1]
                dimensions = self.genotype.nodes[new_node]["dimensions"]
                new_joint = chrono.ChLinkMotorRotationTorque()
                new_joint_pos = list(edge[2]["position"])
                # TODO different types of joints?
                joint_frame = chrono.ChFrameD(chrono.ChVectorD(*new_joint_pos))
                # TODO how to find position of new part based on parent's pos?
                child_part_pos = new_joint_pos
                child_part_pos[1] -= dimensions[1] / 2
                child_part = bone.Bone(dimensions, chrono.ChVectorD(*child_part_pos))
                child_part.GetCollisionModel().SetFamily(1)
                child_part.GetCollisionModel().SetFamilyMaskNoCollisionWithFamily(1)
                self.bones.append(child_part)
                self.env.Add(child_part)
                new_joint.Initialize(parent_part, child_part, joint_frame)
                self.joints.append(new_joint)
                self.env.Add(new_joint)

        # XXX torque function test
        for i in range(len(self.joints)):
            mod = 1 if i % 2 == 0 else -1
            sin_torque = chrono.ChFunction_Sine(
                0, 1, mod * 90  # phase [rad]  # frequency [Hz]
            )  # amplitude [Nm]
            self.joints[i].SetTorqueFunction(sin_torque)
