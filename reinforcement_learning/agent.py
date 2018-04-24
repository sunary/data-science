__author__ = 'sunary'


import random


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

    def check_state_exist(self, state):
        if not self.q_table.get(state):
            self.q_table[state] = [0.0] * len(self.actions)

    def print_table(self):
        for k, v in self.q_table.iteritems():
            print '{}:{}'.format(k, v)