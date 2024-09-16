# /environments/custom_env.py
import gym
from gym import spaces
import numpy as np

class CustomEnv(gym.Env):
    def __init__(self):
        self.state_size = 4  # Example state size
        self.option_size = 2  # Number of high-level options
        self.action_size = 2  # Number of actions for low-level agents
        self.num_agents = 3  # Example number of agents

    def step(self, action):
        next_state = np.random.rand(self.state_size)
        reward = np.random.rand()
        done = np.random.choice([True, False])
        return next_state, reward, done, {}

    def reset(self):
        return np.random.rand(self.state_size)
