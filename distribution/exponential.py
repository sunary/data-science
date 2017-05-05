__author__ = 'sunary'


import matplotlib.pyplot as plt
import numpy as np


def cdf(x, _lambda):
    return 1 - np.exp(-_lambda*x)


def plot():
    x = []
    y = []
    for _ in range(1000):
        x.append(np.random.randn())
        y.append(cdf(x[-1], 0.5))

    plt.scatter(x, y)

    plt.title('Exponential Distribution')
    plt.show()


if __name__ == '__main__':
    plot()

