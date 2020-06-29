from gym.envs.registration import registry, register, make, spec

register(
    id='engine-v0',
    entry_point='engine.envs:EngineEnv',
)