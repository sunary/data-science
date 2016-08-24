__author__ = 'sunary'


import random


team_a = []
team_b = []


def random_kda():
    global team_a, team_b
    team_a = [[0, 0, 0] for _ in range(5)]
    team_b = [[0, 0, 0] for _ in range(5)]

    for _ in range(random.randrange(10, 100)):
        kill = random.randrange(5)
        died = random.randrange(5)
        assist = [random.randrange(2) for _ in range(5)]

        if random.randrange(2):
            team_a[kill][0] += 1
            team_b[died][1] += 1
            for i in range(5):
                if i != kill:
                    team_a[i][2] += assist[i]
        else:
            team_b[kill][0] += 1
            team_a[died][1] += 1
            for i in range(5):
                if i != kill:
                    team_b[i][2] += assist[i]


def score():
    a_kill = sum([x[0] for x in team_a]) or 1
    b_kill = sum([x[0] for x in team_b]) or 1

    a_score = [0]* 5
    b_score = [0]* 5
    sum_assist_a = sum([x[2] for x in team_a])
    sum_assist_b = sum([x[2] for x in team_b])
    a_ratio = (0.5, (0.5 + 0.5* sum_assist_b/a_kill)/5, 0.125* sum_assist_a/b_kill)
    b_ratio = (0.5, (0.5 + 0.5* sum_assist_a/b_kill)/5, 0.125* sum_assist_b/a_kill)
    print a_ratio, b_ratio
    for i in range(5):
        a_score[i] += a_ratio[0] * team_a[i][0]/a_kill
        a_score[i] -= a_ratio[1] * team_a[i][1]/b_kill
        a_score[i] += a_ratio[2] * team_a[i][2]/a_kill
        a_score[i] = int(a_score[i] * a_kill/b_kill * 100)

        b_score[i] += b_ratio[0] * team_b[i][0]/b_kill
        b_score[i] -= b_ratio[1] * team_b[i][1]/a_kill
        b_score[i] += b_ratio[2] * team_b[i][2]/b_kill
        b_score[i] = int(b_score[i] * b_kill/a_kill * 100)

    return a_score, b_score


if __name__ == '__main__':
    random_kda()
    s = score()
    print team_a
    print s[0]
    print team_b
    print s[1]