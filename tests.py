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

from walkingsim.simulation import ChronoSimulation

import walkingsim.ground as ground
import walkingsim.creature.genotype as genotype
import walkingsim.creature.phenotype as phenotype
import walkingsim.creature.bone as bone


class TestsGenotypeToPhenotype:
    def __init__(self):
        self.sim = ChronoSimulation('./environments', 'default')
        self.sim.environment.Add(ground.Ground())

    def run_tests(self):
        self.sim.init()
        self.sim.run()

    def build_creature_with_one_part(self):
        #  g = genotype.Genotype()
        #  g.add_node(genotype.GenotypeNode((20, 20, 40)))
        b = bone.Bone((0.3, 1.80, 0.7))
        #  b.SetMass(80)
        self.sim.environment.Add(b)
        # self.env.Add(b)

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
        three_body_creature = phenotype.Phenotype(gen, self.sim.environment)


if __name__ == "__main__":
    t = TestsGenotypeToPhenotype()
    #  t.build_creature_with_one_part()
    t.build_creature_with_two_legs()
    t.run_tests()
