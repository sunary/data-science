__author__ = 'sunary'


def restaurant(a, b, n):
    r = sum(n) - a - 2*b
    return 0 if r < 0 else r


def black_square(s):
    for i in range(len(s)):
        for j in range(len(s[0])):
            if s[i][j] == 'B':
                s[i][j] = 1
            else:
                s[i][j] = 0

    left = 100
    right = -1
    top = 100
    bot = -1
    for i in range(len(s)):
        for j in range(len(s[0])):
            if s[i][j]:
                # print i, j
                if i < left:
                    left = i

                if i > right:
                    right = i

                if j < top:
                    top = j

                if j > bot:
                    bot = j

    if right == -1:
        return 1

    w = right - left + 1
    h = bot - top + 1

    min_tile = 10000
    if w < h:
        if len(s) < h:
            return -1
        else:
            for a in range(h - w + 1):
                num_tile = 0
                for i in range(max(left - a - 1, 0), max(left - a - 1, 0) + h):
                    for j in range(top, bot + 1):
                        if not s[i][j]:
                            num_tile += 1

                if num_tile < min_tile:
                    min_tile = num_tile
    elif w > h:
        if len(s[0]) < w:
            return -1
        else:
            for a in range(w - h):
                num_tile = 0
                for i in range(left, right + 1):
                    for j in range(max(top - a - 1, 0), max(top - a - 1, 0) + w):
                        if not s[i][j]:
                            num_tile += 1
                if num_tile < min_tile:
                    min_tile = num_tile
    else:
        min_tile = 0
        for i in range(left, right + 1):
            for j in range(top, bot + 1):
                if not s[i][j]:
                    min_tile += 1

    return min_tile

line = int(raw_input().split(' ')[0])
sq = [list(raw_input()) for _ in range(line)]

print black_square(sq)