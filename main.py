import gym
import engine.envs.engineEnv
import time
from engine.virus import Virus

virus = Virus(range = 40, pInfection = 1 , healthParams = 1, healingParams = 1)


#create the cartpole environment
env = gym.make("engine-v0")
observation = env.reset(nLocation = 15)
env.initialize(nLocation = 5, virus = virus)
#initialize the environment and get the first observation
#>[-0.01691473  0.04548045 -0.02779662  0.04136515]

'''
print(observation)
env.render()
input()
exit()
'''

for _ in range(1000):
    env.render()
    action = env.action_space.sample() # your agent here (this takes random actions)
    observation, reward, done, info = env.step(action)

    print(str(reward) + " - " + str(done))
    if (reward==0):
        input()

    time.sleep(0.1)
    if done:
        observation = env.reset()
env.close()
