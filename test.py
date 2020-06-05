import os
import sys
import argparse
import numpy as np
import random
import re
import string
import operator

heuristic = {'quintet': [20000000, ['xxxxx']],
'quartet2open': [400000, ['oxxxxo']],
'quartet1open': [50000, ['nxxxxo', 'oxxxxn']],
'triplet2open': [30000, ['oxxxo']],
'triplet1open': [15000, ['nxxxoo', 'ooxxxn']],
'voidQuartet2open': [7000, ['oxoxxo', 'oxxoxo']],
'voidQuartet1open': [3000, ['nxoxxo', 'nxxoxo', 'oxxoxn', 'oxoxxn']],
'double2open': [500, ['ooxxo', 'oxxoo']],
'double1open': [400, ['nxxooo', 'oooxxn']],
'voidTriplet2opens': [100, ['oxoxo']],
'voidTriplet1open': [40, ['nxoxoo', 'ooxoxn']]}

def boardToStrings(board, player):
    rowStrList = []
    colStrList = []
    diagStrList = []
    # row
    for row in board:
        rowStr = ''
        # print(row)
        for item in row:
            # print(item)
            if item == 0:
                rowStr += 'o'
            elif item == player:
                rowStr += 'x'
            else:
                rowStr += 'n'
        rowStrList.append(rowStr)
    # col
    colBoard = board.copy().transpose()
    for col in colBoard:
        colStr = ''
        for item in col:
            if item == 0:
                colStr += 'o'
            elif item == player:
                colStr += 'x'
            else:
                colStr += 'n'
        colStrList.append(colStr)
    # diagonal
    diagBoard1 = [board.diagonal(i) for i in range(board.shape[1]-5, -board.shape[1]+4, -1)]
    diagBoard2 = [board[::-1, :].diagonal(i) for i in range(board.shape[1]-5, -board.shape[1]+4, -1)]
    for diag in diagBoard1:
        diagStr = ''
        for item in diag:
            if item == 0:
                diagStr += 'o'
            elif item == player:
                diagStr += 'x'
            else:
                diagStr += 'n'
        diagStrList.append(diagStr)
    for diag in diagBoard2:
        diagStr = ''
        for item in diag:
            if item == 0:
                diagStr += 'o'
            elif item == player:
                diagStr += 'x'
            else:
                diagStr += 'n'
        diagStrList.append(diagStr)

    print('ROWS:')
    print(rowStrList)
    print('COLUMNS:')
    print(colStrList)
    print('DIAGONALS:')
    print(diagStrList)
    strList = rowStrList + colStrList + diagStrList
    print('list of strings:  ')
    print(strList)
    return strList

def searchBoardSeq(board, player, sequence):
    boardLists = boardToStrings(board, player)
    occurances = 0
    for string in boardLists:
        occurances += len(re.findall(sequence, string))
    return occurances

def getScore(board, computerColor, playerColor):
    scoreComputer = 0
    scorePlayer = 0
    for item in heuristic.keys():
        weight = heuristic[item][0]
        countComputer = 0
        countPlayer = 0
        sequences = heuristic[item][1]
        for sequence in sequences:
            countComputer += searchBoardSeq(board, computerColor, sequence)
            countPlayer += searchBoardSeq(board, playerColor, sequence)
            print('sequence:  ')
            print(sequence)
            print('count computer:  ')
            print(countComputer)
            print('count player:  ')
            print(countPlayer)
        scoreComputer += countComputer * weight
        scorePlayer += countPlayer * weight
    print('score computer:  ')
    print(scoreComputer)
    print('score player:  ')
    print(scorePlayer)
    score = scoreComputer - scorePlayer
    # score = random.uniform(1,10)
    return score



computer = 8
player = 5
board = np.zeros((6,6), dtype=int)

board[2][2] = computer
board[1][1] = computer
board[3][3] = player

print(getScore(board,computer,player))












# some_scores = [0,1,2,3,4]
# score = random.choice(some_scores)
# heuristic = {'quintet': [20000000, ['xxxxx']],
# 'quartet2opens': [400000, ['exxxxe']],
# 'quartet1open': [50000, ['nxxxxe', 'exxxxn']],
# 'triplet2opens': [30000, ['exxxe']]}
# y1 = np.array([[1, 2, 3, 4], [1, 3, 5, 7], [1, 2, 4, 6], [2, 2, 3, 2]])
# y2 = np.array([[100, 200], [100,300], [100, 200], [200, 200]])
# z = np.array([1, 2])
# b = np.random.randint(5, size=(10, 10))
#
# dig1 = [b.diagonal(i) for i in range(b.shape[1]-5, -b.shape[1]+4, -1)]
# dig2 = [b[::-1, :].diagonal(i) for i in range(b.shape[1]-5, -b.shape[1]+4, -1)]

# a = 'aababa'
# b = 'aba'
# dig1 = len(re.findall(b,a))


# a = {'a5':1, 'b5':2}
# best = max(a.items(), key=operator.itemgetter(1))[0]
# print(best)
# print(b)





# print(threatMoves)
# print(dig2)
# print(np.where(y1==z))
# count = len(np.where(y1==z))
# print(strlist)
