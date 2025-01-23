"""
Tic Tac Toe Player
"""
from copy import deepcopy
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
    flattened_board = [cell for row in board for cell in row]

    x_count = flattened_board.count(X)
    o_count = flattened_board.count(O)

    if x_count > o_count:
        return O
    else:
        return X    


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions_available = set()
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == EMPTY:
                actions_available.add((i,j))
    return actions_available



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise ValueError("Invalid action")
    
    new_board = deepcopy(board)
    i,j = action
    new_board[i][j] = player(board)
    #print(new_board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #Check rows for winner
    
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != EMPTY:
            return row[0]
    
    #Check columns for winner
    for col in range(3):    
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != EMPTY:
            return board[0][col]
    
    #Check both diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return board[0][0]
    if  board[2][0] ==  board[1][1] ==  board[0][2] and board[2][0] != EMPTY:
        return board[2][0]
    
    return None
    


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    moves = actions(board)
    if winner(board) is not None or len(moves) == 0:
        return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    return 1 if winner(board) == X else -1 if winner(board) == O else 0

    


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    current_player = player(board)
    acceptable_actions = actions(board)
    Best_action = (-1,-1)
    if terminal(board):
        return None
    Beta = float('inf') #Determine initial Beta
    Alpha = float('-inf') #Determine intial Alpha
    if current_player == X:
        Best_value = float('-inf')
        
        for move in acceptable_actions:
            new_board = result(board,move)
            value = minimax_value(new_board,Alpha,Beta)#Use helper function to get value            

            if value > Best_value:
                Best_value = value #Modify best value to value
                Best_action = move #Save best action
        return Best_action
    else:
        Best_value = float('inf') 
        
        for move in acceptable_actions:
            new_board = result(board,move)
            value = minimax_value(new_board,Alpha,Beta) #Use helper function to get value           
            
            if value < Best_value:
                Best_value = value #Save best value as value
                Best_action = move #Save best action as the action that got lower value than best value
        return Best_action




def minimax_value(board,alpha,beta):
    """
    Helper function to calculate the value for minimax
    
    returns value v
    """
    Player = player(board)
    if terminal(board):
        return utility(board)
    if Player == X:
        value = max_value(board,alpha,beta)
        return value
    else:
        value = min_value(board,alpha,beta)
        return value
    
def min_value(board,alpha,beta):
    """Helper function to determine the min value for minimax"""
    
    best = float('inf')
    #For each move calculate the min value
    available = actions(board)
    for move in available:
        value = minimax_value(result(board,move),alpha,beta)
        best = min(best,value)
        if best <= alpha: #Check if best is better than alpha
            return best #escape loop early
        beta = min(beta,value)
    return best

def max_value(board,alpha,beta):
    """Helper function to determine the max value for minimax"""
    best = float('-inf')
    available = actions(board)
    #For each move calculate the max value
    for move in available:
        value = minimax_value(result(board,move),alpha,beta)
        best = max(best,value)
        if best >= beta: #Check if best is better than beta
            return best #escape loop early
        alpha = max(alpha,value)
        
    return best