__author__ = 'sunary'


import random


class Tictactoe():

    '''
    Human: 1
    Machine: 2
    '''

    def __init__(self):
        self.human_turn = True
        self.user_board = [0]*9
        self.line = [[0, 1, 2],
                     [3, 4, 5],
                     [6, 7, 8],
                     [0, 3, 6],
                     [1, 4, 7],
                     [2, 5, 8],
                     [0, 4, 8],
                     [2, 4, 6]]

    def start(self):
        who_win = 0
        text = ['tie', 'human win', 'machine win']
        while True:
            if self.human_turn:
                random_move = random.randint(0, len(self.user_board) - 1)
                while True:
                    if self.user_board[random_move] == 0:
                        self.user_board[random_move] = 1
                        break
                    random_move -= 1
                self.human_turn = False
            else:
                max_score = -100
                select_id_max_score = 0
                for i in range(len(self.user_board)):
                    if self.user_board[i] == 0:
                        turn_score = self.next_move(self.human_turn, self.user_board[:], i)
                        if turn_score > max_score:
                            max_score = turn_score
                            select_id_max_score = i

                self.user_board[select_id_max_score] = 2
                self.human_turn = True

            self.print_board()
            who_win = self.board_status(self.user_board)
            if who_win != -1:
                break

        return text[who_win]

    def board_status(self, user_board):
        #who win
        for i in range(len(self.line)):
            if user_board[self.line[i][0]] != 0 and user_board[self.line[i][0]] == user_board[self.line[i][1]]\
               and user_board[self.line[i][0]] == user_board[self.line[i][2]]:
                return user_board[self.line[i][0]]
        #tie
        if all([tile != 0 for tile in user_board]):
            return 0

        return -1

    def next_move(self, human_turn, user_board, select_id):
        if human_turn:
            user_board[select_id] = 1
        else:
            user_board[select_id] = 2

        status_temp_board = self.board_status(user_board)
        if status_temp_board == 0:
            return 1
        elif status_temp_board == 2:
            return 5
        elif status_temp_board == 1:
            return -8

        if human_turn:
            max_score = -100
            for i in range(len(user_board)):
                if user_board[i] == 0:
                    next_move_score = self.next_move(False, user_board, i)
                    max_score = next_move_score if next_move_score > max_score else max_score
            return max_score
        else:
            min_score = 100
            for i in range(len(user_board)):
                if user_board[i] == 0:
                    next_move_score = self.next_move(True, user_board, i)
                    min_score = next_move_score if next_move_score < min_score else min_score
            return min_score

    def print_board(self):
        print '%s %s %s' % (self.user_board[0], self.user_board[1], self.user_board[2])
        print '%s %s %s' % (self.user_board[3], self.user_board[4], self.user_board[5])
        print '%s %s %s' % (self.user_board[6], self.user_board[7], self.user_board[8])
        print '+---+'

if __name__ == '__main__':
    tictactoe = Tictactoe()
    print tictactoe.start()