import gym
import engine.envs.engineEnv
import time
import random
import engine.choices as choices
from engine.virus import Virus

virus = Virus(range = 3, pInfection = 1 , healthParams = 1, healingParams = 1)


#create the cartpole environment
env = gym.make("engine-v0")

observation = env.reset(nHouses = 10)

env.initialize(virus = virus)

for _ in range(1000):
    env.render()
    action = env.action_space.sample() # your agent here (this takes random actions)
    observation, reward, done, info = env.step(action)
    
    #choices.makeChoice(action[0], action[1],self) # action in formato [type,choice]
    choices.makeChoice(random.randint(0,1), random.randint(0,6), env)

    print("inf: " + str(observation[1]))
    print("R0: " + str(observation[4]))

    #print(str(reward) + " - " + str(done))
    if (reward==0):
        input()

    #time.sleep(0.1)
    if done:
        observation = env.reset(nHouses = 40)
env.close()
