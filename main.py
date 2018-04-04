import ast
from popclass import Population
import time

def find_values(board):
    indices = {}
    for i, r in enumerate(board):
        for j, e in enumerate(r):
            if e != ' ':
                indices[(i, j)] = str(e)
    return indices


def import_problem():
    with open('problem.in', 'r') as fileobj:
        lines = fileobj.readlines()
        board = [ast.literal_eval(x) for x in lines]
        return board


def import_solution():
    with open('solution.in', 'r') as fileobj:
        lines = fileobj.readlines()
        board = [ast.literal_eval(x) for x in lines]
        return board


def main():
    start = time.time()
    board = import_problem()
    given_values = find_values(board)
    pop = Population(10, 70000, 2, 0.01, given_values, 0)
    [print(x) for x in pop.solution]
    print(import_solution() == pop.solution)
    end = time.time()
    print('Time taken: {}'.format((end-start)/60))


main()

