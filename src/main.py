"""
3D PyChrono muscle-based walking simulator
File: main.py
Authors:
    BECKER Robin-Gilles
    BOURGEOIS Noé
    HENRY DE FRAHAN Antoine
    PALMISANO Luca
Description:
    Program entry point. Builds the physics system
    and launches the visualiser.
"""

from environment import Environment
from visualiser import Visualiser


def main():
    environment = Environment()
    visuals = Visualiser(environment)
    visuals.run()


if __name__ == "__main__":
    main()