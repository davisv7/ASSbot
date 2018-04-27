###############################################################################################################
# Credit: Vinny (Le God Programmer) and sidekick Scotty.
# Import The following Libraries
import random

###############################################################################################################
"""
This section just initializes the class for the board we plan to do the sudoku problems on, the mutation rate,
and the given values.
"""


class Board(object):
    def __init__(self, given_values, board=None, mutation=.1):
        self.board = board
        self.mRate = mutation
        self.given_values = given_values
        if self.board == None:
            self.generate()
            self.fill()
        # else:
        #     self.mutate()
        #     self.fill()

    ###############################################################################################################
    def generate(self):
        """
        Function Use: Generates the board in which the sudoku will be using to see an example of how this will
        look check out the easyproblem.in or easysolution.in
        """
        self.board = [[' ' for i in range(9)] for j in range(9)]
        for key in self.given_values:
            self.board[key[0]][key[1]] = self.given_values[key]

    ###############################################################################################################
    def fill(self):
        """
        Function Use: Now that the board has been generated from the above funtion we now have to fill it in so
        we will fill in all the given values for the rows, columns, and blocks.
        """
        # limit = {str(x):9 for x in range(1,10)}
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                if (i, j) in self.given_values:
                    # limit[self.board[i][j]]-=1
                    continue
                elif self.board[i][j] == ' ':
                    choice = str(random.randint(1, 9))
                    # choice = random.choice([x for x in limit])
                    self.board[i][j] = choice
                    # limit[self.board[i][j]]-=1
                    continue

    ###############################################################################################################
    def mutate(self):
        """
        Function Use: .
        """
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                if (i, j) in self.given_values:
                    continue
                else:
                    if random.uniform(0, 1) <= self.mRate:
                        self.board[i][j] = str(random.randint(1, 9))
                        # self.board[i][j] = ' '

    ###############################################################################################################
    def get_fitness(self):
        """
        Function Use: This function checks the length of each row,column, and block turned into sets.
        for example 1,2,3,4,5,6,7,8,9 would be a len of 9 while 1,2,3,4,5,6,7,7,7 would be a length of 7
        we then take this "score" and divide it by 216 (which is then
        worst possible fitness) and we round it to the 6th digit.
        """
        score = 0
        for row in self.romanizer():
            score += (9 - len(set(row)))
        for col in self.columizer():
            score += (9 - len(set(col)))
        for block in self.blocker():
            score += (9 - len(set(block)))

        counts = [[x.count(str(i)) for i in range(1, 10)] for x in self.romanizer()]
        rowavg=[sum(x) / 9 for x in counts]
        countavg = sum(rowavg) / 9
        score /= (216 - len(self.given_values))
        weight =1+(max(rowavg)-min([min(x) for x in counts]))/(countavg)
        # print(weight)
        score *= weight

        return round(score, 6)

    ###############################################################################################################
    def romanizer(self):
        """
        Function Use: .
        """
        return [x for x in self.board]

    ###############################################################################################################
    def columizer(self):
        """
        Function Use: .
        """
        return [[self.board[j][i] for j in range(len(self.board[i]))] for i in range(len(self.board))]

    ###############################################################################################################
    def blocker(self):  # TODO Fix this!
        """
        Function Use: .
        """
        blocklist = []
        for i in range(3):
            chunk = self.board[i * 3:i * 3 + 3]
            for j in range(3):
                block = []
                for k in range(3):
                    block += chunk[k][j * 3:j * 3 + 3]
                blocklist.append(block)
        return blocklist

    ###############################################################################################################
    def get_block(self, x, y):
        blocklist = []
        chunk = self.board[x * 3:x * 3 + 3]
        block = []
        for k in range(3):
            block += chunk[k][y * 3:y * 3 + 3]
        blocklist.append(block)
        flatlist = [x for y in blocklist for x in y]
        return flatlist

    ##############################################################################################################
    def set_block(self, x, y, chunk):
        for k in range(3):
            for i,element in enumerate(chunk[k * 3:k * 3 + 3]):
                self.board[k][i * 3]=element

    ###############################################################################################################
    def get_row(self, index):
        """
        Function Use: .
        """
        return [self.board[index]]

    ###############################################################################################################
    def get_col(self, index):
        """
        Function Use: .
        """
        return [self.board[i][index] for i in range(9)]

    def get_cell(self, r, c):
        return self.board[r][c]

    def set_cell(self, r, c, cell):
        # print(len(self.board),len(self.board[r]),r,c)
        self.board[r][c] = cell

    ###############################################################################################################
    def __repr__(self):
        """
        Function Use: .
        """
        return str(self.board)
###############################################################################################################
