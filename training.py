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
from keras.layers import Dense, Conv1D, MaxPooling1D, Flatten, Dropout
from keras.optimizers import Adam

# for storing the NN weights
from keras.models import model_from_yaml

import parameters as param
import engine.envs.render as render

sys.stdout = old_stdout
sys.stderr = old_stderr

class DQNSolver:

    def __init__(self, in_training):
        self.in_training = in_training
        

    def compile_model(self, observation_space, action_space):
        self.exploration_rate = param.EXPLORATION_MAX

        self.action_space = action_space
        self.memory = deque(maxlen=param.MEMORY_SIZE)

        self.model = Sequential()
        self.model.add(Conv1D(filters=64, kernel_size=3, input_shape=observation_space, activation="relu"))
        self.model.add(Conv1D(filters=64, kernel_size=3, activation="relu"))
        self.model.add(MaxPooling1D(pool_size=2))
        self.model.add(Flatten())
        self.model.add(Dropout(0.25))
        self.model.add(Dense(50, activation="relu"))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(self.action_space, activation="linear"))
        self.model.compile(loss="mse", optimizer=Adam(lr=param.LEARNING_RATE))
        self.model.summary()

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state, available_choices):

        # if the DQN has to explore, choose a random choice from the available
        if self.in_training and np.random.rand() < self.exploration_rate:
            ch = [k for k in range(len(available_choices)) if available_choices[k]]

            return random.choice(ch)

        # compute the mask as the logical inverse of available choices
        array_action_mask = np.logical_not(available_choices)
        # predict the Q values
        q_values = self.model.predict(state)
        # mask the available choices and fill the not available with NaN
        q_values = np.ma.masked_array(data=q_values[0], mask=array_action_mask, fill_value=np.nan)
        # return the argmax of the non NaN values
        choice = np.nanargmax(q_values)
        return choice


    def write_model(self):
        # serialize model to YAML
        model_yaml = self.model.to_yaml()
        with open(param.YAML_PATH, "w") as yaml_file:
            yaml_file.write(model_yaml)
        # serialize weights to HDF5
        self.model.save_weights(param.MODEL_PATH)


    def read_model(self):
        yaml_file = open(param.YAML_PATH, 'r')
        loaded_model_yaml = yaml_file.read()
        yaml_file.close()
        loaded_model = model_from_yaml(loaded_model_yaml)
        # load weights into new model
        loaded_model.load_weights(param.MODEL_PATH)
        self.model = loaded_model
        self.model.summary()


    def experience_replay(self):
        if len(self.memory) < param.BATCH_SIZE:   # le prime venti iterazioni le fa a vuoto: non impara niente
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

    dqn_solver = DQNSolver(True)
    dqn_solver.compile_model((param.STATUS_WINDOW, observation_space), action_space)

    epoch = 0

    while True:
        epoch += 1
        curr_state, info = env.reset()
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

            print(info['allowed_choices'])

            action = dqn_solver.act(array_state, info['allowed_choices'])

            curr_state_next, reward, terminal, info = env.step(action)
            sys.stdout.write("\rStep: " + str(step) + ", Reward: " + str(reward))
            sys.stdout.flush()

            state_next = state.copy()
            state_next.popleft()
            state_next.append(curr_state_next)

            acc_reward += reward

            array_state_next = np.reshape(list(state_next), (1, param.STATUS_WINDOW, observation_space))

            #state_next = np.reshape(state_next, [1, observation_space])
            dqn_solver.remember(array_state, action, reward, array_state_next, terminal)
            state = state_next

            if terminal:
                print("\nEpoch: " + str(epoch) + ", exploration: " + str(dqn_solver.exploration_rate) + ", score: " + str(acc_reward / step))
                break


            dqn_solver.experience_replay()

        if (epoch >= param.EPOCHS):
            dqn_solver.write_model()
            print("Saved model to disk")
            return


if __name__ == "__main__":
    simulation()