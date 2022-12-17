from walkingsim.simulation import ChronoSimulation

def main():
    sim = ChronoSimulation('./environments', 'default')

    # TODO: Do something

    sim.init()
    sim.run()

if __name__ == '__main__':
    main()
