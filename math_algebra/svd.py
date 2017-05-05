__author__ = 'sunary'


import numpy as np


def cal_svd(A):
    '''
    U D V^T
    '''
    evalues, evectors = np.linalg.eig(np.dot(A.transpose(), A))

    sort_indices = np.argsort(evalues)[::-1]

    evalues = evalues[sort_indices]
    evectors = evectors[sort_indices]

    V = evectors # V is eigenvectors
    D = np.zeros((len(evalues), len(evalues))) # D is orthogonal matrix of root-square eigenvalues
    for i in range(len(evalues)):
        D[i][i] = np.sqrt(evalues[i])

    U = np.dot(np.dot(A, V), np.linalg.inv(D)) # U = A.V.D^-1

    return np.dot(np.dot(U, D), V.transpose())


if __name__ == '__main__':
    print cal_svd(np.array([[4, 0], [3, -5]]))
    print cal_svd(np.array([[2, 4], [1, 3], [0, 0], [0, 0]]))