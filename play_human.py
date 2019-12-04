import numpy as np
from polican.playMove import playMove, placePiece, isWin, isLoss, isDraw

def prRed(skk): return "\033[91m {}\033[00m".format(skk)
def prGreen(skk): return "\033[92m {}\033[00m".format(skk)
def prYellow(skk): return "\033[93m {}\033[00m".format(skk)
def prLightPurple(skk): return "\033[94m {}\033[00m".format(skk)
def prPurple(skk): return "\033[95m {}\033[00m".format(skk)
def prCyan(skk): return "\033[96m {}\033[00m".format(skk)
def prLightGray(skk): return "\033[97m {}\033[00m".format(skk)


boardsize = (6, 8)


icons = {1: prRed('O'), 0: prLightGray('O'), -1: prPurple('O')}


def display(board):
    print(' ' + '  '.join([str(i) for i in range(len(board[0]))]))
    print('\n'.join([' '.join( [icons[item] for item in row] ) 
                     for row in board]))


if __name__ == '__main__':
    board = np.zeros(boardsize)
    while not isWin(board) and not isLoss(board) and not isDraw(board):
        display(board)
        move = int(input('Make a move: '))
        board = placePiece(board, move, player=-1)
        display(board)

        if isWin(board) or isLoss(board) or isDraw(board):
            break

        comp_move = playMove(board)
        board = placePiece(board, comp_move, player=1)

    if isWin(board):
        print('Human loses')
    if isLoss(board):
        print('Human wins')
    if isDraw(board):
        print('Draw')
