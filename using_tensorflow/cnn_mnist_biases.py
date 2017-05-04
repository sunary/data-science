__author__ = 'sunary'


import numpy as np
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data


key_w = ['wc1', 'wc2', 'wd1', 'out']
key_b = ['bc1', 'bc2', 'bd1', 'out']


def conv2d(x, W, b, strides=1):
    x = tf.nn.conv2d(x, W, strides=[1, strides, strides, 1], padding='SAME')
    x = tf.nn.bias_add(x, b)
    return tf.nn.relu(x)


def maxpool2d(x, k=2):
    return tf.nn.max_pool(x, ksize=[1, k, k, 1], strides=[1, k, k, 1], padding='SAME')


def conv_net(x, weights, biases, dropout):
    x = tf.reshape(x, shape=[-1, 28, 28, 1])

    # Convolution Layer
    conv1 = conv2d(x, weights['wc1'], biases['bc1'])
    # Max Pooling (down-sampling)
    conv1 = maxpool2d(conv1, k=2)

    # Convolution Layer
    conv2 = conv2d(conv1, weights['wc2'], biases['bc2'])
    # Max Pooling (down-sampling)
    conv2 = maxpool2d(conv2, k=2)

    # Fully connected layer
    # Reshape conv2 output to fit fully connected layer input
    fc1 = tf.reshape(conv2, [-1, weights['wd1'].get_shape().as_list()[0]])
    fc1 = tf.add(tf.matmul(fc1, weights['wd1']), biases['bd1'])
    fc1 = tf.nn.relu(fc1)
    # Apply Dropout
    fc1 = tf.nn.dropout(fc1, 0.5)

    # Output, class prediction
    out = tf.add(tf.matmul(fc1, weights['out']), biases['out'])
    return out


def train():
    mnist = input_data.read_data_sets("MNIST-data/", one_hot=True)

    train_data = mnist.train.images
    train_labels = np.asarray(mnist.train.labels, dtype=np.int32)

    eval_data = mnist.test.images
    eval_labels = np.asarray(mnist.test.labels, dtype=np.int32)

    # tf Graph input
    x = tf.placeholder(tf.float32, [None, 28 * 28])
    y = tf.placeholder(tf.float32, [None, 10])
    keep_prob = tf.placeholder(tf.float32) # dropout (keep probability)

    weights = {
        # 5x5 conv, 1 input, 32 outputs
        key_w[0]: tf.Variable(tf.random_normal([5, 5, 1, 32], stddev=0.01)),
        # 5x5 conv, 32 inputs, 64 outputs
        key_w[1]: tf.Variable(tf.random_normal([5, 5, 32, 64], stddev=0.01)),
        # fully connected, 7*7*64 inputs, 1024 outputs
        key_w[2]: tf.Variable(tf.random_normal([7 * 7 * 64, 1024], stddev=0.01)),
        # 1024 inputs, 10 outputs (class prediction)
        key_w[3]: tf.Variable(tf.random_normal([1024, 10], stddev=0.01))
    }
    biases = {
        key_b[0]: tf.Variable(tf.random_normal([32], stddev=0.01)),
        key_b[1]: tf.Variable(tf.random_normal([64], stddev=0.01)),
        key_b[2]: tf.Variable(tf.random_normal([1024], stddev=0.01)),
        key_b[3]: tf.Variable(tf.random_normal([10], stddev=0.01))
    }

    saver = tf.train.Saver()
    [tf.add_to_collection('vars', weights[k]) for k in key_w]
    [tf.add_to_collection('vars', biases[k]) for k in key_b]

    pred = conv_net(x, weights, biases, keep_prob)

    # Define loss and optimizer
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred, labels=y))
    # optimizer = tf.train.AdamOptimizer(learning_rate=0.01).minimize(cost)
    optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01).minimize(cost)

    # Evaluate model
    correct_pred = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())

        batch_size = 50
        epoches = 1000

        for i in xrange(epoches):
            batch_x, batch_y = mnist.train.next_batch(batch_size)
            # Run optimization op (backprop)
            sess.run(optimizer, feed_dict={x: batch_x, y: batch_y, keep_prob: 0.5})

            if (i + 1) % 100 == 0:
                loss, acc = sess.run([cost, accuracy], feed_dict={x: batch_x, y: batch_y, keep_prob: 1.})
                print('Epoch {}: loss: {}, acc: {}'.format(i + 1, loss, acc))

        print sess.run([cost, accuracy], feed_dict={x: eval_data, y: eval_labels, keep_prob: 1.})
        saver.save(sess, 'data/cnn_mnist/model')


def load_model():
    with tf.Session() as sess:
        new_saver = tf.train.import_meta_graph('data/cnn_mnist/model.meta')
        new_saver.restore(sess, tf.train.latest_checkpoint('data/cnn_mnist/'))
        all_vars = tf.get_collection('vars')

        weights = {}
        for i, k in enumerate(key_w):
            weights[k] = all_vars[i]

        biases = {}
        for i, k in enumerate(key_b):
            biases[k] = all_vars[i + len(key_w)]


if __name__ == '__main__':
    train()
    # load_model()
