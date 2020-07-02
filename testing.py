import sys
import os

old_stdout = sys.stdout
sys.stdout = open(os.devnull, "w")
old_stderr = sys.stderr
sys.stderr = open(os.devnull, "w")
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import random
import gym
import engine.envs.engineEnv
import time
import random
import engine.choices as choices
from engine.virus import Virus
import numpy as np
from collections import deque

import parameters as param
import engine.envs.render as render

from training import DQNSolver

sys.stdout = old_stdout
sys.stderr = old_stderr


def simulation():

    env = gym.make(param.ENV_NAME)
    virus = Virus(range = param.VIRUS_RANGE, pInfection = param.VIRUS_P_INFECTION, severity = param.VIRUS_SEVERITY, lethality = param.VIRUS_LETHALITY)
    env.initialize(virus = virus, nHouses = param.N_HOUSES)

    dqn_solver = DQNSolver(False)
    dqn_solver.read_model()

    observation_space = env.observation_space.shape[0]
    action_space = env.action_space.n
   
    curr_state = env.reset()
    state = deque()
    for k in range(param.STATUS_WINDOW):
        state.append(curr_state)
    # end for

    step = 0
    acc_reward = 0

    while True:
        step += 1
        env.render()

        array_state = np.reshape(list(state), (1, param.STATUS_WINDOW, observation_space))

        action = dqn_solver.act(array_state)
        print (action)
        curr_state_next, reward, terminal, info = env.step(action)
        sys.stdout.write("\rStep: " + str(step) + ", Reward: " + str(reward))
        sys.stdout.flush()

        state_next = state.copy()
        state_next.popleft()
        state_next.append(curr_state_next)

        acc_reward += reward

        state = state_next

        if terminal:
            print("\nTerminated with score: " + str(acc_reward / step))
            break




if __name__ == "__main__":
    simulation()