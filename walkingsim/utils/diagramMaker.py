# class running a batch of either simulations or solutions
# retreiving data and saving it in a diagram file

# Path: walkingsim\utils\diagramMaker.py
# Compare this snippet from walkingsim\cli\vis.py:
# # visualization
import argparse
import logging

from walkingsim.cli import parser

class diagramMaker:
    def __init__(self, args):
        self.args = args

    def run(self):
        # arguments all trough loop in increasing generations and
        # population size and then compare the results and select the
        # best one
        pass
