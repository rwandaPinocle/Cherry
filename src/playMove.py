import numpy as np
from multiprocessing import Pool
from scipy import signal


inf = 10**10

DEPTH = 9
PROCESS_CT = 12
'''
WIN_CONDS = [[[1],
              [1],
              [1],
              [1]],
             [[1, 1, 1, 1]],
             [[1, 0, 0, 0],
              [0, 1, 0, 0],
              [0, 0, 1, 0],
              [0, 0, 0, 1]],
             [[0, 0, 0, 1],
              [0, 0, 1, 0],
              [0, 1, 0, 0],
              [1, 0, 0, 0]]]
'''
WIN_CONDS = [[[0, 1],
              [1, 0],
              [0, 1],
              [1, 0]],
             [[1, 0],
              [0, 1],
              [1, 0],
              [0, 1]]]
WIN_CONDS = np.array(WIN_CONDS)


class PlayerNode:
    def __init__(self, board):
        self.board = board
        self.player = 1

    def getChildren(self, history):
        children = []
        moves = validMoves(self.board)
        moves = sorted(moves, key=lambda x: -history[x])
        children = []
        for move in moves:
            new_board = placePiece(self.board, move, player=self.player)
            children.append((EnemyNode(new_board), move))
        return children

    def isTerminal(self):
        return isWin(self.board) or isDraw(self.board)

    def isMaximizingPlayer(self):
        return True


class EnemyNode:
    def __init__(self, board):
        self.board = board
        self.player = -1

    def getChildren(self, history):
        children = []
        moves = validMoves(self.board)
        moves = sorted(moves, key=lambda x: -history[x])
        for move in moves:
            new_board = placePiece(self.board, move, player=self.player)
            children.append((PlayerNode(new_board), move))
        return children

    def isTerminal(self):
        return isLoss(self.board) or isDraw(self.board)

    def isMaximizingPlayer(self):
        return False


def alphaBeta(node, depth, alpha, beta, history=None, max_depth=DEPTH):
    if depth == max_depth:
        history = {move: 0 for move in validMoves(node.board)}

    if depth == 0 or node.isTerminal():
        return scoreBoard(node.board, depth)

    if node.isMaximizingPlayer():
        value = -inf
        for child, move in node.getChildren(history):
            value = max(value, alphaBeta(child, depth-1, alpha, beta, history))
            alpha = max(alpha, value)
            if alpha >= beta:
                history[move] += 2**depth
                break
        return value
    else:
        value = inf
        for child, move in node.getChildren(history):
            value = min(value, alphaBeta(child, depth-1, alpha, beta, history))
            beta = min(beta, value)
            if alpha >= beta:
                history[move] += 2**depth
                break
        return value


def scorePlayerBoard(board):
    convs = [signal.convolve2d(board, cond, mode='valid') 
             for cond in WIN_CONDS]
    flat_convs = np.array([i for conv in convs for row in conv for i in row])
    best = np.max(flat_convs)
    threes = np.sum(flat_convs == 3)
    twos = np.sum(flat_convs == 2)
    score = best + threes/10 + twos/100
    score = min(4, score)  # because 4 in a row wins
    return score


def scoreBoard(board, depth):
    player_score = scorePlayerBoard(board)
    score = player_score - depth/1000
    if isWin(board):
        score = 4
    if isLoss(board):
        score = -1
    # enemy_score = scorePlayerBoard(board*-1)
    # return player_score - enemy_score
    return score


def isLoss(board: np.array):
    return isWin(board*-1)


def isWin(board: np.array):
    convs = [signal.convolve2d(board, cond) for cond in WIN_CONDS]
    result = any([i == 4
                  for conv in convs
                  for row in conv
                  for i in row])
    return result


def isDraw(board: np.array):
    no_win = not isWin(board) and not isLoss(board)
    no_moves = board.size == 0
    return no_win and no_moves


def validMoves(board: np.array):
    result = [idx for idx, value in enumerate(board[0]) if value == 0]
    return np.array(result)


def placePiece(board: np.array, colnum: int, player=1):
    lastEmptyRow = np.where(board[:, colnum] == 0)[0][-1]
    new_board = np.copy(board)
    new_board[lastEmptyRow, colnum] = player
    return new_board


def processNode(node):
    score = alphaBeta(node, DEPTH, -inf, inf)
    return score


def playMove(board):
    moves = validMoves(board)

    next_boards = [placePiece(board, move, player=1) for move in moves]
    next_nodes = [EnemyNode(board) for board in next_boards]

    with Pool(PROCESS_CT) as p:
        scores = p.map(processNode, next_nodes)
    # scores = [alphaBeta(node, DEPTH, -inf, inf) for node in next_nodes]
    moves_scores = sorted(zip(moves, scores), key=lambda x: x[1])

    best_move = moves_scores[-1][0]
    return best_move
