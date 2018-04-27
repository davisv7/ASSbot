###############################################################################################################
# Credit: Vinny (Le God Programmer) and sidekick Scotty.
# Import The following Libraries
import turtle
import random
from itertools import cycle
import copy
from indclass import Board
###############################################################################################################
class Population(object):
    """
    [This Section Does What?]
    """
    def __init__(self, size, generations, poolsize, mRate, given_values,solution, interval,switch,rococ):
        self.rococ=rococ
        self.switch = switch
        self.solution=solution
        self.populationsize = size
        self.mRate = mRate
        self.poolsize = poolsize
        self.given_values = given_values
        self.generations = generations
        self.population = []
        self.fitnesses = []
        self.top_individuals = []
        self.generation = 0
        self.populate()
        self.get_top_individuals()
        # self.get_roullette()
        self.top_fitness = self.top_individuals[0].get_fitness()
        # print(self.top_individuals[0].get_fitness())
        self.create_screen()
        self.og = mRate
        self.sw=switch
        self.mult = .005
        self.max = self.og+.03
        self.update_screen()
        self.regenerate(interval)
        # self.create_screen()
        self.update_screen()
        self.wn.exitonclick()
###############################################################################################################
    def regenerate(self, interval):  # TODO instead of retaining the overall max, just retain the max of the generation
        """
        Function Use: [Explain Me!]
        """
        for i in range(self.generations):
            self.repopulate()
            self.mutate_all()
            self.get_top_individuals()
            # self.get_roullette()

            # print when the fitness changes
            # if interval == 0:
                # if self.top_fitness != self.top_individuals[0].get_fitness():
                    # print(i, self.top_fitness, self.mRate)
                    # self.top_fitness = self.top_individuals[0].get_fitness()
                    # self.update_screen()
                    # pass
            # elif i % interval == 0:
                # print at an interval
                # print(i, self.top_individuals[0].get_fitness(), self.mRate)

            # update fitness, reset mult
            if self.top_fitness >= self.top_individuals[0].get_fitness():
                if self.top_fitness >self.top_individuals[0].get_fitness():
                    print(i, self.top_fitness, self.mRate)
                    if i>500:
                        self.update_screen()
                    self.top_fitness = self.top_individuals[0].get_fitness()
                    self.mRate = self.og
                    self.switch = self.sw
                else:
                    self.mRate = round(min(self.mRate + self.mult, self.max), 7)
                    self.switch = round(min(self.switch - 1, 0), 7)
                    # reset mult
                    if self.mRate == self.max: self.mRate = self.og
                    if self.switch == 0: self.switch = self.sw

            # elif self.top_individuals[0].get_fitness() == self.top_fitness:
                # increment mult towards max
                # self.mRate = self.mRate + self.mult

            if self.top_individuals[0].get_fitness() == 0:
                # solution reached
                self.solution = self.top_individuals[0].board
                break
        else:  # end of generations
            self.solution = self.top_individuals[0].board
###############################################################################################################
    def populate(self):
        """
        Function Use: [Explain Me!]
        """
        for i in range(self.populationsize):
            self.population.append(Board(self.given_values, mutation=self.mRate))
###############################################################################################################
    def repopulate(self):
        """
        Function Use: [Explain Me!]
        """
        self.population = self.population[:1]
        for i in range(1, self.populationsize):
            self.crossover()
###############################################################################################################
    def crossover(self):
        """
        Function Use: [Explain Me!]
        """
        if self.poolsize == 1:
            board = copy.deepcopy(self.top_individuals[0])
            self.population.append(board)
            return

        choices = [0, random.randint(0, self.poolsize - 1)]
        # choices = random.sample(range(0, self.poolsize),2)
        board = copy.deepcopy(self.top_individuals[choices[0]])
        indexlist = random.sample(range(8),self.switch)
        for index in indexlist:
            index = random.randint(0, 8)
            if self.rococ==0: #cell
                poslist=[]
                while len(poslist)<self.switch:
                    x=list(range(9))
                    y=list(range(9))
                    random.shuffle(x)
                    random.shuffle(y)
                    poslist.extend(list(zip(x,y))[:self.switch-len(poslist)])
                    poslist=list(set(poslist)-set(self.given_values))
                for i in range(self.switch):
                    a,b=poslist[i][0],poslist[i][1]
                    c,d=poslist[i-1][0],poslist[i-1][1]
                    board.set_cell(a,b,self.top_individuals[choices[1]].get_cell(c,d))
            elif self.rococ in [1,3,7]:
                for i in range(9): #row
                    board.set_cell(index,i,self.top_individuals[choices[1]].get_cell(index,i))
            elif self.rococ in [2,3,7]:
                col = self.top_individuals[choices[1]].get_col(index)
                for i in range(len(col)): #col
                    board.set_cell(i,index,col[i])
            elif self.rococ in [4,7]:
                block = self.top_individuals[choices[1]].get_block((index+1)%3,index%3)
                board.set_block((index+1)%3,index%3, block)

        self.population.append(board)

###############################################################################################################
    def mutate_all(self):
        """
        Function Use: [Explain Me!]
        """
        for i in range(len(self.population)):
            self.population[i].mutate()
###############################################################################################################
    def get_fitnesses(self):
        """
        Function Use: [Explain Me!]
        """
        self.fitnesses = [(index, x.get_fitness()) for (index, x) in enumerate(self.population)]
###############################################################################################################
    def get_roullette(self):
        """
        Function Use: [Explain Me!]
        """
        self.get_fitnesses()
        normalizer = sum(element[1] for element in self.fitnesses)
        while len(self.top_individuals) < self.poolsize:
            rando = random.choice(self.fitnesses)
            if random.uniform(0, 1) > rando[1] / normalizer:
                if self.population[rando[0]] not in self.top_individuals:
                    self.top_individuals.append(self.population[rando[0]])
###############################################################################################################
    def get_top_individuals(self):
        """
        Function Use: [Explain Me!]
        """
        self.get_fitnesses()
        self.fitnesses.sort(key=lambda r: r[1])
        self.top_individuals = [self.population[self.fitnesses[i][0]] for i in range(self.poolsize)]
###############################################################################################################
    def create_screen(self):
        """
        Function Use: [Explain Me!]
        """
        self.wn = turtle.Screen()
        self.Droo = turtle.Turtle()
        self.Droo.speed(0)
        self.pos = self.Droo.pos()
###############################################################################################################
    def update_screen(self):
        """
        Function Use: [Explain Me!]
        """
        self.wn.clear()
        pcycle = cycle([(self.pos[0] + i * 20, self.pos[0] - j * 20) for j in range(0, 9) for i in range(0, 9)])
        x, y = self.pos
        self.Droo.penup()
        self.Droo.goto(next(pcycle))
        for i,row in enumerate(self.top_individuals[0].board):
            for j,cell in enumerate(row):
                if cell == self.solution[i][j]:
                    self.Droo.write(cell, font=('Arial', 16, 'normal'))
                # self.Droo.write(self.solution[i][j], font=('Arial', 16, 'normal'))
                self.Droo.goto(next(pcycle))
        self.Droo.goto(-160, 30)
        self.Droo.write('{}% Solved'.format(round(100 - self.top_fitness * 100, 2)), font=('Arial', 16, 'normal'))
###############################################################################################################
