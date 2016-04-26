__author__ = 'sunary'


import random
from neural_network.model_rnn import RecurrentNeuralNetwork


def to_bins(num):
    array = []
    while num:
        array.append(num %2)
        num /= 2

    array = reversed(array)
    array = [a for a in array]
    array[:0] = [0] *(8 - len(array))
    return array


def simple_rnn():
    rnn = RecurrentNeuralNetwork([2, 5, 2])
    binary_dim = 8
    largest_number = pow(2, binary_dim)

    for _ in range(500):
        a = random.randrange(0, largest_number/2)
        b = random.randrange(0, largest_number/2)
        c = a + b
        a = to_bins(a)
        b = to_bins(b)
        c = to_bins(c)

        print rnn.train(zip(a, b), c)


if __name__ == '__main__':
    simple_rnn()