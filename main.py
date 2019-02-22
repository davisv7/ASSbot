###############################################################################################################
# Credit: Vinny (Le God Programmer) and sidekick Scotty.
# Import The following Libraries
import ast
import time

from popclass import Population


class Simulation:
    def __init__(self):
        self.population = Population(10, 50000, 5, 0.01,0)





###############################################################################################################
def main():
    """
    Function Use: [Explain Me!]
    """
    start = time.time()
    Simulation()
    # possibles(board)
    # [print(x) for x in pop.solution]
    # print(import_solution() == pop.solution)
    end = time.time()
    print('Time taken: {}'.format((end - start) / 60))


def possibles(board):
    # for it in range(64):
    for i, row in enumerate(board):
        # print(row)
        for j, col in enumerate(row):
            possibilities = list(map(str, range(1, 10)))
            if col == " ":
                # print(row)
                [possibilities.remove(x) for x in board.get_row(i) if x in possibilities]
                [possibilities.remove(x) for x in board.get_col(j) if x in possibilities]
                [print(x) for x in board.blocker()]
                # print(possibilities)
                if len(possibilities) == 1:
                    print(possibilities)
                    board.board[i][j] = possibilities[0]
    [print(x) for x in board]
    # print(board)


###############################################################################################################
main()
###############################################################################################################
