__author__ = 'sunary'


import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np


data = []

X = tf.placeholder(tf.float32, name='X')
Y = tf.placeholder(tf.float32, name='Y')

w = tf.Variable(0.0, name='Weight')
b = tf.Variable(0.0, name='bias')

Y_predict = w * X + b

loss = tf.square(Y - Y_predict, name='loss')
optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01).minimize(loss)

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

    for _ in range(100):
        for x, y in data:
            sess.run([optimizer, loss], feed_dict={X: x, Y:y})

    w_value, b_value = sess.run([w, b])


X, Y = data.T[0], data.T[1]
plt.plot(X, Y, 'bo', label='Real data')
plt.plot(X, X * w_value + b_value, 'r', label='Predicted data')
plt.legend()
plt.show()