import gym
import engine.envs.engineEnv
import time
import random
import engine.choices as choices
from engine.virus import Virus

covid19 = Virus(range = 2, pInfection = 0.1, severity = 0.2, lethality = 0.1)
black_plague = Virus(range = 3, pInfection = 0.6, severity = 0.9, lethality = 0.7)
measles = Virus(range = 30, pInfection = 0.9, severity = 0.9, lethality = 0.1)

virus = covid19

#create the cartpole environment
env = gym.make("engine-v0")

env.initialize(virus = virus, nHouses = 100, render = env.RENDER_ALL_DAILY)

observation = env.reset()

for _ in range(1000):
    env.render()
    action = env.action_space.sample() # your agent here (this takes random actions)
    observation, reward, done, info = env.step(0)

    
    #choices.makeChoice(action[0], action[1],self) # action in formato [type,choice]
    #choices.makeChoice(random.randint(0,1), random.randint(0,6), env)
    
    if (env.steps_done > 10):
        choices.makeChoice(choices.ENACT, choices.CH_CL_WORK, env)
        choices.makeChoice(choices.ENACT, choices.CH_CL_LEISURES, env)
        choices.makeChoice(choices.ENACT, choices.CH_CL_SCHOOLS, env)
        choices.makeChoice(choices.ENACT, choices.CH_MAND_MASKS, env)
        choices.makeChoice(choices.ENACT, choices.CH_QUAR_INF, env)
        choices.makeChoice(choices.ENACT, choices.CH_MAND_DIST, env)

    print("inf: " + str(observation[1]))
    print("R0: " + str(observation[4]))

    #print(str(reward) + " - " + str(done))
    if (reward==0):
        input()

    #time.sleep(0.1)
    if done:
        observation = env.reset()
env.close()
