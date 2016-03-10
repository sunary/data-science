__author__ = 'sunary'


import numpy as np
import matplotlib.pyplot as plt


def warmup():
    x = np.arange(0, 3 * np.pi, 0.1)
    y_sin = np.sin(x)
    y_cos = np.cos(x)

    plt.plot(x, y_sin)
    plt.plot(x, y_cos)

    plt.xlabel('x axis label')
    plt.ylabel('y axis label')

    plt.title('Sine and Cosine')
    plt.legend(['Sine', 'Cosine'])

    plt.show()


def subplot():
    x = np.arange(0, 3 * np.pi, 0.1)
    y_sin = np.sin(x)
    y_cos = np.cos(x)

    plt.subplot(2, 1, 1)
    plt.plot(x, y_sin)
    plt.title('Sine')

    plt.subplot(2, 1, 2)
    plt.plot(x, y_cos)
    plt.title('Cosine')

    plt.show()


if __name__ == '__main__':
    warmup()
    subplot()