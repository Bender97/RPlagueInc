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

from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

# for storing the NN weights
from keras.models import model_from_yaml

import parameters as param
import engine.envs.render as render

class DQNSolver:

    def __init__(self):
        yaml_file = open(param.YAML_PATH, 'r')
        loaded_model_yaml = yaml_file.read()
        yaml_file.close()
        loaded_model = model_from_yaml(loaded_model_yaml)
        # load weights into new model
        loaded_model.load_weights(param.MODEL_PATH)
        self.model = loaded_model


    def act(self, state):
        q_values = self.model.predict(state)
        print(q_values)
        return np.argmax(q_values[0])


def simulation():

    env = gym.make(param.ENV_NAME)
    virus = Virus(range = param.VIRUS_RANGE, pInfection = param.VIRUS_P_INFECTION, severity = param.VIRUS_SEVERITY, lethality = param.VIRUS_LETHALITY)
    env.initialize(virus = virus, nHouses = param.N_HOUSES) 

    dqn_solver = DQNSolver()

    sys.stdout = old_stdout
    sys.stderr = old_stderr

    observation_space = env.observation_space.shape[0]
    action_space = env.action_space.n
   
    state = env.reset()
    state = np.reshape(state, [1, observation_space])
    step = 0
    acc_reward = 0

    while True:
        step += 1
        env.render()
        action = dqn_solver.act(state)
        print (action)
        state_next, reward, terminal, info = env.step(action)
        sys.stdout.write("\rStep: " + str(step) + ", Reward: " + str(reward))
        sys.stdout.flush()

        acc_reward += reward

        state_next = np.reshape(state_next, [1, observation_space])
        state = state_next

        if terminal:
            print("\nTerminated with score: " + str(acc_reward / step))
            break




if __name__ == "__main__":
    simulation()