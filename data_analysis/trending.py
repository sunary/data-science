__author__ = 'sunary'


from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.gaussian_process import GaussianProcess
import numpy as np
import matplotlib.pyplot as plt


def linear_regression():
    x = np.arange(0, 10, 1)
    y = x * np.sin(x)

    matrix_x = np.asmatrix(x).T
    matrix_y = np.asmatrix(y).T

    lg = LinearRegression()
    lg.fit(matrix_x, matrix_y)

    pred_x = np.arange(0, 10, 0.2)
    pred_x = np.asmatrix(pred_x).T
    pred_y = lg.predict(pred_x)

    plt.scatter(x, y, label='observed')
    plt.plot(pred_x, pred_y, label='estimate')
    plt.show()


def logistic_regression():
    lg = LogisticRegression()


def gaussian():
    x = np.arange(0, 10, 1)
    y = x * np.sin(x)

    matrix_x = np.asmatrix(x).T
    matrix_y = np.asmatrix(y).T

    gp = GaussianProcess(theta0=1e-2, thetaL=1e-4, thetaU=1e-1, nugget=1e-5)
    gp.fit(matrix_x, matrix_y)

    pred_x = np.arange(0, 10, 0.2)
    pred_x = np.asmatrix(pred_x).T
    pred_y, mean_square_error = gp.predict(pred_x, eval_MSE=True)
    sigma = np.sqrt(mean_square_error)
    error = 3 * sigma
    lower = pred_y - np.asmatrix(error).T
    upper = pred_y + np.asmatrix(error).T

    plt.scatter(x, y, label='observed')
    plt.plot(pred_x, pred_y, label='estimate')
    plt.plot(pred_x, lower,'--r', label='lower threshold')
    plt.show()


if __name__ == '__main__':
    gaussian()
