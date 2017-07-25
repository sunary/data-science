__author__ = 'sunary'



def binary(s):
    number = ''
    s = s.split('0')
    for x in s:
        number += str(len(x))

    return number

def five_in_row(b):
    for i in range(10):
        for j in range(10):
            if b[i][j] != 'O':
                filled = b[i][j] == '.'
                passed = True
                for t in range(1, 5):
                    if legal_tile(i + t, j + t) and (b[i + t][j + t] == 'X' or (not filled and b[i + t][j + t] == '.')):
                        if b[i + t][j + t] == '.':
                            filled = True
                    else:
                        passed = False
                        break
                if passed:
                    return 'YES'

                filled = b[i][j] == '.'
                passed = True
                for t in range(1, 5):
                    if legal_tile(i + t,j) and (b[i + t][j] == 'X' or (not filled and b[i + t][j] == '.')):
                        if b[i + t][j] == '.':
                            filled = True
                    else:
                        passed = False
                        break
                if passed:
                    return 'YES'

                filled = b[i][j] == '.'
                passed = True
                for t in range(1, 5):
                    if legal_tile(i, j + t) and (b[i][j + t] == 'X' or (not filled and b[i][j + t] == '.')):
                        if b[i][j + t] == '.':
                            filled = True
                    else:
                        passed = False
                        break
                if passed:
                    return 'YES'

                filled = b[i][j] == '.'
                passed = True
                for t in range(1, 5):
                    if legal_tile(i - t, j + t) and (b[i - t][j + t] == 'X' or (not filled and b[i - t][j + t] == '.')):
                        if b[i - t][j + t] == '.':
                            filled = True
                    else:
                        passed = False
                        break

                if passed:
                    return 'YES'

    return 'NO'


def legal_tile(x, y):
    return x >= 0 and x < 10 and y >= 0 and y < 10


def solving(d, k):
    d = sorted(d)

    lower_than = 0

    last_k = k
    for x in d:
        if x <= k:
            lower_than += 1
            last_k = x
        else:
            break

    for x in d[lower_than:]:
        if last_k >= (x + 1)/2:
            lower_than += 1
            last_k = x
        else:
            break

    return len(d) - lower_than

k = int(raw_input().split(' ')[1])
d = [int(x) for x in raw_input().split(' ')]

print solving(d, k)