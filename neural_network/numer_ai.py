__author__ = 'sunary'


from neural_network.model_nn import NeuralNetwork
import pandas as pd
import datetime


model = NeuralNetwork([50, 20, 10, 2])
model.load('numer_ai.dat')


def train(file='/Users/sunary/Downloads/numerai_datasets/numerai_training_data.csv'):
    df = pd.read_csv(file)

    for _round in range(100):
        print 'Round {}: {}'.format(_round, datetime.datetime.now())
        for index, row in df.iterrows():
            model.train(row[:50].tolist(), int(row['target']))

        model.save('numer_ai.dat')


def test(file='/Users/sunary/Downloads/numerai_datasets/numerai_training_data.csv'):
    df = pd.read_csv(file)

    accuracy = 0
    for index, row in df.iterrows():
        predict_id = model.train(row[:50].tolist())
        if predict_id == int(row['target']):
            accuracy += 1

    print 'Rate: {}'.format(accuracy * 100.0 / len(df))


def predict(file='/Users/sunary/Downloads/numerai_datasets/numerai_tournament_data.csv'):
    df = pd.read_csv(file)
    result = []
    for index, row in df.iterrows():
        probability = model.train(row[:50].tolist())
        result.append([index, probability])
        break

    df_predict = pd.DataFrame(result, columns=['t_id', 'probability'])
    df_predict.to_csv('/Users/sunary/Downloads/numerai_datasets/numerai_result_data.csv')


if __name__ == '__main__':
    # train()
    test()
    # predict()