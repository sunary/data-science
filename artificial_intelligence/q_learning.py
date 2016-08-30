__author__ = 'sunary'


learning_rate = 0.5
BOARD_SIZE = 10
sign4 = [[-1, 0], [0, -1], [0, 1], [1, 0]]
sign8 = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]

weight = [[-1]*100 for _ in range(100)]


def q_learning(src=(7, 9), dest=(0, 0)):
    # init board
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            for s in sign4:
                if i + s[0] in range(BOARD_SIZE) and j + s[1] in range(BOARD_SIZE):
                    if (i + s[0], j + s[1]) == dest:
                        weight[i*BOARD_SIZE + j][(i + s[0])*BOARD_SIZE + (j + s[1])] = 100
                    else:
                        weight[i*BOARD_SIZE + j][(i + s[0])*BOARD_SIZE + (j + s[1])] = 0

    # learning
    for _ in range(50):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                for s in sign4:
                    if i + s[0] in range(BOARD_SIZE) and j + s[1] in range(BOARD_SIZE):
                        cell_weights = []
                        for s2 in sign4:
                            if i + s[0] + s2[0] in range(BOARD_SIZE) and j + s[1] + s2[1] in range(BOARD_SIZE) and\
                                    weight[(i + s[0])*BOARD_SIZE + (j + s[1])][(i + s[0] + s2[0])*BOARD_SIZE + (j + s[1] + s2[1])] >= 0:
                                cell_weights.append(weight[(i + s[0])*BOARD_SIZE + (j + s[1])][(i + s[0] + s2[0])*BOARD_SIZE + (j + s[1] + s2[1])])

                        weight[i*BOARD_SIZE + j][(i + s[0])*BOARD_SIZE + (j + s[1])] =\
                            max(weight[i*BOARD_SIZE + j][(i + s[0])*BOARD_SIZE + (j + s[1])], learning_rate * max(cell_weights))

    # find path
    path = []
    i, j = src
    while True:
        path.append((i, j))
        cell_weights = []
        for s in sign4:
            if i + s[0] in range(BOARD_SIZE) and j + s[1] in range(BOARD_SIZE):
                cell_weights.append((weight[i*BOARD_SIZE + j][(i + s[0])*BOARD_SIZE + (j + s[1])], i + s[0], j + s[1]))

        i, j = argmax(cell_weights)
        if (i, j) == dest:
            path.append((i, j))
            print path
            break

    # print weight
    for i in range(BOARD_SIZE **2):
        for j in range(BOARD_SIZE **2):
            if weight[i][j] > 0:
                print str(((i/BOARD_SIZE, i%BOARD_SIZE), (j/BOARD_SIZE, j%BOARD_SIZE))) + ': ' + str(weight[i][j])


def argmax(cell_weights):
    max_arg = cell_weights[0][1], cell_weights[0][2]
    max_value = cell_weights[0][0]

    for v in cell_weights[1:]:
        if v[0] > max_value:
            max_arg = v[1], v[2]
            max_value = v[0]

    return max_arg

if __name__ == '__main__':
    q_learning()