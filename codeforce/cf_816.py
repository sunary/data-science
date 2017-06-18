__author__ = 'sunary'


def time_palindrome(hh, mm):
    i = 0
    while True:
        if check_paldindrome(hh, mm):
            return i
        else:
            i += 1
            if mm == 59:
                if hh == 23:
                    hh = 0
                else:
                    hh += 1
                mm = 0
            else:
                mm += 1

def check_paldindrome(h1, h2):
    str1 = str(h1) if h1 > 9 else '0' + str(h1)
    str2 = str(h2) if h2 > 9 else '0' + str(h2)
    return str1 == str2[::-1]


def grid_game(b):
    result = []
    while check(b):
        dosomething = False
        if len(b) < len(b[0]):
            for i in range(len(b)):
                min_r = min(b[i])
                if min_r:
                    dosomething = True
                    result += ['row {}'.format(i + 1) for _ in range(min_r)]
                    for j in range(len(b[0])):
                        b[i][j] -= min_r

        for j in range(len(b[0])):
            min_c = min([b[i][j] for i in range(len(b))])
            if min_c:
                dosomething = True
                result += ['col {}'.format(j + 1) for _ in range(min_c)]
                for i in range(len(b)):
                    b[i][j] -= min_c

        if len(b) >= len(b[0]):
            for i in range(len(b)):
                min_r = min(b[i])
                if min_r:
                    dosomething = True
                    result += ['row {}'.format(i + 1) for _ in range(min_r)]
                    for j in range(len(b[0])):
                        b[i][j] -= min_r

        if not dosomething:
            return -1
    return '\n'.join([str(len(result))] + result)


def check(b):
    for i in range(len(b)):
        for j in range(len(b[0])):
            if b[i][j]:
                return True

    return False

n = int(raw_input().split(' ')[0])
board = []
for _ in range(n):
    board.append([int(x) for x in raw_input().split(' ')])

print grid_game(board)
