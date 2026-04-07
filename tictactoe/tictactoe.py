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


def who_won(board):

    res = None

    # First row or first column
    if (board[0][0] == board[0][1] and board[0][1] == board[0][2] or
        board[0][0] == board[1][0] and  board[1][0] == board[2][0]):

        if (board[0][0] == O or board[0][0] == X):
            return board[0][0]

    # Last row and last column
    if (board[0][2] == board[1][2] and  board[1][2] == board[2][2] or
        board[2][0] == board[2][1] and  board[2][1] == board[2][2]):

        if (board[2][2] == O or board[2][2] == X):
            return board[2][2]

    # Diagonals and middle row and column
    if (board[0][0] == board[1][1] and board[1][1] == board[2][2] or 
        board[0][2] == board[1][1] and board[1][1] == board[2][0] or

        board[0][1] == board[1][1] and board[1][1] == board[2][1] or 
        board[1][0] == board[1][1] and board[1][1] == board[1][2]):


        if (board[1][1] == O or board[1][1] == X):
            return board[1][1]
    
    return EMPTY


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    res = who_won(board)
    return None if res == EMPTY else res

def is_full(board):
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False
    return True


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) != None or is_full(board)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if (win != None):
        return 1 if win == X else -1
    
    return 0

def min_value(state):
    if (terminal(state)):
        return utility(state)
    
    value = float('inf')
    for action in actions(state):
        value = min(value, max_value(result(state, action)))
    return value

def max_value(state):
    if (terminal(state)):
        return utility(state)
    
    value = float('-inf')
    for action in actions(state):
        value = max(value, min_value(result(state, action)))
    return value

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    player_to_move = player(board)
    if (player_to_move == X):
        best_util = -1
        best_action = None
        for action in actions(board):
            curr_util = min_value(result(board, action))
            if curr_util > best_util:
                best_action = action
                best_util = curr_util

        return best_action
    

    else:
        best_util = 1
        best_action = None
        for action in actions(board):
            curr_util = max_value(result(board, action))
            if curr_util < best_util:
                best_action = action
                best_util = curr_util

        return best_action
