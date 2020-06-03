import gym
import engine.envs.engineEnv
import time
from engine.virus import Virus

virus = Virus(range = 3, pInfection = 1 , healthParams = 1, healingParams = 1)


#create the cartpole environment
env = gym.make("engine-v0")

observation = env.reset(nHouses = 30)

env.initialize(virus = virus)

for _ in range(1000):
    env.render()
    action = env.action_space.sample() # your agent here (this takes random actions)
    observation, reward, done, info = env.step(action)
    
    print("inf: " + str(observation[1][1]))
    print("R0: " + str(observation[4][1]))

    #print(str(reward) + " - " + str(done))
    if (reward==0):
        input()

    #time.sleep(0.1)
    if done:
        observation = env.reset()
env.close()
