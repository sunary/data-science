__author__ = 'sunary'


import numpy as np
import random
from neural_network.model_rnn import RecurrentNeuralNetwork


def simple_rnn():
    largest_number = 2 **8
    binary = np.unpackbits(np.array([range(largest_number)], dtype=np.uint8).T, axis=1)

    rnn = RecurrentNeuralNetwork([2, 3, 2])
    for _ in range(10000):
        a = random.randrange(largest_number/2)
        b = random.randrange(largest_number/2)
        c = a + b

        a = binary[a]
        b = binary[b]
        c = binary[c]

        a = [a[len(a) - i - 1] for i in range(len(a))]
        b = [b[len(b) - i - 1] for i in range(len(b))]
        c = [c[len(c) - i - 1] for i in range(len(c))]

    for _ in range(10):
        a = random.randrange(largest_number/2)
        b = random.randrange(largest_number/2)
        c = a + b

        a = binary[a]
        b = binary[b]
        c = binary[c]

        a = [a[len(a) - i - 1] for i in range(len(a))]
        b = [b[len(b) - i - 1] for i in range(len(b))]
        c = [c[len(c) - i - 1] for i in range(len(c))]

        print rnn.train([a, b])
        print c
        print '--'


if __name__ == '__main__':
    simple_rnn()