"""
3D PyChrono muscle-based walking simulator
File: utils.py
Authors:
    BECKER Robin-Gilles
    BOURGEOIS Noé
    HENRY DE FRAHAN Antoine
    PALMISANO Luca
Description:
    Utility functions.
"""

import math

def distance(a, b):
    return math.sqrt(
        (a[0] + b[0]) ** 2 + (a[1] + b[1]) ** 2 + (a[2] + b[2]) ** 2
    )
