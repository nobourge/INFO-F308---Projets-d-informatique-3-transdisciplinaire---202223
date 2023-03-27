# simulation & genetic algorithm parameters meta heuristical
# optimization research

import argparse
import logging

from walkingsim.cli import parser

# meta heuristic class
class MetaHeuristic:
    def __init__(self, args):
        self.args = args

    def run(self):
        # arguments all trough loop in increasing generations and
        # population size and then compare the results and select the
        # best one
        pass
