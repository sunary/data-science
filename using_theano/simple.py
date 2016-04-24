__author__ = 'sunary'


from theano import tensor as T
import theano
import numpy as np


def warmup():
    x = T.vector('x')
    W = theano.shared(np.array([1, 2]), 'W')

    y = (x * W).sum()

    f = theano.function([x], y)

    print f(np.ones(2))


def scan():
    def fn(c, a, b):
        return c + a + b
        # return c * a * b

    k = T.iscalar('k')
    A = T.ivector('A')
    B = T.ivector('B')

    result, updates = theano.scan(fn,
                                 outputs_info=T.ones_like(A),
                                 sequences=None,
                                 non_sequences=[A, B],
                                 n_steps=k)

    power = theano.function(inputs=[A, B, k], outputs=result, updates=updates)

    print power(range(10), range(10), 2)


def liner_regression():
    x = T.vector('x')
    target = T.scalar('target')

    W = theano.shared(np.array([0.2, 0.7]), 'W')
    y = (x * W).sum()

    cost = T.sqr(target - y)
    gradient = T.grad(cost, [W])
    update = [(W, W - 0.1 * gradient[0])]

    f = theano.function([x, target], y, updates=update)

    for _ in np.arange(10):
        f([1, 1], 20)
        print W.get_value()


if __name__ == '__main__':
    # warmup()
    # scan()
    liner_regression()