# /agents/low_level_agent.py
import numpy as np
import torch
from models.q_network import QNetwork

class LowLevelAgent:
    def __init__(self, state_size, action_size, learning_rate=0.001):
        self.q_network = QNetwork(state_size, action_size)
        self.target_network = QNetwork(state_size, action_size)
        self.optimizer = torch.optim.Adam(self.q_network.parameters(), lr=learning_rate)
        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01
        self.gamma = 0.99

    def select_action(self, state):
        if np.random.rand() < self.epsilon:
            return np.random.choice(range(self.q_network.action_size))
        else:
            with torch.no_grad():
                return self.q_network(torch.FloatTensor(state)).argmax().item()

    def update_q_values(self, state, action, reward, next_state, done):
        q_values = self.q_network(torch.FloatTensor(state))
        next_q_values = self.target_network(torch.FloatTensor(next_state))

        target = reward + (1 - done) * self.gamma * next_q_values.max().item()
        loss = torch.nn.functional.mse_loss(q_values[action], torch.FloatTensor([target]))

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
