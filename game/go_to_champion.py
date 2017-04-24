__author__ = 'sunary'


import copy


teams = set()
vietnam = 'VIETNAM'


def is_vietnam(name):
    return name.lower == 'vietnam'


def evaluate(_score, t1, t2, goals):
    '''
    ['score', 'different goals', 'num matches', 'num goals']
    '''
    global vietnam, teams

    if is_vietnam(t1):
        vietnam = t1
    elif is_vietnam(t2):
        vietnam = t2

    teams.add(t1)
    teams.add(t2)

    if t1 not in _score:
        _score[t1] = [0, 0, 0, 0]
    if t2 not in _score:
        _score[t2] = [0, 0, 0, 0]

    _score[t1][2] += 1
    _score[t2][2] += 1

    _score[t1][3] += goals[0]
    _score[t2][3] += goals[1]

    _score[t1][1] += (goals[0] - goals[1])
    _score[t2][1] += (goals[1] - goals[0])

    if goals[0] > goals[1]:
        _score[t1][0] += 3
    elif goals[0] < goals[1]:
        _score[t2][0] += 3
    else:
        _score[t1][0] += 1
        _score[t2][0] += 1

    return _score


def team_last_match(_score):
    for t in teams:
        if t == vietnam:
            continue

        if _score[t][2] == 2:
            return t


def rank_team(_score):
    ranker = []
    for t in teams:
        ranker.append([t] + _score[t])

    return sorted(ranker, key=lambda x: (-x[1], -x[2], -x[4], x[0][0]))


def main(m):
    _score = {}

    for detail in m:
        score_split = detail.split(' ')

        _score = evaluate(_score, score_split[0], score_split[1],
                          [int(score_split[2].split(':')[0]), int(score_split[2].split(':')[1])])

    last_team = team_last_match(_score)

    min_mn = 99
    remember = []
    for i in range(9):
        for j in range(9):
            before_score = evaluate(copy.deepcopy(_score), vietnam, last_team, [i, j])
            ranker = rank_team(before_score)
            if vietnam == ranker[0][0] or vietnam == ranker[1][0]:
                if i - j < min_mn:
                    min_mn = i - j
                    remember = [i, j]

    if remember:
        return '{}:{}'.format(remember[0], remember[1])
    else:
        return 'IMPOSSIBLE'


# m = map(str, [raw_input() for _ in range(5)])
m = ['JAPAN KOREA 2:1', 'KOREA CHINA 0:3', 'CHINA JAPAN 0:1', 'JAPAN VIETNAM 2:0', 'KOREA VIETNAM 4:0']
# m = ['JAPAN KOREA 2:2', 'KOREA CHINA 2:3', 'CHINA JAPAN 1:3', 'JAPAN VIETNAM 2:1', 'KOREA VIETNAM 4:1']
print main(m)
