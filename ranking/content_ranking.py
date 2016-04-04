__author__ = 'sunary'


from datetime import datetime
import math
import matplotlib.pyplot as plt


epoch = datetime(1970, 1, 1)

def epoch_seconds(date):
    datedelta = date - epoch
    return datedelta.days * 86400 + datedelta.seconds + (float(datedelta.microseconds) / 1000000)


def score(ups, downs):
    return ups - downs


def reddit_hot(ups, downs, date):
    s = score(ups, downs)
    order = math.log(max(abs(s), 1), 10)
    sign = 1 if s > 0 else -1 if s < 0 else 0
    seconds = epoch_seconds(date) - 1134028003
    return round(sign * order + seconds / 45000, 4)


def reddit_confidence(ups, downs):
    n = ups + downs
    if n == 0:
        return 0

    z = 1.0 # 1.0 = 85%, 1.6 = 95%
    phat = float(ups) / n
    return math.sqrt(phat + z * z /(2 * n) - z *((phat *(1 - phat) + z * z / (4 * n)) / n)) /(1 + z * z / n)


def hacknews_score(age_days, readers, gravity=1.9):
    return (readers - 1) / pow((age_days + 2), gravity)


def test_reddit_confidence():
    votes = [[5, 0], [10, 1], [50, 60], [100, 15], [500, 80], [1000, 300], [1000, 800], [5000, 2000], [5000, 4000]]
    idx = []
    score = []
    for i, v in enumerate(votes):
        idx.append(i)
        score.append(reddit_confidence(*v))

    plt.bar(idx, score)
    plt.show()


def test_hacknews_score():
    stats = [[100, 1000], [20, 500], [10, 300], [5, 200], [5, 100], [1, 30], [1, 50]]
    idx = []
    score = []
    for i, s in enumerate(stats):
        idx.append(i)
        score.append(hacknews_score(*s))

    plt.bar(idx, score)
    plt.show()


if __name__ == '__main__':
    print reddit_hot(3800, 247, datetime(2015, 8, 8))
    # test_reddit_confidence()
    test_hacknews_score()