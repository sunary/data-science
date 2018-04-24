__author__ = 'sunary'


from agent import Agent


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
            is_done = True
        elif next_state in self.obstacles:
            reward = -100
            is_done = True
        else:
            reward = 0
            is_done = False

        self.current_state = next_state
        return next_state, reward, is_done


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