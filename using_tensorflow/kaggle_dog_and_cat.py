__author__ = 'sunary'


import tensorflow as tf
import numpy as np
from tensorflow.contrib import learn
from tensorflow.contrib.learn.python.learn.estimators import model_fn as model_fn_lib


WIDTH = 64
HEIGHT = 64
resize_fn = lambda image: tf.image.resize_image_with_crop_or_pad(image, HEIGHT, WIDTH)


def cnn_model_fn(features, labels, mode):
    input_layer = tf.reshape(features, [-1, WIDTH, HEIGHT, 3])

    conv1 = tf.layers.conv2d(
        inputs=input_layer,
        filters=64,
        kernel_size=[5, 5],
        padding='valid',
        activation=tf.nn.relu
    )

    pool1 = tf.layers.max_pooling2d(inputs=conv1, pool_size=[2, 2], strides=2)

    conv2 = tf.layers.conv2d(
        inputs=pool1,
        filters=128,
        kernel_size=[5, 5],
        padding='valid',
        activation=tf.nn.relu
    )

    pool2 = tf.layers.max_pooling2d(inputs=conv2, pool_size=[2, 2], strides=2)

    # Dense Layer
    pool2_flat = tf.reshape(pool2, [-1, 13 * 13 * 128])
    dense = tf.layers.dense(inputs=pool2_flat, units=1024, activation=tf.nn.relu)
    dropout = tf.layers.dropout(inputs=dense,
                                rate=0.5,
                                training=mode == learn.ModeKeys.TRAIN)
    # Logits Layer
    logits = tf.layers.dense(inputs=dropout, units=2)

    loss = None
    train_op = None

    if mode != learn.ModeKeys.INFER:
        onehot_labels = tf.one_hot(indices=tf.cast(labels, tf.int32), depth=2)
        loss = tf.losses.softmax_cross_entropy(onehot_labels=onehot_labels, logits=logits)

    if mode == learn.ModeKeys.TRAIN:
        train_op = tf.contrib.layers.optimize_loss(
            loss=loss,
            global_step=tf.contrib.framework.get_global_step(),
            learning_rate=0.01,
            optimizer='SGD'
        )

    # Generate Predictions
    predictions = {"classes": tf.argmax(input=logits, axis=1),
                   "probabilities": tf.nn.softmax(logits, name="softmax_tensor")}

    return model_fn_lib.ModelFnOps(mode=mode, predictions=predictions, loss=loss, train_op=train_op)


def load_dataset(path_files):
    '''
    image format: cat|dog.index.jpg
    index 0-11499: train
    index 11500-12499: test
    [64, 64, 3]
    '''

    train_size = 11500
    eval_size = 1000
    if False:
        # 0 0 0 0 0 .... 1 1 1 1 1 ....
        train_data = decode_image(['{}/{}.{}.jpg'.format(path_files, name, x) for name in ['cat', 'dog'] for x in xrange(train_size)],
                                  resize_func=resize_fn)
        train_data = np.divide(train_data, 255.0, dtype=np.float32)
        train_labels = np.concatenate((np.zeros(train_size), np.ones(train_size)))

        eval_data = decode_image(['{}/{}.{}.jpg'.format(path_files, name, x) for name in ['cat', 'dog'] for x in xrange(train_size, train_size + eval_size)],
                                 resize_func=resize_fn)
        eval_data = np.divide(eval_data, 255.0, dtype=np.float32)
        eval_labels = np.concatenate((np.zeros(eval_size), np.ones(eval_size)))
    else:
        # 0 1 0 1 0 1 0 1 0 1 0 1 ....
        train_data = decode_image(['{}/{}.{}.jpg'.format(path_files, name, x) for x in xrange(train_size) for name in ['cat', 'dog']],
                                  resize_func=resize_fn)
        train_data = np.divide(train_data, 255.0, dtype=np.float32)
        train_labels = np.reshape(np.tile(np.array([0, 1]), train_size), -1)

        eval_data = decode_image(['{}/{}.{}.jpg'.format(path_files, name, x) for x in xrange(train_size, train_size + eval_size) for name in ['cat', 'dog']],
                                 resize_func=resize_fn)
        eval_data = np.divide(eval_data, 255.0, dtype=np.float32)
        eval_labels = np.reshape(np.tile(np.array([0, 1]), eval_size), -1)

    return train_data, train_labels, eval_data, eval_labels


def decode_image(image_file_names, resize_func=None):
    images = []

    graph = tf.Graph()
    with graph.as_default():
        file_name = tf.placeholder(dtype=tf.string)
        file = tf.read_file(file_name)
        image = tf.image.decode_jpeg(file)
        if resize_func is not None:
            image = resize_func(image)

    with tf.Session(graph=graph) as session:
        tf.global_variables_initializer()
        for i in range(len(image_file_names)):
            images.append(session.run(image, feed_dict={file_name: image_file_names[i]}))
            if (i + 1) % 1000 == 0:
                print('Images processed: {}'.format(i + 1))

        session.close()

    return images


def train():
    train_data, train_labels, eval_data, eval_labels = load_dataset('/Users/sunary/Downloads/train')

    tensors_to_log = {"probabilities": "softmax_tensor"}
    logging_hook = tf.train.LoggingTensorHook(tensors=tensors_to_log, every_n_iter=50)

    dogvscat_classifier = learn.SKCompat(learn.Estimator(model_fn=cnn_model_fn, model_dir='/tmp/dogvscat_convnet_model'))
    dogvscat_classifier.fit(
        x=train_data,
        y=train_labels,
        batch_size=50,
        steps=1000,
        monitors=[logging_hook]
    )

    metrics = {"accuracy": learn.MetricSpec(metric_fn=tf.metrics.accuracy,
                                            prediction_key="classes")}
    eval_results = dogvscat_classifier.score(
        x=eval_data,
        y=eval_labels,
        metrics=metrics
    )
    print(eval_results)


def inference():
    pass


if __name__ == '__main__':
    train()
    # inference()

