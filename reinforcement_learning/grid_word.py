__author__ = 'sunary'


import random


class Env(object):
    width, height = 5, 5
    direction_move = [[0, 1], [1, 0], [0, -1], [-1, 0]]
    n_actions = len(direction_move)

    def __init__(self):
        self.obstacles = [[2, 3], [3, 2]]
        self.destination = [3, 3]
        self.current_state = None

    def reset(self):
        self.current_state = [0, 0]
        return self.current_state

    def step(self, action):
        next_state = [self.current_state[0] + self.direction_move[action][0],
                      self.current_state[1] + self.direction_move[action][1]]

        next_state[0] = 0 if next_state[0] < 0 else next_state[0]
        next_state[0] = self.n_actions - 1 if next_state[0] > self.width - 1 else next_state[0]
        next_state[1] = 0 if next_state[1] < 0 else next_state[1]
        next_state[1] = self.n_actions - 1 if next_state[1] > self.height - 1 else next_state[1]

        if next_state == self.destination:
            reward = 100
            done = True
        elif next_state in self.obstacles:
            reward = -100
            done = True
        else:
            reward = 0
            done = False

        self.current_state = next_state
        return next_state, reward, done


class Agent(object):

    def __init__(self, actions):
        self.actions = actions
        self.learning_rate = 0.01
        self.discount_factor = 0.9
        self.epsilon = 0.9

        self.q_table = {}

    def get_action(self, state):
        if random.random() > self.epsilon:
            return random.choice(self.actions)
        else:
            self.check_state_exist(state)

            state_action = self.q_table[state]
            return self.argmax(state_action)

    def learn(self, state, action, reward, next_state):
        self.check_state_exist(next_state)

        q1 = self.q_table[state][action]
        q2 = reward + self.discount_factor * max(self.q_table[next_state])

        self.q_table[state][action] += self.learning_rate * (q1 - q2)

    def check_state_exist(self, state):
        if not self.q_table.get(state):
            self.q_table[state] = [0.0] * len(self.actions)

    def argmax(self, state_action):
        list_max_index = []
        max_value = state_action[0]

        for index, value in enumerate(state_action):
            if value > max_value:
                max_value = value
                list_max_index.append(index)
            elif value == max_value:
                list_max_index.append(index)

        return random.choice(list_max_index)

    def print_table(self):
        print ''
        for k, v in self.q_table.iteritems():
            print '{}:{}'.format(k, v)


def run():
    env = Env()
    agent = Agent(actions=range(env.n_actions))

    for i in range(1000):
        state = env.reset()

        while True:
            action = agent.get_action(str(state))

            next_state, reward, done = env.step(action)
            agent.learn(str(state), action, reward, str(next_state))

            state = next_state
            if done:
                if (i + 1) % 100 == 0:
                    agent.print_table()
                break


if __name__ == '__main__':
    run()