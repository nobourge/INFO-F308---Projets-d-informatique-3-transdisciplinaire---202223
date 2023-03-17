from gymnasium.envs.registration import register

register(
    id="quadrupede-v0",
    entry_point="walkingsim.simulation.gym:Gym_Simulation",
    max_episode_steps=300,
)
