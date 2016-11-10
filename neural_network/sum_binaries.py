__author__ = 'sunary'


import numpy as np
import random
from neural_network.model_rnn import RecurrentNeuralNetwork


def simple_rnn():
    largest_number = 2 **8
    binary = np.unpackbits(np.array([range(largest_number)], dtype=np.uint8).T, axis=1)

    rnn = RecurrentNeuralNetwork([2, 16, 2])
    rnn.set_sequence(8)

    for _ in range(10000):
        a = random.randrange(largest_number/2)
        b = random.randrange(largest_number/2)
        c = a + b

        a = binary[a][::-1]
        b = binary[b][::-1]
        c = binary[c][::-1]

        rnn.train([a, b], expected_id=c)

    for _ in range(10):
        a = random.randrange(largest_number/2)
        b = random.randrange(largest_number/2)
        c = a + b

        a = binary[a][::-1]
        b = binary[b][::-1]
        c = binary[c][::-1]

        print rnn.train([a, b])
        print c
        print '--'


if __name__ == '__main__':
    simple_rnn()