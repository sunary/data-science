__author__ = 'sunary'


import numpy as np


'''
https://github.com/agyorev/Eigenfaces/blob/master/eigenfaces.py
'''

def img_to_vector():
    pass


def train(L, _energy=0.85):
    global mean_img_col, evectors, W

    mn, l = L.shape

    mean_img_col = np.sum(L, axis=1) / l

    for i in xrange(l):
        L[:, i] -= mean_img_col

    C = np.matrix(L.transpose()) * L
    C /= l

    evalues, evectors = np.linalg.eig(C)
    sort_indices = np.argsort()[::-1]
    evalues = evalues[sort_indices]
    evectors = evectors[sort_indices]

    evalues_sum = np.sum(evalues)

    evalues_count = 0
    evalues_enegy = 0.0
    while True:
        evalues_enegy += evalues[evalues_count] / evalues_sum
        evalues_count += 1

        if evalues_enegy >= _energy:
            break

    evalues = evalues[:evalues_count]
    evectors = evectors[:evalues_count]

    evectors = evectors.transpose()
    evectors = L * evectors

    norms = np.linalg.norm(evectors, axis=0)
    evectors /= norms

    W = evectors.transpose() * L


def classify(img_vector):
    img_vector -= mean_img_col

    one, mn = img_vector.shape
    img_vector = np.reshape(img_vector, (mn, one))

    S = evectors.transpose() * img_vector
    diff = W - S
    norms = np.linalg.norm(diff, axis=0)

    return np.argmin(norms)


def main():
    pass


if __name__ == '__main__':
    main()