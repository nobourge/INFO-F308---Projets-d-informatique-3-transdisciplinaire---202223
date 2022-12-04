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


class Phenotype:
    def __init__(self, genotype):
        self.genotype = genotype
        self._create_morphology()

    def _create_morphology(self):
        for c in self.genotype.edges.items():
            print(c)
