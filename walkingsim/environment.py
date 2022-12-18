"""
3D PyChrono muscle-based walking simulator
File: environment.py
Authors:
    BECKER Robin-Gilles
    BOURGEOIS Noé
    HENRY DE FRAHAN Antoine
    PALMISANO Luca
Description:
    Class for loading and creating the physics system (= Environment).
"""
import json
import os

import pychrono.core as chrono
from walkingsim._logging import logger


class EnvironmentLoader:
    """Class to load environments from JSON files. 
    
    Environments can be described in JSON files in an agnostic way, completely
    independently of the physics engine used.

    The available engines are: 'chrono'
    """

    def __init__(self, __datapath: str, __engine: str):
        self.__datapath = __datapath
        self.__engine = __engine

        self.__loaders = {
            'chrono': self._load_environment_chrono
        }

    def load_environment(self, __env: str):
        """Loads an environment from a JSON file.

        :param __env: The name of the environment to load
        :return: The environment system
        """
        # try:
        #     with open(os.path.join(self.__datapath, __env + '.json'), 'r') as _file:
        #         _config = json.load(_file)
        # except FileNotFoundError:
        #     logger.error(f'Environment "{__env}" not found.')
        #     # raise FileNotFoundError
        #     # if windows condition:
        #     if os.path.exists(os.path.join(self.__datapath, __env + '.json')):
        #         logger.error(f'Environment "{__env}" not found.')
        #     else:
        #         pass
        #         # adapt path:
        #         # os.path.join(os.getcwd(), 'walkingsim', 'data', 'environments', __env + '.json')
        #     # else
        #         # raise FileNotFoundError
        filename = os.path.join(self.__datapath, f'{__env}.json')

        logger.info(f'Loading environment from {filename}')
        # filename = "../environments/default.json"
        # logger.info(f'Loading environment from {filename}')


        with open(filename, 'r') as fp:
            config = json.load(fp)

        return self.__loaders[self.__engine](config)

    def _load_environment_chrono(self, __config: dict):
        _sys = chrono.ChSystemNSC()
        _sys.Set_G_acc(chrono.ChVectorD(*__config.get('gravity')))

        chrono.ChCollisionModel.SetDefaultSuggestedEnvelope(0.001)
        chrono.ChCollisionModel.SetDefaultSuggestedMargin(0.001)

        return _sys
