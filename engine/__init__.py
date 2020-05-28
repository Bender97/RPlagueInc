from gym.envs.registration import register

register(
    id='engine-v0',
    entry_point='engine.envs:EngineEnv',
)