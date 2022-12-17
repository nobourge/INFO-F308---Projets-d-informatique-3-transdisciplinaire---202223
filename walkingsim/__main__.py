import walkingsim.ground as ground
from walkingsim.simulation import ChronoSimulation

def main():
    sim = ChronoSimulation('./environments', 'default', './creatures')
    sim.environment.Add(ground.Ground())

    creature = sim.generator.generate_creature('bipede')
    creature.add(sim.environment)

    sim.init()
    sim.run()

if __name__ == '__main__':
    main()
