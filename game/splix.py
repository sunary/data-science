__author__ = 'sunary'


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
                        priority_direction[x - 2] != LATEST_MOVE:
            distance = shorted_path(_board, [l[0] + m[0], l[1] + m[1]], [d])
            not_prefer_latest_move = not priority_direction[x] != LATEST_MOVE
            prefer_home = not is_home(_board[l[0] + m[0]][l[1] + m[1]])
            if [distance, not_prefer_latest_move, prefer_home] < min_step:
                min_step = [distance, not_prefer_latest_move, prefer_home]
                next_move_id = x

    return next_move_id


def shorted_path(_board, l, dests):
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

        for i, j in priority_direction_move:
            n = [current[0] + i, current[1] + j]
            if n in dests:
                return board[current[0]][current[1]] + 1
            if (is_empty(_board[n[0]][n[1]]) or is_home(_board[n[0]][n[1]])) and board[n[0]][n[1]] == 0:
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
        if not check_dangerous(enemies_location=_locations[1:], check_points=[[i, j]]):
            next_move_id = goto(_board, _locations[0], [i, j])
            if next_move_id >= 0:
                return priority_direction[next_move_id]


def len_home_away(_board, _locations):
    unstable_tiles = []

    for i, j in priority_direction_move:
        if _board[_locations[0][0] + i][_locations[0][1] + j] >= 0:
            unstable_tiles.append([_locations[0][0] + i, _locations[0][1] + j])

    for i in range(SIZE[0]):
        for j in range(SIZE[1]):
            if is_unstable(_board[i][j]):
                unstable_tiles.append([i, j])

    min_distance = INFINITY_VALUE
    for i, j in unstable_tiles:
        for ei, ej in _locations[1:]:
            distance = abs(i - ei) + abs(j - ej)
            if distance < min_distance:
                min_distance = distance

    count_home = 0
    for i in range(SIZE[0]):
        for j in range(SIZE[1]):
            if is_home(_board[i][j]):
                count_home += 1

    safety_mode = (count_home >= SIZE[0]*SIZE[1] * 3/5)
    return max(1, min_distance - (3 if safety_mode else 1))


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


def check_dangerous(_board=None, enemies_location=[], check_points=[], size=4):
    if check_points:
        unstable_tiles = check_points
    else:
        unstable_tiles = []
        for i in range(SIZE[0]):
            for j in range(SIZE[1]):
                if is_unstable(_board[i][j]):
                    unstable_tiles.append([i, j])

    for l in enemies_location:
        for i, j in unstable_tiles:
            if l[0] == -1:
                continue
            if abs(l[0] - i) + abs(l[1] - j) <= size:
                return True

    return False


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
        if next_move_id >= 0 and priority_direction[next_move_id - 2] != LATEST_MOVE:
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

    move = ''
    if is_home(_board[_locations[0][0]][_locations[0][1]]):
        move = find_nearest_empty(_board, _locations)
    else:
        size = len_home_away(_board, _locations)
        if not check_dangerous(_board=_board, enemies_location=_locations[1:], size=size):
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
    board = map(str, [raw_input() for _ in range(SIZE[0])])
    locations = map(str, [raw_input() for _ in range(num_player)])

num_player = 2
HOME_VALUE = 1 * 2 - 1

S = '''003333333333333333333333333333
003333333333333333333333333333
003333333333333333333333333333
003333333333333333333333333333
003333333333333333333333333333
003333333333333333333333111111
033333333333333333333331111111
033333333333333333333311111111
033331111333333333311111111111
033331111333333333111111111111
001111111333333331111111111111
000000111333311111111111111111
111111111111111111111111111111
111111111111111111111111111111
111111111111111111111111111111
111111111111111131111111111111
111111000011111131111111111111
111110000011110331111111111111
111110000000110331111111111111
111110000000110333333333333333
10 4
9 3
'''
board = map(str, [S.split('\n')[i] for i in range(SIZE[0])])
locations = map(str, [S.split('\n')[i] for i in range(SIZE[0], SIZE[0] + num_player)])
print main(board, locations)
