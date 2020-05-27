import random
import gym
import gym_foo
import numpy as np
from collections import deque

from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

import time

# for storing the NN weights
from keras.models import model_from_yaml
import os

#from scores.score_logger import ScoreLogger

ENV_NAME = "foo-v0"

GAMMA = 0.95
LEARNING_RATE = 0.001

MEMORY_SIZE = 1000000
BATCH_SIZE = 20

EXPLORATION_MAX = 1.0
EXPLORATION_MIN = 0.01
EXPLORATION_DECAY = 0.995

class DQNSolver:

    def __init__(self, observation_space, action_space):
        self.exploration_rate = EXPLORATION_MAX

        self.action_space = action_space
        self.memory = deque(maxlen=MEMORY_SIZE)

        self.model = Sequential()
        self.model.add(Dense(10, input_shape=(observation_space,), activation="relu"))
        self.model.add(Dense(10, activation="relu"))
        self.model.add(Dense(self.action_space, activation="linear"))
        self.model.compile(loss="mse", optimizer=Adam(lr=LEARNING_RATE))

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() < self.exploration_rate:
            return random.randrange(self.action_space)
        q_values = self.model.predict(state)
        return np.argmax(q_values[0])

    def experience_replay(self):
        if len(self.memory) < BATCH_SIZE:   # le prime venti iterazioni le fa a vuoto: non impara niente (BATCH_SIZE = 20)
            return
        batch = random.sample(self.memory, BATCH_SIZE)
        for state, action, reward, state_next, terminal in batch:
            # quindi reward nella formula in wikipedia è Q_vecchio_valore
            q_update = reward

            if not terminal:
                #print("state: " + str(state))
                temp = self.model.predict(state_next)[0] # per ogni azione nell'action space , ritorna la qualità associata
                #print(str(temp) + " and with max: " + str(np.amax(temp)))
                #input()
                # funzione iterativa di aggiornamento della qualità associata ad una coppia stato-azione
                # per la formula corretta vedere https://it.wikipedia.org/wiki/Q-learning
                # NB: non si fa uso di ricom
                # q_update = new Q
                # reward = ricompensa (r_t)
                # GAMMA = fattore di sconto

                q_update = (reward + GAMMA * np.amax(temp))
            
            q_values = self.model.predict(state)

            q_values[0][action] = q_update
            self.model.fit(state, q_values, verbose=0)
        self.exploration_rate *= EXPLORATION_DECAY
        self.exploration_rate = max(EXPLORATION_MIN, self.exploration_rate)

def cartpole():
    env = gym.make(ENV_NAME)
    #score_logger = ScoreLogger(ENV_NAME)    

    observation_space = env.observation_space.shape[0]
    action_space = env.action_space.n

    dqn_solver = DQNSolver(observation_space, action_space)
    run = 0
    while True:
        run += 1
        state = env.reset()
        state = np.reshape(state, [1, observation_space])
        step = 0
        while True:
            step += 1
            #env.render()
            action = dqn_solver.act(state)
            state_next, reward, terminal, info = env.step(action)
            reward = reward if not terminal else -reward
            state_next = np.reshape(state_next, [1, observation_space])
            dqn_solver.remember(state, action, reward, state_next, terminal)
            state = state_next
            if terminal:
                print("Run: " + str(run) + ", exploration: " + str(dqn_solver.exploration_rate) + ", score: " + str(step))
                #score_logger.add_score(step, run)
                break
            dqn_solver.experience_replay()
        if (step>1000):
            # serialize model to YAML
            model_yaml = dqn_solver.model.to_yaml()
            with open("model.yaml", "w") as yaml_file:
                yaml_file.write(model_yaml)
            # serialize weights to HDF5
            dqn_solver.model.save_weights("model.h5")
            print("Saved model to disk")
            exit()
            run += 1
            state = env.reset()
            state = np.reshape(state, [1, observation_space])
            step = 0
            while True:
                step += 1
                env.render()
                time.sleep(0.02)
                action = dqn_solver.predict(state)
                state_next, reward, terminal, info = env.step(action)
                reward = reward if not terminal else -reward
                state_next = np.reshape(state_next, [1, observation_space])
                dqn_solver.remember(state, action, reward, state_next, terminal)
                state = state_next
                if terminal:
                    print("Run: " + str(run) + ", exploration: " + str(dqn_solver.exploration_rate) + ", score: " + str(step))
                    #score_logger.add_score(step, run)
                    break
                dqn_solver.experience_replay()


if __name__ == "__main__":
    cartpole()