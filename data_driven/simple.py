__author__ = 'sunary'


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


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


def with_pandas():
    df = pd.DataFrame(np.random.randn(10, 4), index=pd.date_range('1/1/2010', periods=10), columns=list('ABCD'))
    # ts = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2010', periods=1000))
    df = df.cumsum()
    # df.plot()
    df.plot.bar()
    # df.plot.barh()
    # df.plot.hist(alpha=0.7)
    # df.plot.box()
    # df.plot.kde()
    # df.plot.area()
    # df.plot.scatter(x='A', y='B')
    # df.plot.hexbin(x='A', y='B', gridsize=30)
    # df.plot.pie(figsize=(6, 6))
    plt.show()


def heatmap():
    uniform_data = np.random.rand(10, 12)
    ax = sns.heatmap(uniform_data)


if __name__ == '__main__':
    # warmup()
    # subplot()
    with_pandas()