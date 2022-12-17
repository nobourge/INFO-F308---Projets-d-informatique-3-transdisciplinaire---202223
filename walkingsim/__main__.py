import sys

import walkingsim.ground as ground
from walkingsim.simulation import ChronoSimulation

def main():
    environment, creature_name = 'default', 'bipede'
    if len(sys.argv) >= 2:
        environment = sys.argv[1]
    if len(sys.argv) >= 3:
        creature_name = sys.argv[2]

    sim = ChronoSimulation('./environments', environment, './creatures')
    sim.environment.Add(ground.Ground())

    creature = sim.generator.generate_creature(creature_name)
    creature.add(sim.environment)

    sim.init()
    sim.run()

if __name__ == '__main__':
    main()
