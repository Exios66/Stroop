# /training/train.py
import torch
from agents.high_level_agent import HighLevelAgent
from agents.low_level_agent import LowLevelAgent
from environments.custom_env import CustomEnv
from collections import deque

def train_hierarchy():
    env = CustomEnv()
    high_level_agent = HighLevelAgent(env.state_size, env.option_size)
    low_level_agents = [LowLevelAgent(env.state_size, env.action_size) for _ in range(env.num_agents)]
    memory = deque(maxlen=10000)

    for episode in range(1000):
        state = env.reset()
        done = False
        total_reward = 0
        while not done:
            option = high_level_agent.select_option(state)
            for agent in low_level_agents:
                action = agent.select_action(state)
                next_state, reward, done, _ = env.step(action)
                agent.update_q_values(state, action, reward, next_state, done)
                state = next_state
                total_reward += reward
            high_level_agent.update_q_values(state, option, reward, next_state, done)
        print(f"Episode {episode}, Total Reward: {total_reward}")
