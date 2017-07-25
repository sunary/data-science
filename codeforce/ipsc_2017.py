__author__ = 'sunary'


maxim_start = 987654321


def nnext(n):
    n = str(n)
    maxim_lower = ''

    digits = list('9876543210')

    while len(maxim_lower) < len(n):
        appended = False

        for max_index in range(len(digits)):
            if maxim_lower + digits[max_index] < n:
                maxim_lower += digits[max_index]
                del digits[max_index]
                appended = True
                break
            else:
                max_index += 1

        if not appended:
            i = 1
            while i < len(maxim_lower):
                j = 0
                while j < len(digits):
                    if digits[j] < maxim_lower[-i]:
                        maxim_lower = maxim_lower[:-i] + digits[j]
                        digits = sorted([x for x in list('0123456789') if x not in maxim_lower])[::-1]

                        j = len(digits)
                        i = len(maxim_lower)

                    j += 1
                i += 1

    return int(maxim_lower)

# print nnext(965432107)

def prob_d(N):
    min_a = [1] * 100
    maxim = min(maxim_start, nnext(N))

    for _ in range(10):
        a = []
        n = N
        while n > maxim:
            a.append(maxim)
            n -= maxim

        while not dazzling_number(n):
            m = maxim
            while m > n:
                m = m/10

            a.append(m)
            n -= m

        a.append(n)

        if len(a) < len(min_a):
            min_a = a[:]

        maxim = nnext(maxim)

        if len(min_a) <= 2:
            return min_a

    return min_a


def dazzling_number(n):
    s = str(n)
    return len(s) == len(set(s))

with open('/Users/sunary/Downloads/d1.in', 'r') as of:
    input = of.read().split('\n')

with open('/Users/sunary/Downloads/d1.out', 'w') as of:
    for x in input:
        if x:
            result = prob_d(int(x))
            of.write('{} {}\n'.format(len(result), ' '.join([str(x) for x in result])))