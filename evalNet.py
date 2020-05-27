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

ENV_NAME = "foo-v0"
LEARNING_RATE = 0.001

env = gym.make(ENV_NAME)

observation_space = env.observation_space.shape[0]
action_space = env.action_space.n

# load YAML and create model
yaml_file = open('model.yaml', 'r')
loaded_model_yaml = yaml_file.read()
yaml_file.close()
loaded_model = model_from_yaml(loaded_model_yaml)
# load weights into new model
loaded_model.load_weights("model.h5")
print("Loaded model from disk")


loaded_model.compile(loss="mse", optimizer=Adam(lr=LEARNING_RATE))

state = env.reset()
state = np.reshape(state, [1, observation_space])
step = 0

while True:
	step+=1
	print(step)
	env.render()
	time.sleep(0.1)
	action = np.argmax(loaded_model.predict(state))
	state_next, reward, terminal, info = env.step(action)
	if terminal:
		break
	state_next = np.reshape(state_next, [1, observation_space])
	state = state_next