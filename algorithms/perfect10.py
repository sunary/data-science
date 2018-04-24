__author__ = 'sunary'


def perfect_sub10(n):
    value = 0
    start = 0
    mark = [0] * len(n)
    for i in range(len(n)):
        value += int(n[i])
        while value > 10:
            value -= int(n[start])
            start += 1

        if value == 10:
            for j in range(start, i + 1):
                mark[j] = 1

    return 'YES' if all(mark) else 'NO'


print(perfect_sub10(raw_input()))