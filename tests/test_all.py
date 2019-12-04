from ..polican.playMove import (playMove, 
                                isWin, 
                                validMoves, 
                                placePiece, 
                                alphaBeta,
                                PlayerNode,
                                EnemyNode)
import numpy as np


def test_isWin():
    a = [[1, 0, 0, 0],
         [1, 0, 0, 0],
         [1, 0, 0, 0],
         [1, 0, 0, 0]]
    a = np.array(a)
    assert(isWin(a))

    a = [[1, 1, 1, 1],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]]
    a = np.array(a)
    assert(isWin(a))

    a = [[0, 0, 0, 0],
         [1, 1, 1, 1],
         [0, 0, 0, 0],
         [0, 0, 0, 0]]
    a = np.array(a)
    assert(isWin(a))

    a = [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [1, 1, 1, 1],
         [0, 0, 0, 0]]
    a = np.array(a)
    assert(isWin(a))

    a = [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [1, 1, 1, 1]]
    a = np.array(a)
    assert(isWin(a))

    a = [[1, 0, 0, 0],
         [0, 1, 0, 0],
         [0, 0, 1, 0],
         [0, 0, 0, 1]]
    a = np.array(a)
    assert(isWin(a))

    a = [[0, 0, 0, 1],
         [0, 0, 1, 0],
         [0, 1, 0, 0],
         [1, 0, 0, 0]]
    a = np.array(a)
    assert(isWin(a))

    a = [[0, 0, 0, 0],
         [0, 0, 1, 0],
         [0, 1, 0, 0],
         [1, 0, 0, 0]]
    assert(not isWin(a))

    a = [[0, 0, 0, 0],
         [0, 1, 1, 1],
         [0, 1, 0, 1],
         [1, 0, 0, 1]]
    assert(not isWin(a))

    a = [[0, 0, 0, -1],
         [0, 0, -1, 0],
         [0, -1, 0, 0],
         [-1, 0, 0, 0]]
    assert(not isWin(a))

    a = [[1, 1, 0, 1],
         [1, 0, 1, 0],
         [1, 1, 0, 1],
         [0, 1, 1, 1]]
    assert(not isWin(a))


def test_validMoves():
    board = [[0, 0, 0, 0], [1, 1, 1, 1]]
    assert(np.array_equal(validMoves(board), [0, 1, 2, 3]))

    board = [[1, 0, 0, 0], [1, 1, 1, 1]]
    assert(np.array_equal(validMoves(board), [1, 2, 3]))

    board = [[1, 0, 1, 0], [1, 1, 1, 1]]
    assert(np.array_equal(validMoves(board), [1, 3]))

    board = [[1, 1, 1, 1], [1, 1, 1, 1]]
    assert(np.array_equal(validMoves(board), []))


def test_placePiece():
    x_board = [[0, 0, 0, 0], 
               [0, 0, 0, 0], 
               [0, 0, 0, 0], 
               [0, 0, 0, 0]]

    y_board = [[0, 0, 0, 0], 
               [0, 0, 0, 0], 
               [0, 0, 0, 0], 
               [1, 0, 0, 0]]
    x_board = np.array(x_board)
    y_board = np.array(y_board)
    assert(np.array_equal(placePiece(x_board, 0), y_board))

    x_board = [[0,0,0,0],
               [1,0,0,0],
               [1,0,0,0],
               [1,0,0,0]]

    y_board = [[1,0,0,0],
               [1,0,0,0],
               [1,0,0,0],
               [1,0,0,0]]
    x_board = np.array(x_board)
    y_board = np.array(y_board)
    assert(np.array_equal(placePiece(x_board, 0), y_board))

    x_board = [[0,0,0,0],
               [0,0,0,0],
               [0,0,0,0],
               [1,1,1,1]]

    y_board = [[0,0,0,0],
               [0,0,0,0],
               [0,1,0,0],
               [1,1,1,1]]
    x_board = np.array(x_board)
    y_board = np.array(y_board)
    assert(np.array_equal(placePiece(x_board, 1), y_board))

    x_board = [[0,0,0,0],
               [0,0,0,0],
               [0,0,0,0],
               [-1,-1,-1,-1]]

    y_board = [[0,0,0,0],
               [0,0,0,0],
               [0,0,1,0],
               [-1,-1,-1,-1]]
    x_board = np.array(x_board)
    y_board = np.array(y_board)
    assert(np.array_equal(placePiece(x_board, 2), y_board))


def test_alphaBeta():
    board = [[0,0,0,0],
             [1,0,0,0],
             [1,0,0,0],
             [1,0,0,0]]
    board = np.array(board)
    node = PlayerNode(board)
    assert(alphaBeta(node, 3, -10**10, 10**10, max_depth=3) == 4)

    board = [[0,0,0,0],
             [-1,0,0,0],
             [-1,0,0,0],
             [-1,0,0,0]]
    board = np.array(board)
    node = EnemyNode(board)
    assert(alphaBeta(node, 3, -10**10, 10**10, max_depth=3) == -1)

    board = [[0,0,0,0],
             [1,1,0,0],
             [1,1,0,0],
             [1,1,0,0]]
    board = np.array(board)
    node = EnemyNode(board)
    assert(alphaBeta(node, 3, -10**10, 10**10, max_depth=3) == 4)

    board = [[0,0,0,0],
             [-1,-1,0,0],
             [-1,-1,0,0],
             [-1,-1,0,0]]
    board = np.array(board)
    node = PlayerNode(board)
    assert(alphaBeta(node, 3, -10**10, 10**10, max_depth=3) == -1)
