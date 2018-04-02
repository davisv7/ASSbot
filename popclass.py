import turtle
import random
from itertools import cycle
import copy
from indclass import Board


class Population(object):
    def __init__(self, size, generations, poolsize, mRate, given_values, interval):
        self.populationsize = size
        self.mRate = mRate
        self.poolsize = poolsize
        self.given_values = given_values
        self.generations=generations
        self.population = []
        self.fitnesses = []
        self.top_individuals = []
        self.generation = 0
        self.populate()
        self.get_top_individuals()
        self.top = copy.deepcopy(self.top_individuals[0])
        print(self.top_individuals[0].get_fitness())
        # self.create_screen()
        self.mult=.005
        self.og=mRate
        self.regenerate(interval)
        self.create_screen()
        self.update_screen()
        self.wn.exitonclick()

    def regenerate(self,interval):
        for i in range(self.generations):
            self.repopulate()
            self.mutate_all()
            self.population[0] = self.top
            self.get_top_individuals()
            if self.top.get_fitness()>self.top_individuals[0].get_fitness():
                self.top = copy.copy(self.top_individuals[0])
                self.mRate=self.og
                # print(i, self.top.get_fitness())
                # self.update_screen()
                # continue
            if self.top_individuals[0].get_fitness() == self.top.get_fitness():
                self.mRate+=self.mult
            if self.top.get_fitness() == 0:
                self.solution = self.top.board
                break
            if i %interval ==0:
                print(i, self.top.get_fitness(),self.mRate)
                # self.update_screen()
        else:
            self.solution = self.top_individuals[0]

    def populate(self):
        for i in range(self.populationsize):
            self.population.append(Board(self.given_values, mutation=self.mRate))

    def repopulate(self):
        for i in range(1, self.populationsize):
            self.crossover(i)

    def crossover(self, ind):
        choice = random.randint(0, self.poolsize-1)
        board = copy.deepcopy(self.top.board)
        for j in range(1):
            roworcol = random.randint(0, 1)
            index = random.randint(0, 8)
            if roworcol == 0:
                board = board[:index] + self.top_individuals[choice].get_row(index) + board[index + 1:]
            else:
                col = self.top_individuals[choice].get_col(index)
                for i in range(9):
                    board[i][index] = col[i]
        self.population[ind] = Board(self.given_values, board, self.mRate)

    def mutate_all(self):
        for i in range(1, len(self.population)):
            self.population[i].mutate()

    def get_fitnesses(self):
        self.fitnesses = [(index, x.get_fitness()) for (index, x) in enumerate(self.population)]

    def get_roullette(self):
        normalizer = sum(element[1] for element in self.fitnesses)
        while len(self.top_individuals) < 2:
            rando = random.choice(self.fitnesses)
            if random.uniform(0, 1) > rando[1] / normalizer:
                if self.population[rando[0]] not in self.top_individuals:
                    self.top_individuals.append(self.population[rando[0]])

    def get_top_individuals(self):
        self.get_fitnesses()
        self.fitnesses.sort(key=lambda r: r[1])
        self.top_individuals = [self.population[self.fitnesses[i][0]] for i in range(self.poolsize)]

    def create_screen(self):
        self.wn = turtle.Screen()
        self.Droo = turtle.Turtle()
        self.Droo.speed(0)
        self.pos = self.Droo.pos()

    def update_screen(self):
        self.wn.clear()
        pcycle = cycle([(self.pos[0] + i * 20, self.pos[0] - j * 20) for j in range(0, 9) for i in range(0, 9)])
        x, y = self.pos
        self.Droo.penup()
        self.Droo.goto(next(pcycle))
        for row in self.top_individuals[0].board:
            for cell in row:
                self.Droo.write(cell, font=('Arial', 16, 'normal'))
                self.Droo.goto(next(pcycle))
        self.Droo.goto(-150, 20)
        self.Droo.write(self.top.get_fitness(), font=('Arial', 16, 'normal'))
