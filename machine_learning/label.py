__author__ = 'sunary'


import pandas as pd
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn import metrics
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression


def logistic_regression():
    df = pd.read_csv('../resources/data0.txt', header=None)
    x, x_test, y, y_test = train_test_split(df[df.columns[:-1]], df[df.columns[-1]])

    lg = LogisticRegression()
    lg.fit(x, y)

    value0 = df.loc[df[df.columns[-1]] == 0]
    value1 = df.loc[df[df.columns[-1]] == 1]
    plt.scatter(value0[value0.columns[0]], value0[value0.columns[1]], marker='+', c='red')
    plt.scatter(value1[value1.columns[0]], value1[value1.columns[1]], marker='o', c='green')
    plt.xlabel('Score 1')
    plt.ylabel('Score 2')
    plt.legend(['Admitted', 'Not admitted'], loc='upper right')
    plt.show()

    y_predict = lg.predict(x_test)
    print metrics.accuracy_score(y_test, y_predict)


def lg2():
    data = np.loadtxt('../resources/data1.txt', delimiter=',')
    x, x_test, y, y_test = train_test_split(data[:, :-1], data[:, -1])
    lg = LogisticRegression()
    lg.fit(x, y)

    y_predict = lg.predict(x_test)
    print metrics.accuracy_score(y_test, y_predict)


if __name__ == '__main__':
    lg2()