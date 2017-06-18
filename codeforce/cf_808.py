__author__ = 'sunary'


# http://codeforces.com/contest/808


def lucky_year(n):
    return int(n[0] + '9' * len(n[1:])) + 1 - int(n)


print lucky_year('201')