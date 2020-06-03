import os
import sys
import argparse
import numpy as np
import random
import re
import string
import operator

EMPTY = 0
DARK = 1
LIGHT = 2
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

def print_board(board):
    sys.stdout.write("  ")
    i = 0
    for c in string.ascii_lowercase:
        i += 1
        if i > len(board):
            break
        sys.stdout.write("   %s" % c)
    sys.stdout.write("\n   +")
    for i in range(0, len(board)):
        sys.stdout.write("---+")
    sys.stdout.write("\n")

    for i in range(0, len(board)):
        sys.stdout.write("%2d |" % (i + 1))
        for j in range(0, len(board)):
            if board[i][j] == LIGHT:
                sys.stdout.write(" L |")
            elif board[i][j] == DARK:
                sys.stdout.write(" D |")
            else:
                sys.stdout.write("   |")
        sys.stdout.write("\n   +")
        for j in range(0, len(board)):
            sys.stdout.write("---+")
        sys.stdout.write("\n")

def moveConvertType(move):
    if type(move) == str:
        new_move = re.split('(\d+)', move)
        letters = new_move[0].split(' ')
        col = string.ascii_lowercase.index(letters[-1])
        row = int(new_move[1])-1
        move = [row, col]
    else:
        letter = string.ascii_lowercase[move[1]]
        number = move[0] + 1
        move = str(letter)+str(number)
    return move


def isMoveIllegal(board, move):
    # Check if the player's input move is legal
    illegal_flag = True
    if board[move[0]][move[1]] == 0:
        illegal_flag = False

    '''TODO: check for out of bounds'''

    return illegal_flag

def getPlayerMove(board):
    illegal = True
    while illegal:
        playerInput = input()
        move = moveConvertType(playerInput)
        if isMoveIllegal(board, move) == True:
            print('Illegal move! Try again:')
        else:
            illegal = False
    line = 'Move played: ' + playerInput + '\n'
    sys.stdout.write(line)
    sys.stdout.flush()
    return move

def boardToStrings(board, player):
    rowStrList = []
    colStrList = []
    diagStrList = []
    # row
    for row in board:
        rowStr = ''
        for item in row:
            if item == 0:
                rowStr += 'o'
            if item == player:
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
            if item == player:
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
            if item == player:
                diagStr += 'x'
            else:
                diagStr += 'n'
        diagStrList.append(diagStr)
    for diag in diagBoard2:
        diagStr = ''
        for item in diag:
            if item == 0:
                diagStr += 'o'
            if item == player:
                diagStr += 'x'
            else:
                diagStr += 'n'
        diagStrList.append(diagStr)
    strList = rowStrList + colStrList + diagStrList
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
        scoreComputer += countComputer * weight
        scorePlayer += countPlayer * weight
    score = scoreComputer - scorePlayer
    # score = random.uniform(1,10)
    return score

def generateMoves(board, computerColor, playerColor, depth):
    scenarios = dict()
    max_moves = set() # empty fields on the board for MAX to play
    min_moves = set() # options for MIN to play after possible MAX move
    for row in range(board.shape[0]):
        for col in range(board.shape[1]):
            if board[row][col] == EMPTY:
                possible_move = moveConvertType([row,col])
                max_moves.add(possible_move)
    # Create new boards with possible max moves
    for maxmove in max_moves:
        min_moves = max_moves.copy()
        min_moves.remove(maxmove)
        scenarios[maxmove] = dict()
        for minmove in min_moves:
            new_board = board.copy()
            max_move = moveConvertType(maxmove)
            min_move = moveConvertType(minmove)
            new_board[max_move[0]][max_move[1]] = computerColor
            new_board[min_move[0]][min_move[1]] = playerColor
            # Get scores for all the possible scenarios
            scenarios[maxmove][minmove] = getScore(new_board, computerColor, playerColor)
    return scenarios

def minimax(scenarios):
    scores = dict()
    
    for move in scenarios:
        bestMinMove = min(scenarios[move].items(), key=operator.itemgetter(1))[0]
        score = scenarios[move][bestMinMove]
        # print(score)
        scores[move] = score
    bestMaxMove = max(scores.items(), key=operator.itemgetter(1))[0]
    move = moveConvertType(bestMaxMove)
    return move

def getComputerMove(board, computerColor, playerColor, depth):
    # If computer goes first, place the stone in the middle
    if not board.any():
        move = [int(len(board)/2+1), int(len(board)/2+1)]
    else:
    #### MINIMAX Algorithm ####
    # 1. Generate all possible scenarios of depth D (possible moves)
    # 2. Compute all childs' scores (how likely each will lead to a win)
    # 3. Use minimax algorithm to make a choice of next move
        scenarios = generateMoves(board, computerColor, playerColor, depth) # return dict of dicts with moves and scores
        move = minimax(scenarios) # make a move based on minimax algorithm

    move_string = moveConvertType(move)
    line = 'Move played: ' + move_string + '\n'
    sys.stdout.write(line)
    sys.stdout.flush()
    return move

def makeMove(board, player, move):
    the_board = board
    if player == LIGHT:
        the_board[move[0]][move[1]] = LIGHT
    else:
        the_board[move[0]][move[1]] = DARK
    return the_board

def isWinner(board, who):
    answer = False
    if who == LIGHT:
        player = 1
    if who == DARK:
        player = 2
    return answer

def isBoardFull(board):
    answer = False
    possible_moves = np.argwhere(board == EMPTY)
    if len(possible_moves) == 0:
        answer = True
    return answer


def play_gomoku(board_size, light_player_flag, depth_of_search):

    the_board = np.zeros((board_size, board_size), dtype=int)

    if light_player_flag==True:
        playerColor = LIGHT
        computerColor = DARK
        turn = 'computer'
    else:
        playerColor = DARK
        computerColor = LIGHT
        turn = 'player'

    print('The ' + turn + ' will go first')


    gameIsPlaying = True
    while gameIsPlaying:
        if turn == 'player':
            # Player's turn to make a move
            print_board(the_board)
            move = getPlayerMove(the_board)
            makeMove(the_board, playerColor, move)
            if isWinner(the_board, playerColor):
                # drawBoard(the_board)
                gameIsPlaying = False
                print('You have won!')
                break
            else:
                if isBoardFull(the_board):
                    # drawBoard(the_board)
                    gameIsPlaying = False
                    print('The game is a tie')
                    break
                else:
                    turn = 'computer'
            # turn = 'computer'

        else:
            # Computer's turn to make a
            move = getComputerMove(the_board, computerColor, playerColor, depth_of_search)
            makeMove(the_board, computerColor, move)
            if isWinner(the_board, computerColor):
                # drawBoard(the_board)
                gameIsPlaying = False
                print('The computer have won!')
                break
            else:
                if isBoardFull(the_board):
                    # drawBoard(the_board)
                    gameIsPlaying = False
                    print('The game is a tie')
                    break
                else:
                    turn = 'player'
            # turn = 'player'
    return

def main():
    parser = argparse.ArgumentParser(description='Gomoku Player')
    parser.add_argument('-n', type=int, default=11, help='This option specifies the size of the board. Allowed values are from 5 to 26. The default value is 11.')
    parser.add_argument('-l', action='store_true', help='If this option is specified, the human opponent is going to play with the light colors. If the option is not specified, the human player will be playing with the dark colors. In both cases, the dark players move first.')
    parser.add_argument('-d', type=int, default=3, help='This option specifies the depth of search for Minimax algorithm. The default value is 3.')

    args = parser.parse_args()

    play_gomoku(args.n, args.l, args.d)

if __name__ == "__main__":
    main()
