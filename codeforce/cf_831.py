__author__ = 'sunary'


def udimol(a):
    last = a[0]
    status = 0
    for x in a[1:]:
        if status == 0:
            if x == last:
                status = 1
            elif x > last:
                pass
            else:
                status = 2
            last = x
        elif status == 1:
            if x < last:
                status = 2
                last = x
            elif x == last:
                last = x
            else:
                return 'NO'
        else:
            if x < last:
                last = x
            else:
                return 'NO'

    return 'YES'


def keyboard(key, value, text):
    result = ''
    for c in text:
        if c not in '0123456789':
            t = value[key.index(c.lower())]
            if not c.islower():
                t = chr(ord(t) - 32)
        else:
            t = c

        result += t

    return result


def card_sorting(cards):
    for i in range(len(cards)):
        cards[i] = [cards[i], i]


    s = sorted(cards)
    print s

    start = 0
    turns = 0
    sub = 0
    while s:
        if s[0][0] == start:
            turns += s[0][1] - sub
        else:
            turns += len(s) + s[0][1] - sub
            print turns

        start = s[0][0]
        sub += 1
        s = s[1:]

    return turns

raw_input()
x = [int(x) for x in raw_input().split(' ')]

print card_sorting(x)