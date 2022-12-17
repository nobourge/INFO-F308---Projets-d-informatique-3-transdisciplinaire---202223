"""
3D PyChrono muscle-based walking simulator
File: environment.py
Authors:
    BECKER Robin-Gilles
    BOURGEOIS Noé
    HENRY DE FRAHAN Antoine
    PALMISANO Luca
Description:
    Class for the complete physics system.
"""
import json
import os

import pychrono.core as chrono

class EnvironmentLoader:

    def __init__(self, __datapath: str, __engine: str):
        self.__datapath = __datapath
        self.__engine = __engine

        self.__loaders = {
            'chrono': self._load_environment_chrono
        }

    def load_environment(self, __env: str):
        filename = os.path.join(self.__datapath, f'{__env}.json')
        with open(filename, 'r') as fp:
            config = json.load(fp)

        return self.__loaders[self.__engine](config)

    def _load_environment_chrono(self, __config: dict):
        _sys = chrono.ChSystemNSC()
        _sys.Set_G_acc(chrono.ChVectorD(*__config.get('gravity')))

        chrono.ChCollisionModel.SetDefaultSuggestedEnvelope(0.001)
        chrono.ChCollisionModel.SetDefaultSuggestedMargin(0.001)

        return _sys
