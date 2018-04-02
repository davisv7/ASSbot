import random


class Board(object):
    def __init__(self, given_values, board=None, mutation=.1):
        self.board = board
        self.mRate = mutation
        self.given_values = given_values
        if self.board == None:
            self.generate()
            self.fill()

    def generate(self):
        self.board = [[' ' for i in range(9)] for j in range(9)]
        for key in self.given_values:
            self.board[key[0]][key[1]] = self.given_values[key]

    def fill(self):
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                if (i, j) in self.given_values:
                    continue
                elif self.board[i][j] == ' ':
                    choice = str(random.randint(1, 9))
                    self.board[i][j] = choice
                    continue

    def mutate(self):
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                if (i, j) in self.given_values:
                    continue
                else:
                    if random.uniform(0, 1) <= self.mRate:
                        self.board[i][j] = str(random.randint(1, 9))

    def get_fitness(self):
        score = 0
        for row in self.romanizer():
            score += (9 - len(set(row)))
        for col in self.columizer():
            score += (9 - len(set(col)))
        for block in self.blocker():
            score += (9 - len(set(block)))
        return round(score/216,6)

    def romanizer(self):
        return [x for x in self.board]

    def columizer(self):
        return [[self.board[j][i] for j in range(len(self.board[i]))] for i in range(len(self.board))]

    def blocker(self):
        blist = []
        for i in range(9, 3):
            for j in range(9, 3):
                chunk = self.board[i:i + 3]
                block = [x[j:j + 3] for x in chunk]
                flat_block = [item for sublist in block for item in sublist]
                blist.append(flat_block)
        return blist

    def get_row(self, index):
        return [self.board[index]]

    def get_col(self, index):
        return [self.board[i][index] for i in range(9)]

    def __repr__(self):
        return str(self.board)
