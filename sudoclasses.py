import turtle
import random
from itertools import cycle


class Population(object):
    def __init__(self, size, generations, mRate, given_values):
        self.populationsize = size
        self.mRate = mRate
        self.given_values = given_values
        self.population = []
        self.fitnesses = []
        self.top_individuals = []
        self.generation = 0
        self.populate()
        self.get_fitnesses()
        self.get_top_individuals()

        # self.wn = turtle.Screen()
        # self.Droo = turtle.Turtle()
        # self.Droo.speed(0)
        # self.pos = self.Droo.pos()
        for i in range(generations):
            self.repopulate()
            # self.update_screen()
            if self.fitnesses[0][1] == 0:
                self.solution = self.top_individuals[0].board
                break
        else:
            self.solution = self.top_individuals[0]
        # self.wn.exitonclick()

    def populate(self):
        for i in range(self.populationsize):
            self.population.append(Board(self.given_values, mutation=self.mRate))

    def repopulate(self):
        self.population = []
        for i in range(self.populationsize):
            self.crossover()
        self.top_individuals = []
        self.get_fitnesses()
        self.get_top_individuals()
        # self.print()

    def crossover(self):
        # roworcol = random.randint(0, 2)
        board = self.top_individuals[0].board
        for j in range(1):
            roworcol = random.randint(0, 2)

            index = random.randint(0, 8)
            # roworcol=0
            if roworcol == 0:
                board = board[:index] + self.top_individuals[1].get_row(index) + board[index + 1:]
            else:
                col = self.top_individuals[1].get_col(index)
                for i in range(9):
                    # print(i,index)
                    board[i][index] = col[i]
            # print(board)
        self.population.append(Board(self.given_values, board, self.mRate))

    def get_fitnesses(self):
        self.fitnesses = [(index, x.get_fitness()) for (index, x) in enumerate(self.population)]
        # print(self.fitnesses)

    def get_top_individuals(self):
        # self.fitnesses.sort(key=lambda r: r[1])
        # self.top_individuals = [self.population[self.fitnesses[i][0]] for i in range(2)]
        normalizer = sum(element[1] for element in self.fitnesses)
        while len(self.top_individuals) < 2:
            rando = random.choice(self.fitnesses)
            if random.uniform(0, 1) > rando[1] / normalizer:
                if self.population[rando[0]] not in self.top_individuals:
                    self.top_individuals.append(self.population[rando[0]])

        print(self.fitnesses[0][1])
        # print(self.top_individuals)

    def update_screen(self):
        self.wn.clear()
        pcycle = cycle([(self.pos[0] + i * 15, self.pos[0] - j * 15) for j in range(0, 9) for i in range(0, 9)])
        x, y = self.pos
        self.Droo.penup()
        self.Droo.goto(next(pcycle))
        for row in self.top_individuals[0].board:
            for cell in row:
                self.Droo.write(cell)
                self.Droo.goto(next(pcycle))
        self.Droo.goto(-150, 0)
        self.Droo.write(self.fitnesses[0][1])


class Board(object):
    def __init__(self, given_values, board=None, mutation=.1):
        self.board = board
        self.mRate = mutation
        self.given_values = given_values
        if self.board == None:
            self.generate()
            self.fill()
        else:
            self.mutate()
            self.fill()
        # print(self.board)

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
                    choice = random.randint(1, 9)
                    self.board[i][j] = choice
        # print(self.board)

    def mutate(self):
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                if (i, j) in self.given_values:
                    continue
                else:
                    if random.uniform(0, 1) < self.mRate:
                        self.board[i][j] = ' '
                        # self.board[i][j] = random.randint(1,9)

    def get_fitness(self):
        score = 0
        for row in self.romanizer():
            score += 9 - len(set(row))
        for col in self.columizer():
            score += 9 - len(set(col))
        return score / 144

    def romanizer(self):
        return [x for x in self.board]

    def columizer(self):
        return [[self.board[j][i] for j in range(len(self.board[i]))] for i in range(len(self.board))]

    def get_row(self, index):
        return [self.board[index]]

    def get_col(self, index):
        return [self.board[i][index] for i in range(9)]

    def __repr__(self):
        return str(self.board)
