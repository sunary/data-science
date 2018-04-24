__author__ = 'sunary'


def palin(text):
    text = text.replace('0', '')
    if not text or text == text[::-1]:
        return 'YES'

    return 'NO'


def kayak_dp(weights):
    INF = 1000000
    weights = sorted(weights)

    scores = [[INF]*len(weights) for _ in range(3)]

    scores[0][0] = weights[0]
    scores[1][0] = 0
    scores[2][0] = 0
    scores[0][1] = weights[1] - weights[0]
    scores[1][1] = weights[1]
    scores[2][1] = 0
    for i in range(2, len(weights)):
        scores[0][i] = scores[0][i-2] + weights[i] - weights[i - 1]
        scores[1][i] = scores[1][i-2] + weights[i] - weights[i - 1]
        scores[2][i] = min(scores[0][i-2], scores[2][i-2] + weights[i] - weights[i-1])

        scores[1][i] = min(scores[1][i], scores[0][i-1])
        scores[2][i] = min(scores[2][i], scores[1][i-1])

    return min(scores[0][-1], scores[1][-1], scores[2][-1])

raw_input()
print kayak_dp([int(s) for s in raw_input().split(' ')])