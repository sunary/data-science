__author__ = 'sunary'


import numpy as np
import tensorflow as tf
from tensorflow.contrib import learn
from tensorflow.contrib.learn.python.learn.estimators import model_fn as model_fn_lib


def cnn_model_fn(features, labels, mode):
    input_layer = tf.reshape(features, [-1, 28, 28, 1])

    conv1 = tf.layers.conv2d(
        inputs=input_layer,
        filters=20,
        kernel_size=[5, 5],
        padding='valid',
        activation=tf.nn.relu
    )

    print conv1.get_shape()
    pool1 = tf.layers.max_pooling2d(inputs=conv1, pool_size=[2, 2], strides=2)
    print pool1.get_shape()

    conv2 = tf.layers.conv2d(
        inputs=pool1,
        filters=40,
        kernel_size=[5, 5],
        padding='valid',
        activation=tf.nn.relu
    )
    print conv2.get_shape()
    pool2 = tf.layers.max_pooling2d(inputs=conv2, pool_size=[2, 2], strides=2)
    print pool2.get_shape()

    # Dense Layer
    pool2_flat = tf.reshape(pool2, [-1, 4 * 4 * 40])
    dense = tf.layers.dense(inputs=pool2_flat, units=1024, activation=tf.nn.relu)
    dropout = tf.layers.dropout(inputs=dense,
                                rate=0.5,
                                training=mode == learn.ModeKeys.TRAIN)
    # Logits Layer
    logits = tf.layers.dense(inputs=dropout, units=10)

    loss = None
    train_op = None

    if mode != learn.ModeKeys.INFER:
        onehot_labels = tf.one_hot(indices=tf.cast(labels, tf.int32), depth=10)
        loss = tf.losses.softmax_cross_entropy(onehot_labels=onehot_labels, logits=logits)

    if mode == learn.ModeKeys.TRAIN:
        train_op = tf.contrib.layers.optimize_loss(
            loss=loss,
            global_step=tf.contrib.framework.get_global_step(),
            learning_rate=0.005,
            optimizer='SGD'
        )

    # Generate Predictions
    predictions = {"classes": tf.argmax(input=logits, axis=1),
                   "probabilities": tf.nn.softmax(logits, name="softmax_tensor")}

    return model_fn_lib.ModelFnOps(mode=mode, predictions=predictions, loss=loss, train_op=train_op)


def train():
    mnist = learn.datasets.load_dataset('mnist')

    train_data = mnist.train.images
    train_labels = np.asarray(mnist.train.labels, dtype=np.int32)

    eval_data = mnist.test.images
    eval_labels = np.asarray(mnist.test.labels, dtype=np.int32)

    mnist_classifier = learn.Estimator(model_fn=cnn_model_fn, model_dir='/tmp/mnist_convnet_models')
    mnist_classifier.fit(
        x=train_data,
        y=train_labels,
        batch_size=50,
        steps=10000
    )

    metrics = {"accuracy": learn.MetricSpec(metric_fn=tf.metrics.accuracy,
                                            prediction_key="classes")}
    eval_results = mnist_classifier.evaluate(
        x=eval_data,
        y=eval_labels,
        metrics=metrics
    )
    print(eval_results)


if __name__ == '__main__':
    train()





