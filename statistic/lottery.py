__author__ = 'sunary'


import requests
import re
from datetime import datetime, timedelta
from collections import Counter
from redis.client import StrictRedis


redis = StrictRedis()
expire = 41 * 84600
time_out = 19


def crawl_lottery(date, full=False):
    date = [(str(d) if d > 9 else '0' + str(d)) for d in date]

    key = 'mienbac-{0}/{1}/{2}'.format(date[0], date[1], date[2])
    redis_ketqua = redis.get(key)

    if redis_ketqua and not full:
        return redis_ketqua

    res = requests.get('http://www.minhngoc.com.vn/getkqxs/mien-bac/{0}-{1}-{2}.js'.format(date[0], date[1], date[2])).text

    giai = ['giaidb', 'giai1', 'giai2', 'giai3', 'giai4', 'giai5', 'giai6', 'giai7']
    ketqua = ''
    result_today = []
    for g in giai:
        match = re.search('<td\sclass="{0}">([^<]+)</td>'.format(g), res)
        if match:
            row = match.group(1).strip().replace(' ', '').split('-')
            row = [str(r) for r in row]
            if full:
                result_today.append(' - '.join(row))

            row = [r[-2:] for r in row]
            ketqua += ','.join(row) + ','

    ketqua = ketqua.strip(',')
    if not redis_ketqua:
        redis.set(key, ketqua)
        redis.expire(key, expire)
    if full:
        return ketqua, result_today

    return ketqua


def last_n_days(days=40, timezone=7):
    start_date = datetime.utcnow()

    if start_date.hour + timezone < time_out:
        start_date -= timedelta(days=1)

    crawl_date = []
    for i in range(days):
        crawl_date.append([start_date.day, start_date.month, start_date.year])
        start_date -= timedelta(days=1)

    return crawl_date


def str_today(timezone=7):
    today = datetime.utcnow()

    if today.hour + timezone < time_out:
        today -= timedelta(days=1)

    return '{0}-{1}-{2}'.format(today.day, today.month, today.year)


def soi(days=40):
    dates = last_n_days(days)
    ketqua = []
    bin_result_today = ''
    result_today = []
    for i, d in enumerate(dates):
        if i == 0:
            result_today = crawl_lottery(d, True)
            bin_result_today = result_today[0]
            result_today = result_today[1]

            ketqua.append(bin_result_today)
        else:
            ketqua.append(crawl_lottery(d))

    lokhan, most_appears, prefix, suffix = statistic(ketqua)

    bin_result_today = bin_result_today.split(',')[:-1]
    group_head = [[] for _ in range(10)]
    group_tail = [[] for _ in range(10)]

    for bin in bin_result_today:
        group_head[int(bin[0])].append(bin[1])
        group_tail[int(bin[1])].append(bin[0])

    for i in range(10):
        group_head[i] = sorted(group_head[i])
        group_head[i] = ', '.join(group_head[i])

        group_tail[i] = sorted(group_tail[i])
        group_tail[i] = ', '.join(group_tail[i])

    return result_today, group_head, group_tail, lokhan, most_appears, prefix, suffix


def statistic(ketqua_n_days):
    lokhan = []
    for i in range(100):
        i = str(i) if i > 9 else '0' + str(i)
        lokhan.append([i, 0])

    for lo in lokhan:
        for kq in ketqua_n_days:
            if lo[0] in kq:
                break
            lo[1] += 1

    lokhan = sorted(lokhan, key=lambda item:-item[1])[:10]

    most_appears = []
    ketqua_n_days = ','.join(ketqua_n_days).split(',')
    frequency = Counter(ketqua_n_days)

    for i in range(100):
        i = str(i) if i > 9 else '0' + str(i)
        if not frequency.get(i):
            frequency[i] = 0

    for k, v in frequency.iteritems():
        most_appears.append((k, v))

    most_appears = sorted(most_appears, key=lambda item:item[0])

    prefix = [0] * 10
    suffix = [0] * 10

    for k in ketqua_n_days:
        prefix[int(k[0])] += 1
        suffix[int(k[1])] += 1

    return lokhan, most_appears, prefix, suffix


if __name__ == '__main__':
    print soi(3)