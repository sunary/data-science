__author__ = 'sunary'


def treasure(x1, y1, x2, y2, step_x, step_y):
    return 'YES' if not (x1 - x2) % step_x and not (y1 - y2) % step_y and ((x1 - x2)/step_x) % 2 == ((y1 - y2)/step_y) % 2 else 'NO'


def really_big(k, s):
    return k - sum([int(x) for x in str(k)]) >= s


def find_big(n, k):
    if not really_big(n, k):
        return 0

    left = 0
    right = n
    while True:
        m = left + (right - left) / 2
        if really_big(m, k):
            if not really_big(m - 1, k):
                break
            right = m - 1

        else:
            left = m + 1

    return n - m + 1

ip = raw_input().split(' ')
print find_big(int(ip[0]), int(ip[1]))
