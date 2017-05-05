__author__ = 'sunary'


import numpy as np
import matplotlib.pyplot as plt


def cal_pca():
    # PCA-2D
    # plt.figure(figsize=(10, 10))
    fig = plt.figure()
    pca_data = np.loadtxt('data/pcaData.txt', dtype=np.float32)

    X = np.transpose(pca_data)
    # plt.plot(x[:, 0], x[:, 1], 'ro')

    avg = np.mean(X, axis=0)
    X = X - np.tile(avg, [X.shape[0], 1]) # x = x - mean(x)

    # Plot X with zero mean
    plt.plot(X[:, 0], X[:, 1], 'ro')

    # Compute covariance matrix
    sigma = np.matmul(np.transpose(X), X) / (X.shape[1] - 1)

    # svd sigma
    u, d, v = np.linalg.svd(sigma) # here u = v because sigma is symmetric
    print u
    plt.plot([0, u[0, 0]], [0, u[1, 0]], 'k-', lw=1)
    plt.plot([0, u[0, 1]], [0, u[1, 1]], 'k-', lw=1)

    plt.axis([-1, 1, -1, 1])
    plt.axes().set_aspect('equal', 'datalim')

    # project data on fisrt eigen basis
    X_pc1 = np.matmul(X, u[:, 0])
    X_pc2 = np.matmul(X, u[:, 1])

    # engineface
    print [np.matmul(X[0], u[:, 0]), np.matmul(X[0], u[:, 1])]
    # plot X_pc1
    fig = plt.figure()
    plt.plot(X_pc1, np.ones_like(X_pc1), 'rx')
    plt.title('First Principal Component')

    # plot X_pc2
    fig = plt.figure()
    plt.plot(X_pc2, np.ones_like(X_pc2), 'mx')
    plt.title('Second Principal Component')
    plt.show()


if __name__ == '__main__':
    cal_pca()