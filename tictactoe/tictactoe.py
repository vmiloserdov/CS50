"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count_X = 0
    count_O = 0

    for row in board:
        for cell in row:
            if cell == EMPTY:
                continue
            elif cell == X:
                count_X += 1
            else:
                count_O += 1

    if count_X > count_O:
        return O
    return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    res = set()

    for i in range(3):
        for j in range(3):
            if (board[i][j] == EMPTY):
                res.add((i,j))

    return res

def in_bounds(i, j):
    return (i >= 0 and i <= 2 and j >= 0 and j <= 2)

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action

    if (not in_bounds(i, j)):
        raise Exception("Out of bounds!")
    if (board[i][j] != EMPTY):
        raise Exception("Square is taken!")

    res_board = copy.deepcopy(board)
    curr_move = player(board)
    
    res_board[i][j] = curr_move

    return res_board


print(result(initial_state(), (0,0)))


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
