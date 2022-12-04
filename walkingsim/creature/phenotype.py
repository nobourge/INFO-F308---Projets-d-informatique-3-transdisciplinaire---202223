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
        for node in self.genotype.nodes():
            if node == 1:  # Root node
                root_part = bone.Bone(
                    self.genotype.nodes[node]["dimensions"], chrono.ChVectorD(0, 1.9, 0)
                )
                root_part.SetBodyFixed(True)
                self.bones.append(root_part)
                self.env.Add(root_part)
            for edge in self.genotype.edges(nbunch=node, data=True):
                new_node = edge[1]
                dimensions = self.genotype.nodes[new_node]["dimensions"]
                # TODO how to find position of new part based on parent's pos?
                pos = list(edge[2]["position"])
                pos[1] -= dimensions[1] / 2
                new_part = bone.Bone(dimensions, chrono.ChVectorD(*pos))
                self.bones.append(new_part)
                self.env.Add(new_part)
                print(pos)
