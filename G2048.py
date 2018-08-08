import random


class Board(object):
    def __init__(self, size=4):
        self.board = []
        self.over = False
        self.size = size
        for i in range(self.size):
            self.board.append([0 for j in range(self.size)])
        for i in range(2):
            self.__new()
        self.merged = []

    def __up(self):
        need_new = False
        for k in range(self.size):
            for i in range(self.size):
                for j in range(1, self.size):
                    need_new = self.__step(j, i, j-1, i) or need_new
        return self.__finish_move('up', need_new)

    def __down(self):
        need_new = False
        for k in range(self.size):
            for i in range(self.size):
                for j in reversed(range(self.size-1)):
                    need_new = self.__step(j, i, j+1, i) or need_new
        return self.__finish_move('down', need_new)

    def __left(self):
        need_new = False
        for k in range(self.size):
            for i in range(self.size):
                for j in range(1, self.size):
                    need_new = self.__step(i, j, i, j-1) or need_new
        return self.__finish_move('left', need_new)

    def __right(self):
        need_new = False
        for k in range(self.size):
            for i in range(self.size):
                for j in reversed(range(self.size-1)):
                    need_new = self.__step(i, j, i, j+1) or need_new
        return self.__finish_move('right', need_new)

    def __finish_move(self, direction, need_new):
        if need_new:
            print 'Direction: ' + direction
            self.__new()
            return True
        else:
            if not self.__has_a_move():
                self.over = True
            print "Can't go " + direction
            return False

    def __has_zeros(self):
        for row in self.board:
            if 0 in row:
                return True
        return False

    def __has_a_merge(self):
        for i in range(self.size):
            for j in range(self.size):
                if (j < 3 and self.board[i][j] == self.board[i][j+1]) or (i < 3 and self.board[i][j] == self.board[i+1][j]):
                    return True
        return False

    def __has_a_move(self):
        return self.__has_zeros() or self.__has_a_merge()

    def __new(self):
        self.merged = []
        row = -1
        col = -1
        has_zeroes = not self.__has_zeros()
        while not has_zeroes:
            row = random.randint(0, self.size-1)
            col = random.randint(0, self.size-1)
            if self.board[row][col] == 0:
                break
        if not has_zeroes:
            self.board[row][col] = 2
        self.over = not self.__has_a_move()
            
    def __step(self, row1, col1, row2, col2):
        need_new = False
        if self.board[row1][col1] > 0 and self.board[row2][col2] == 0:
            self.board[row2][col2] = self.board[row1][col1]
            self.board[row1][col1] = 0
            need_new = True
        elif self.board[row1][col1] > 0:
            need_new = self.__merge(row2, col2, row1, col1) or need_new
        return need_new

    def __merge(self, row1, col1, row2, col2):
        if self.board[row1][col1] == self.board[row2][col2] \
                and (row1, col1) not in self.merged and (row2, col2) not in self.merged:
            self.board[row1][col1] *= 2
            self.board[row2][col2] = 0
            self.merged.append((row1, col1))
            return True
        return False

    def print_board(self):
        for i in range(self.size):
            print self.board[i]

    def __get_highest_score(self):
        score = 0
        for row in self.board:
            for cell in row:
                if cell > score:
                    score = cell
        return score
            
    def play(self):
        print 'Player Plays'
        self.print_board()
        while not self.over:
            direction = raw_input('Next move: ')
            if direction == 'w':
                self.__up()
                self.print_board()
            elif direction == 's':
                self.__down()
                self.print_board()
            elif direction == 'a':
                self.__left()
                self.print_board()
            elif direction == 'd':
                self.__right()
                self.print_board()
        print 'Game Over,   Score:{}'.format(self.__get_highest_score())
        
    def play_random(self):
        print 'Random Play'
        self.print_board()
        directions = [self.__up, self.__right, self.__left, self.__down]
        while not self.over:
            direction = random.choice(directions)
            direction()
            self.print_board()
        print 'Game Over,   Score:{}'.format(self.__get_highest_score())

    def play_bottom_right(self):
        print 'Bottom right Play'
        self.print_board()
        plan_a = [self.__down, self.__right]
        plan_b = self.__left
        plan_c = self.__up
        while not self.over:
            choices = plan_a[:]
            direction = random.choice(choices)
            res = direction()
            if res:
                self.print_board()
                continue
            else:
                choices.remove(direction)
                direction = choices[0]
                res = direction()
                if res:
                    self.print_board()
                    continue
            if plan_b:
                res = plan_b()
                if res:
                    self.print_board()
                    continue
            if plan_c and res is False:
                plan_c()
                self.print_board()
        print 'Game Over,   Score:{}'.format(self.__get_highest_score())
