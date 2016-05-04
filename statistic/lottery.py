__author__ = 'sunary'


import requests
import re
from datetime import datetime, timedelta
from collections import Counter
from redis.client import StrictRedis
from ranking import scale


redis = StrictRedis()
expire = 41 * 84600


def crawl_lottery(date, full=False):
    key = 'mienbac-{0}'.format(date.strftime('%d/%m/%Y'))
    redis_ketqua = redis.get(key)

    if redis_ketqua and not full:
        return redis_ketqua

    res = requests.get('http://www.minhngoc.com.vn/getkqxs/mien-bac/{0}.js'.format(date.strftime('%d-%m-%Y'))).text

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


def last_n_days(days=40):
    start_date = datetime.utcnow()

    if requests.get('http://www.minhngoc.com.vn/getkqxs/mien-bac/{0}.js'.format(start_date.strftime('%d-%m-%Y')),
                    allow_redirects=False).status_code == 302:
        start_date -= timedelta(days=1)

    today = start_date
    crawl_dates = []
    for i in range(days):
        crawl_dates.append(start_date)
        start_date -= timedelta(days=1)

    return crawl_dates, today


def soi(days=40):
    crawl_dates, today = last_n_days(days)
    today = today.strftime('%d-%m-%Y')

    ketqua = []
    bin_result_today = ''
    result_today = []
    for i, d in enumerate(crawl_dates):
        if i == 0:
            result_today = crawl_lottery(d, True)
            bin_result_today = result_today[0]
            result_today = result_today[1]

            ketqua.append(bin_result_today)
        else:
            ketqua.append(crawl_lottery(d))

    lokhan, most_appears, prefix, suffix = statistic(ketqua, days)

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

    return today, result_today, group_head, group_tail, lokhan, most_appears, prefix, suffix


def statistic(ketqua_n_days, days):
    distance_days = []
    for i in range(100):
        i = str(i) if i > 9 else '0' + str(i)
        distance_days.append([i, []])

    for lo in distance_days:
        lo[1] += [0]
        i = 0
        for kq in ketqua_n_days:
            if lo[0] in kq:
                lo[1] += [0]
                i += 1
            lo[1][i] += 1

    lokhan = [[lo[0], lo[1][0]] for lo in distance_days]
    coefficient = [get_coefficient(lo[1], days) for lo in distance_days]
    coefficient = scale.standard_competition_ranking(coefficient)

    lokhan = sorted(lokhan, key=lambda item:-item[1])[:10]

    most_appears = []
    ketqua_n_days = ','.join(ketqua_n_days)
    ketqua_n_days = ketqua_n_days.replace('|', ',')
    ketqua_n_days = ketqua_n_days.split(',')
    frequency = Counter(ketqua_n_days)

    for i in range(100):
        i = str(i) if i > 9 else '0' + str(i)
        if not frequency.get(i):
            frequency[i] = 0

    for k, v in frequency.iteritems():
        most_appears.append((k, v))

    most_appears = sorted(most_appears, key=lambda item:item[0])

    for i in range(len(most_appears)):
        most_appears[i] = list(most_appears[i])
        most_appears[i].append(coefficient[i])

    prefix = [0] * 10
    suffix = [0] * 10

    for k in ketqua_n_days:
        prefix[int(k[0])] += 1
        suffix[int(k[1])] += 1

    return lokhan, most_appears, prefix, suffix


def get_coefficient(distances, days):
    sum_distance = sum(distances)*1.0/len(distances)
    coefficient = 0
    for dis in distances:
        coefficient += (sum_distance - dis) **2

    return coefficient/days


if __name__ == '__main__':
    soi(3)