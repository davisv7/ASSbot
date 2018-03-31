import ast
from sudoclasses import Population



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


def main():
    board = import_problem()
    given_values = find_values(board)
    pop = Population(1000, 1,1, 0.01, given_values,10)
    print(pop.solution)


main()