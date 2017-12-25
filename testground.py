from Desk import T9Desk
from DQNAgent import DQNAgent
import numpy as np


env = T9Desk("random_1", "Deep QN_2")
state_size = env.observation_space
action_size = env.action_space_size
agent = DQNAgent(state_size, action_size)
agent.load("T9-dqn.h5")

for i in range(100):
    state = env.reset(False)
    done = False
    # print(i)
    while not done:
        pr, op = env.who_moves_str
        if pr == 'p2':
            action_space = env.action_space[pr]
            action = action_space[np.random.randint(0, action_space.size)]
        else:
            action = agent.act(state) + 1
        next_state, reward, done, _ = env.step(action)
        env.render()
    score_sum = env.win_count['p1'] + env.win_count['p2'] + env.win_count['draw']
