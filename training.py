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

    def __init__(self, observation_space, action_space):
        self.exploration_rate = param.EXPLORATION_MAX

        self.action_space = action_space
        self.memory = deque(maxlen=param.MEMORY_SIZE)

        self.model = Sequential()
        self.model.add(Dense(10, input_shape=(observation_space,), activation="relu"))
        self.model.add(Dense(10, activation="relu"))
        self.model.add(Dense(self.action_space, activation="linear"))
        self.model.compile(loss="mse", optimizer=Adam(lr=param.LEARNING_RATE))

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() < self.exploration_rate:
            return random.randrange(self.action_space)
        q_values = self.model.predict(state)
        return np.argmax(q_values[0])

    def experience_replay(self):
        if len(self.memory) < param.BATCH_SIZE:   # le prime venti iterazioni le fa a vuoto: non impara niente (BATCH_SIZE = 20)
            return
        batch = random.sample(self.memory, param.BATCH_SIZE)
        for state, action, reward, state_next, terminal in batch:
            # quindi reward nella formula in wikipedia è Q_vecchio_valore
            q_update = reward

            if not terminal:
                temp = self.model.predict(state_next)[0] # per ogni azione nell'action space , ritorna la qualità associata
                
                # funzione iterativa di aggiornamento della qualità associata ad una coppia stato-azione
                # per la formula corretta vedere https://it.wikipedia.org/wiki/Q-learning
                # NB: non si fa uso di ricom
                # q_update = new Q
                # reward = ricompensa (r_t)
                # NET_GAMMA = fattore di sconto

                q_update = (reward + param.NET_GAMMA * np.amax(temp))
            
            q_values = self.model.predict(state)

            q_values[0][action] = q_update
            self.model.fit(state, q_values, verbose=0)
        self.exploration_rate *= param.EXPLORATION_DECAY
        self.exploration_rate = max(param.EXPLORATION_MIN, self.exploration_rate)

def simulation():

    env = gym.make(param.ENV_NAME)
    virus = Virus(range = param.VIRUS_RANGE, pInfection = param.VIRUS_P_INFECTION, severity = param.VIRUS_SEVERITY, lethality = param.VIRUS_LETHALITY)
    env.initialize(virus = virus, nHouses = param.N_HOUSES) 

    observation_space = env.observation_space.shape[0]
    action_space = env.action_space.n

    dqn_solver = DQNSolver(observation_space, action_space)
    epoch = 0

    sys.stdout = old_stdout
    sys.stderr = old_stderr

    while True:
        epoch += 1
        state = env.reset()
        state = np.reshape(state, [1, observation_space])
        step = 0
        acc_reward = 0

        while True:
            step += 1
            env.render()
            action = dqn_solver.act(state)
            state_next, reward, terminal, info = env.step(action)
            sys.stdout.write("\rStep: " + str(step) + ", Reward: " + str(reward))
            sys.stdout.flush()

            acc_reward += reward

            state_next = np.reshape(state_next, [1, observation_space])
            dqn_solver.remember(state, action, reward, state_next, terminal)
            state = state_next

            if terminal:
                print("\nEpoch: " + str(epoch) + ", exploration: " + str(dqn_solver.exploration_rate) + ", score: " + str(acc_reward / step))
                break


            dqn_solver.experience_replay()

        if (epoch >= param.EPOCHS):
            # serialize model to YAML
            model_yaml = dqn_solver.model.to_yaml()
            with open(param.YAML_PATH, "w") as yaml_file:
                yaml_file.write(model_yaml)
            # serialize weights to HDF5
            dqn_solver.model.save_weights(param.MODEL_PATH)
            print("Saved model to disk")
            return


if __name__ == "__main__":
    simulation()