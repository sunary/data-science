__author__ = 'sunary'


import numpy as np
from numpy.linalg import inv
import matplotlib.pyplot as plt


def ln():
    # y = 0.5 * x1 + 2 + epsilon
    np.random.seed(0)

    x0 = 2.
    x1 = np.random.uniform(0, 12, 50)
    real_y = 0.5*x1 + x0

    plt.plot(x1, real_y, 'ro')
    plt.plot([0, 12], [2, 8], 'k-', lw=2)

    noisy_y = 0.5*x1 + x0 + np.random.normal(0, 1, 50)
    plt.plot(x1, noisy_y, 'bx')

    X = np.column_stack((np.ones_like(x1), x1))

    # Calculate beta coefficients by normal equation
    t_X = np.transpose(X)       # X'
    cov_X = np.matmul(t_X, X)   # X'*X
    pseudo_inv_X = np.matmul(inv(cov_X), t_X) # (X'*X)^-1*X'
    beta = np.matmul(pseudo_inv_X, noisy_y)

    # Calculate y_hat
    y_hat = np.matmul(X, beta)
    plt.plot(x1, y_hat, 'ms')
    print("Regression coefficients:", beta)
    plt.axis([0, 12, 0, 12])
    plt.show()