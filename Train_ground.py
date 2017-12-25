from Desk import T9Desk
from DQNAgent import DQNAgent
import numpy as np
EPISODES = 5000


def prRed(prt): print("\033[91m {}\033[00m" .format(prt))
def prGreen(prt): print("\033[92m {}\033[00m" .format(prt))
def prYellow(prt): print("\033[93m {}\033[00m" .format(prt))
def prLightPurple(prt): print("\033[94m {}\033[00m" .format(prt))
def prPurple(prt): print("\033[95m {}\033[00m" .format(prt))
def prCyan(prt): print("\033[96m {}\033[00m" .format(prt))
def prLightGray(prt): print("\033[97m {}\033[00m" .format(prt))
def prBlack(prt): print("\033[98m {}\033[00m" .format(prt))


if __name__ == '__main__':
    env = T9Desk()
    state_size = env.observation_space
    action_size = env.action_space_size
    print("state_size ", state_size)
    print("action_size ", action_size)
    agent = DQNAgent(state_size, action_size)
    # agent.load("T9-dqn.h5")
    batch_size = 32 * 3

    for e in range(EPISODES):
        state = env.reset()
        # print("state = env.reset() ", state)
        state = np.reshape(state, [1, state_size])
        # print("state ", state)
        done = False
        while not done:
            # env.render()
            action_0to8 = agent.act(state)
            next_state, reward, done, _ = env.step(action_0to8 + 1, symmetric_state=True)
            # print("action ", action_0to8 + 1)
            # print(next_state, reward, done)
            reward = reward if not done else -10
            next_state = np.reshape(next_state, [1, state_size])
            agent.remember(state, action_0to8, reward, next_state, done)
            state = next_state
            if done:
                prGreen("episode: {}/{}, score: {}, e: {:.4}".format(e, EPISODES, 'time', agent.epsilon))
        if len(agent.memory) > batch_size:
            agent.replay(batch_size)
        if e % 10 == 0:
            agent.save("T9-dqn.h5")

