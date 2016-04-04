__author__ = 'sunary'


import numpy as np
import pandas as pd
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
    x = np.random.randn(2000)
    y = np.random.randn(2000)
    heatmap, xedges, yedges = np.histogram2d(x, y, bins=(50, 50))
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

    plt.clf()
    plt.imshow(heatmap, extent=extent)
    plt.show()


def draw_object():
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    rect = plt.Rectangle((5, 4), 1, 4, color='k', alpha=0.3)
    circ = plt.Circle((4, 4), 1.0, color='b', alpha=0.3)
    pgon = plt.Polygon([[1, 1], [1.5, 2], [0, 3]], color='g', alpha=0.3)

    ax.plot(range(10), 'o', color='black')
    ax.add_patch(rect)
    ax.add_patch(circ)
    ax.add_patch(pgon)

    plt.show(ax)


if __name__ == '__main__':
    # warmup()
    # subplot()
    # with_pandas()
    heatmap()
    # draw_object()