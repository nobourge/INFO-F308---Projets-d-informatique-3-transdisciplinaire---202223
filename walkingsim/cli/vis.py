from loguru import logger

def visualize_ga(*
                 , date: str = None
                 , timestep: float = 1e-2
                 , delay: int = 0):
    logger.info("Visualizing GA")
    logger.debug(f"date: {date}")
    logger.debug(f"timestep: {timestep}")
    logger.debug(f"delay: {delay}")
    from walkingsim.algorithms.ga import GeneticAlgorithm

    model = GeneticAlgorithm.load(
        date=date, visualize=True, timestep=timestep, ending_delay=delay
    )
    model.visualize()


def visualize_ppo(*, date: str, timestep: float = 1e-2, delay: int = 0):
    from walkingsim.algorithms.ppo import PPO_Algo

    model = PPO_Algo.load(date=date, visualize=True, timestep=timestep)
    model.visualize()
