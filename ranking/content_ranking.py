__author__ = 'sunary'


from datetime import datetime, timedelta
import math


class ContentRanking():

    def __init__(self):
        self.epoch = datetime(1970, 1, 1)

    def epoch_seconds(self, date):
        datedelta = date - self.epoch
        return datedelta.days * 86400 + datedelta.seconds + (float(datedelta.microseconds) / 1000000)

    def score(self, ups, downs):
        return ups - downs

    def reddit_hot(self, ups, downs, date):
        s = self.score(ups, downs)
        order = math.log(max(abs(s), 1), 10)
        sign = 1 if s > 0 else -1 if s < 0 else 0
        seconds = self.epoch_seconds(date) - 1134028003
        return round(sign * order + seconds / 45000, 4)

    def reddit_confidence(self, ups, downs):
        n = ups + downs
        if n == 0:
            return 0

        z = 1.0 #1.0 = 85%, 1.6 = 95%
        phat = float(ups) / n
        return math.sqrt(phat + z * z /(2 * n) - z *((phat *(1 - phat) + z * z / (4 * n)) / n)) /(1 + z * z / n)

    def hacknews_score(self, age_days, readers, gravity=1.9):
        return (readers - 1) / pow((age_days + 2), gravity)


if __name__ == '__main__':
    ranking = ContentRanking()
    print ranking.hot(3800, 247, datetime(2015, 8, 8))
    print ranking.confidence(3800, 247)