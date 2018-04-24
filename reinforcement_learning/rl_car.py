__author__ = 'sunary'


import random


class Car(object):

    def reset(self):
        pass

    def next_move(self, action):
        pass

    def get_status(self):
        return 0

    def current_state(self):
        pass


class Env(object):

    moves = [-3, -2, -1, 0, 1, 2, 3]
    n_actions = len(moves)

    def __init__(self):
        self.current_state = None

        self.car = Car()

    def reset(self):
        self.car.reset()
        return self.car.current_state()

    def step(self, action):
        self.car.next_move(action)

        car_status = self.car.get_status()
        if car_status == -1:
            is_done = True
            reward = -100
        elif car_status == 0:
            is_done = False
            reward = 0
        elif car_status == 1:
            is_done = True
            reward = 100
        else:
            raise Exception('Invalid car status')

        return self.car.current_state(), reward, is_done


def run():
    env = Env()
    agent = Agent(actions=range(env.n_actions))

    for i in range(1000):
        state = env.reset()
        action = agent.get_action(str(state))

        next_state, reward, done = env.step(action)
        agent.learn(str(state), action, reward, str(next_state))

        state = next_state
        if done:
            if (i + 1) % 100 == 0:
                agent.print_table()
            break