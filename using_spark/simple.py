__author__ = 'sunary'


import pyspark


def count_word():
    sc = pyspark.SparkContext()

    text_file = sc.textFile("hdfs://...")

    text_file.flatMap(lambda line: line.split(" ")) \
            .map(lambda word: (word, 1)) \
            .reduceByKey(lambda a, b: a + b) \
            .collect()


def parallel():
    sc = pyspark.SparkContext()

    data = [(1, 'a'), (1, 'b'), (2, 'c'), (2, 'd'), (2, 'e'), (3, 'f')]
    sc.parallelize(data) \
        .saveAsTextFile("res.csv")