__author__ = 'sunary'


def check_rc(r, c, v):
    for x in r:
        for y in c:
            if x + y == v:
                return True
    return False


def check_square(s):
    for i in range(len(s)):
        for j in range(len(s[0])):
            if s[i][j] == 1:
                continue
            srow = set(s[i])
            scol = set([s[x][j] for x in range(len(s))])

            if check_rc(srow, scol, s[i][j]):
                continue

            return 'No'

    return 'Yes'


def banana(m, b):
    a = b*m
    x0 = (a + b)/2

    max = 0
    for i in range(21):
        x = x0 + 10 - i
        y = - x/m + b
        if x >= 0 and y >= 0 and x*y*(x + y) > max:
            max = x*y*(x + y)

    y0 = (a + b)/2
    for i in range(21):
        y = y0 + 10 - i
        x = (b - y) * m
        if x >= 0 and y >= 0 and x * y * (x + y) > max:
            max = x * y * (x + y)

    return max


s = raw_input().split(' ')
print banana(int(s[0]), int(s[1]))