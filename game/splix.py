__author__ = 'sunary'


import sys


INFINITY_VALUE = 9999
SIZE = (20, 30)
HOME_VALUE = 1
LATEST_MOVE = ''

priority_direction = ['RIGHT', 'DOWN', 'LEFT', 'UP']
priority_direction_move = [[0, 1], [1, 0], [0, -1], [-1, 0]]
priority_direction_range = [lambda x, y: [(x, b) for b in range(y + 1, SIZE[1])],
                            lambda x, y: [(a, y) for a in range(x + 1, SIZE[0])],
                            lambda x, y: [(x, b) for b in range(y - 1, -1, -1)],
                            lambda x, y: [(a, y) for a in range(x - 1, -1, -1)]]


def is_empty(value):
    return value >= 0 and not (is_unstable(value) or is_home(value))


def is_unstable(value):
    return value == HOME_VALUE + 1


def is_home(value):
    return value == HOME_VALUE


def goto(_board, l, d):
    min_step = [INFINITY_VALUE, True, True]
    next_move_id = -1
    for x, m in enumerate(priority_direction_move):
        if (is_empty(_board[l[0] + m[0]][l[1] + m[1]]) or is_home(_board[l[0] + m[0]][l[1] + m[1]])) and \
                (is_home(_board[l[0]][l[1]]) or priority_direction[x - 2] != LATEST_MOVE):
            distance = shorted_path(_board, [l[0] + m[0], l[1] + m[1]], [d])
            not_prefer_latest_move = not priority_direction[x] != LATEST_MOVE
            prefer_home = not is_home(_board[l[0] + m[0]][l[1] + m[1]])
            if [distance, not_prefer_latest_move, prefer_home] < min_step:
                min_step = [distance, not_prefer_latest_move, prefer_home]
                next_move_id = x

    return next_move_id


def shorted_path(_board, l, dests, unstable_value=None):
    if unstable_value is None:
        unstable_value = HOME_VALUE + 1

    if l in dests:
        return 1

    board = [[-1 for _ in range(SIZE[1] + 2)] for _ in range(SIZE[0] + 2)]

    for i in range(SIZE[0]):
        for j in range(SIZE[1]):
            board[i][j] = 0

    queue_path = list()
    queue_path.append(l)

    board[l[0]][l[1]] = 1
    while queue_path:
        current = queue_path[0]
        queue_path = queue_path[1:]

        for x, (i, j) in enumerate(priority_direction_move):
            if board[current[0]][current[1]] == 0 and LATEST_MOVE == priority_direction[x - 2]:
                continue

            n = [current[0] + i, current[1] + j]
            if n in dests:
                return board[current[0]][current[1]] + 1

            if _board[n[0]][n[1]] >= 0 and _board[n[0]][n[1]] != unstable_value and board[n[0]][n[1]] == 0:
                queue_path.append(n)
                board[n[0]][n[1]] = board[current[0]][current[1]] + 1

    return INFINITY_VALUE


def find_nearest_empty(_board, _locations):
    def empty_near_home(l):
        if is_empty(_board[l[0]][l[1]]):
            for i, m in enumerate(priority_direction_move):
                if is_home(_board[l[0] + m[0]][l[1] + m[1]]):
                    return True

        return False

    empty_tiles = []

    for i in range(SIZE[0]):
        for j in range(SIZE[1]):
            if empty_near_home([i, j]):
                empty_tiles.append([i, j, abs(_locations[0][0] - i) + abs(_locations[0][1] - j)])

    nearest_l = [INFINITY_VALUE, INFINITY_VALUE]
    for l in _locations[1:]:
        if l[0] == -1:
            continue

        if abs(_locations[0][0] - l[0]) + abs(_locations[0][1] - l[1]) < abs(_locations[0][0] - nearest_l[0]) + abs(_locations[0][1] - nearest_l[1]):
            nearest_l = [l[0], l[1]]

    empty_tiles = sorted(empty_tiles, key=lambda x: [x[2], -(abs(x[0] - nearest_l[0]) + abs(x[1] - nearest_l[1]))])

    for i, j, _ in empty_tiles:
        next_move_id = goto(_board, _locations[0], [i, j])
        if next_move_id >= 0 and safe_step(_board, _locations, next_move_id):
            return priority_direction[next_move_id]


def safe_step(_board, _locations, next_move_id):
    for l in _locations[1:]:
        if l[0] == -1:
            continue
        if abs(_locations[0][0] + priority_direction_move[next_move_id][0] - l[0]) + abs(_locations[0][1] + priority_direction_move[next_move_id][1] - l[1]) <= 2:
            return False

    return True


