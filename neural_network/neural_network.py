__author__ = 'sunary'


import numpy as np
import random


class NN(object):

    def __init__(self, sizes):
        self.num_layers = len(sizes)
        self.bias = [np.random.randn(y, 1) for y in sizes[1:]]
        self.weights = [np.random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])]

    def feedforward(self, x):
        for b, w in zip(self.bias, self.weights):
            x = self.sigmoid(np.dot(w, x) + b)

        return x

    def SGD(self, training_data, batch_size, epoches, eta, test_data=None):
        if test_data: n_test = len(test_data)

        n = len(training_data)
        for j in range(epoches):
            random.shuffle(training_data)
            mini_batches = [training_data[k: k + batch_size] for k in range(0, n, batch_size)]
            for mini_batch_data in mini_batches:
                self.update_mini_batch(mini_batch_data, eta)

            if test_data:
                print "Epoch {0}: {1} / {2}".format(j, self.evaluate(test_data), n_test)
            else:
                print 'Epoch: {0}: Done'.format(j)

    def update_mini_batch(self, mini_batch, eta):
        nabla_b = [np.zeros(b.shape) for b in self.bias]
        nabla_w = [np.zeros(w.shape) for w in self.weights]

        for x, y in mini_batch:
            delta_nabla_b, delta_nabla_w = self.backprop(x, y)
            nabla_b = [nb + dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw + dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]

        self.bias = [b - eta * nb/len(mini_batch) for b, nb in zip(self.bias, nabla_b)]
        self.weights = [w - eta * nw/len(mini_batch) for w, nw in zip(self.weights, nabla_w)]

    def backprop(self, x, y):
        nabla_b = [np.zeros(b.shape) for b in self.bias]
        nabla_w = [np.zeros(w.shape) for w in self.weights]

        activation = x
        activations = [activation]
        zs = []
        for b, w in zip(self.bias, self.weights):
            z = np.dot(w, activation) + b
            zs.append(z)
            activation = self.sigmoid(z)
            activations.append(activation)

        delta = self.cost_derivative(activations[-1], y) * self.sigmoid_prime(zs[-1])

        for l in range(2, self.num_layers):
            z = zs[-l]
            sp = self.sigmoid_prime(z)
            delta = np.dot(self.weights[-l + 1].transpose(), delta) * sp
            nabla_b[-l] = delta
            nabla_w[-l] = np.dot(delta, activations[-l - 1].transpose())

        return nabla_b, nabla_w

    def evaluate(self, test_data):
        test_results = [(np.argmax(self.feedforward(x)), y) for x, y in test_data]
        return sum([int(x == y) for x, y in test_results])

    def cost_derivative(self, output_activations, y):
        return output_activations - y

    @classmethod
    def sigmoid(cls, x):
        return 1.0 / (1 + np.exp(-x))

    @classmethod
    def sigmoid_prime(cls, x):
        return cls.sigmoid(x) * (1 - cls.sigmoid(x))


if __name__ == '__main__':
    import mnist_loader
    # training_dt, _, test_dt = mnist_loader.load_data_wrapper()
    # print training_dt[0]
    #
    # nn = NN([784, 100, 10])
    # nn.SGD(training_dt, 10, 100, 0.1, test_dt)
    nn = NN([2, 3, 2])
    training_dt = np.array([[[[0], [0]], [[1], [0]]], [[[1], [1]], [[0], [1]]]])
    print training_dt[0]
    nn.SGD(training_dt, 1, 1, 0.5, None)