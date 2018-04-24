__author__ = 'sunary'


def text_volume(text):
    max_volume = 0

    for s in text.split(' '):
        count_vol = 0
        for x in s:
            if 'A' <= x <= 'Z':
                count_vol += 1

        if count_vol > max_volume:
            max_volume = count_vol

    return max_volume


def rgb_flag(f):
    color = ['R', 'G', 'B']
    positions = [[len(f), len(f[0]), 0, 0],
                [len(f), len(f[0]), 0, 0],
                [len(f), len(f[0]), 0, 0]]

    for i in range(len(f)):
        for j in range(len(f[0])):
            index = color.index(f[i][j])
            if positions[index][0] > i:
                positions[index][0] = i

            if positions[index][1] > j:
                positions[index][1] = j

            if positions[index][2] < i:
                positions[index][2] = i

            if positions[index][3] < j:
                positions[index][3] = j

    width_r = positions[0][2] - positions[0][0]
    width_g = positions[1][2] - positions[1][0]
    width_b = positions[2][2] - positions[2][0]

    height_r = positions[0][3] - positions[0][1]
    height_g = positions[1][3] - positions[1][1]
    height_b = positions[2][3] - positions[2][1]

    if width_r == width_g and width_g == width_b and height_r == height_g and height_g == height_b \
        and (width_r + 1) * (height_r + 1) + (width_g + 1) * (height_g + 1) + (width_b + 1) * (height_b + 1) == len(f)*len(f[0]):
        return 'YES'

    return 'NO'


def two_seals(a, b, seals):
    max_fit = 0

    for i in range(len(seals)):
        for j in range(i + 1, len(seals)):
            if (max(seals[i][0], seals[j][0]) <= a and seals[i][1] + seals[j][1] <= b) or \
                    (max(seals[i][0], seals[j][0]) <= b and seals[i][1] + seals[j][1] <= a) or \
                    (seals[i][0] + seals[j][0] <= a and max(seals[i][1], seals[j][1]) <= b) or \
                    (seals[i][0] + seals[j][0] <= b and max(seals[i][1], seals[j][1]) <= a) or \
                    (max(seals[i][0], seals[j][1]) <= a and seals[i][1] + seals[j][0] <= b) or \
                    (max(seals[i][0], seals[j][1]) <= b and seals[i][1] + seals[j][0] <= a) or \
                    (seals[i][0] + seals[j][1] <= a and max(seals[i][1], seals[j][0]) <= b) or \
                    (seals[i][0] + seals[j][1] <= b and max(seals[i][1], seals[j][0]) <= a):

                if max_fit < seals[i][0] * seals[i][1] + seals[j][0] * seals[j][1]:
                    max_fit = seals[i][0] * seals[i][1] + seals[j][0] * seals[j][1]

    return max_fit


def round_subset(k, a):
    divide = []

    for i in range(len(a)):
        d = [0, 0, i]

        x = int(a[i])
        while x % 5 == 0:
            d[0] += 1
            x /= 5

        while x % 2 == 0:
            d[1] += 1
            x /= 2

        divide.append(d)

    divide5 = sorted(divide, key=lambda x: [-x[0], -x[1]])[:k]
    divide2 = sorted(divide, key=lambda x: [-x[1], -x[0]])[:k]
    divide_id = set()

    d2 = 0
    d5 = 0
    start_d2 = 0
    start_d5 = 0
    for _ in range(k):
        if d2 <= d5:
            while divide2[start_d2][2] in divide_id:
                start_d2 += 1

            d2 += divide2[start_d2][1]
            d5 += divide2[start_d2][0]
            divide_id.add(divide2[start_d2][2])
        else:
            while divide5[start_d5][2] in divide_id:
                start_d5 += 1

            d2 += divide5[start_d5][1]
            d5 += divide5[start_d5][0]
            divide_id.add(divide5[start_d5][2])

    return min(d2, d5)

k = int(raw_input().split(' ')[1])
a = [x for x in raw_input().split(' ')]
print round_subset(k, a)