def distance_home_away(_board, _locations):
    unstable_tiles = []

    for i, j in priority_direction_move:
        if _board[_locations[0][0] + i][_locations[0][1] + j] >= 0:
            unstable_tiles.append([_locations[0][0] + i, _locations[0][1] + j])

    for i in range(SIZE[0]):
        for j in range(SIZE[1]):
            if is_unstable(_board[i][j]):
                unstable_tiles.append([i, j])

    min_distance = SIZE[0]
    for i, l in enumerate(_locations[1:]):
        if l[0] == -1:
            continue

        enemy_unstable_value = (i + 2) * 2
        if enemy_unstable_value == HOME_VALUE + 1:
            enemy_unstable_value = 2

        distance = shorted_path(_board, l, dests=unstable_tiles, unstable_value=enemy_unstable_value) - 1
        if distance < min_distance:
            min_distance = distance

        for i2 in range(SIZE[0]):
            for j2 in range(SIZE[1]):
                if _board[i2][j2] == enemy_unstable_value - 1:
                    for i3, j3 in unstable_tiles:
                        distance = abs(l[0] - i2) + abs(l[1] - j2) + abs(i2 - i3) + abs(j2 - j3)
                        if distance < min_distance:
                            min_distance = distance

    return min_distance


def find_boundary(_board, _locations, size):
    home_tiles = []
    for i in range(SIZE[0]):
        for j in range(SIZE[1]):
            if is_home(_board[i][j]):
                home_tiles.append([i, j])

    max_distance = [0, False]
    next_move_id = -1
    for i, m in enumerate(priority_direction_move):
        if is_empty(_board[_locations[0][0] + m[0]][_locations[0][1] + m[1]]) and priority_direction[i - 2] != LATEST_MOVE:
            distance = shorted_path(_board, [_locations[0][0] + m[0], _locations[0][1] + m[1]], home_tiles)
            prefer_more_tiles = not any([is_unstable(_board[a][b]) for a, b in priority_direction_range[i](_locations[0][0], _locations[0][1])])
            if size > distance and [distance, prefer_more_tiles] > max_distance:
                max_distance = [distance, prefer_more_tiles]
                next_move_id = i

    if next_move_id >= 0:
        return priority_direction[next_move_id]


def back_home(_board, _locations):
    home_tiles = []
    for i in range(SIZE[0]):
        for j in range(SIZE[1]):
            if is_home(_board[i][j]):
                home_tiles.append([i, j, abs(i - _locations[0][0]) + abs(j - _locations[0][1])])

    if len(home_tiles) > 13:
        home_tiles = sorted(home_tiles, key=lambda x: x[2])[:13]

    for i in range(len(home_tiles)):
        home_tiles[i][2] = shorted_path(_board, _locations[0], [[home_tiles[i][0], home_tiles[i][1]]])

    home_tiles = sorted(home_tiles, key=lambda x: x[2])
    for i, j, _ in home_tiles:
        next_move_id = goto(_board, _locations[0], [i, j])
        if next_move_id >= 0 and (is_home(_board[_locations[0][0]][_locations[0][1]]) or priority_direction[next_move_id - 2] != LATEST_MOVE):
            return priority_direction[next_move_id]


def main(board_, locations_):
    global LATEST_MOVE

    _board = [[-1 for _ in range(SIZE[1] + 2)] for _ in range(SIZE[0] + 2)]
    for i in range(SIZE[0]):
        for j in range(SIZE[1]):
            _board[i][j] = int(board_[i][j])

    _locations = []
    for l in locations_:
        _locations.append([int(l.split(' ')[0]), int(l.split(' ')[1])])

    _locations[0], _locations[(HOME_VALUE - 1)/2] = _locations[(HOME_VALUE - 1)/2], _locations[0]

    if is_home(_board[_locations[0][0]][_locations[0][1]]):
        move = find_nearest_empty(_board, _locations)
    else:
        size = distance_home_away(_board, _locations)
        move = find_boundary(_board, _locations, size)
    if not move:
        move = back_home(_board, _locations)
    if not move:
        for l in _locations[1:]:
            if l[0] == -1:
                continue
            next_move_id = goto(_board, _locations[0], l)
            if next_move_id >= 0:
                move = priority_direction[next_move_id]
                break

    LATEST_MOVE = move
    return move


num_player = int(raw_input())
HOME_VALUE = int(raw_input()) * 2 - 1
board = map(str, [raw_input() for _ in range(SIZE[0])])
locations = map(str, [raw_input() for _ in range(num_player)])

while True:
    print main(board, locations)
    sys.stdout.flush()
    board = map(str, [raw_input() for _ in range(SIZE[0])])
    locations = map(str, [raw_input() for _ in range(num_player)])

num_player = 2
HOME_VALUE = 2 * 2 - 1

S = '''000000000000001111111110033333
000000000000001111111111133333
000000000000001111111111133333
000000000000001111111111111113
000000000000000000111111111111
000000000000000000111111111111
000000000000000000001111111113
000000000000000000001111113333
000000000000000000001111111333
000000000000000000011111111113
000000333333333333311111131113
000000333333333333111111333333
000000000000333331111111333333
000000000000033331111113333333
000000000000003331111113333333
000000000000000331111113333333
000000000000000001111113333333
000000000000000001111133333333
000000000000000000111133333333
000000000000000000111113333333
3 28
3 29
'''
board = map(str, [S.split('\n')[i] for i in range(SIZE[0])])
locations = map(str, [S.split('\n')[i] for i in range(SIZE[0], SIZE[0] + num_player)])
print main(board, locations)
