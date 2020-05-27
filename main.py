import gym
import gym_foo
import time
#create the cartpole environment
env = gym.make("foo-v0")
#initialize the environment and get the first observation
observation = env.reset()
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

    time.sleep(0.5)
    if done:
        observation = env.reset()
env.close()