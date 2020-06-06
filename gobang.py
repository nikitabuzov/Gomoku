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
SCORE_WEIGHT = 1.1

heuristic = {'five': [200000000, ['xxxxx']],
'four2open': [2000000, ['oxxxxo']],
'four1open': [1000000, ['nxxxxo', 'oxxxxn']],
'three2open': [40000, ['oxxxo']],
'three1open': [15000, ['nxxxoo', 'ooxxxn']],
'voidFour2open': [7000, ['oxoxxo', 'oxxoxo']],
'voidFour1open': [3000, ['nxoxxo', 'nxxoxo', 'oxxoxn', 'oxoxxn']],
'two2open': [1000, ['ooxxo', 'oxxoo']],
'two1open': [400, ['nxxooo', 'oooxxn']],
'voidThree2opens': [100, ['oxoxo']],
'voidThree1open': [40, ['nxoxoo', 'ooxoxn']]}

WIN = heuristic['five'][1][0]
STRAIGHT_FOUR = heuristic['four2open'][1][0]

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


def isMoveTaken(board, move):
    # Check if the player's input move is legal
    illegal_flag = True
    if board[move[0]][move[1]] == 0:
        illegal_flag = False
    return illegal_flag

def getPlayerMove(board):
    illegal = True
    while illegal:
        try:
            print('Enter your move:  ')
            playerInput = input()
            move = moveConvertType(playerInput)
            if isMoveTaken(board, move) == True:
                print('That square is taken! Try again:')
            else:
                illegal = False
        except (ValueError, IndexError):
            print('Oops! That is an invalid move. Please try again... ')
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
        rowStr = 'n'
        for item in row:
            if item == 0:
                rowStr += 'o'
            elif item == player:
                rowStr += 'x'
            else:
                rowStr += 'n'
        rowStr += 'n'
        rowStrList.append(rowStr)

    # col
    colBoard = board.copy().transpose()
    for col in colBoard:
        colStr = 'n'
        for item in col:
            if item == 0:
                colStr += 'o'
            elif item == player:
                colStr += 'x'
            else:
                colStr += 'n'
        colStr += 'n'
        colStrList.append(colStr)
    # diagonal
    diagBoard1 = [board.diagonal(i) for i in range(board.shape[1]-5, -board.shape[1]+4, -1)]
    diagBoard2 = [board[::-1, :].diagonal(i) for i in range(board.shape[1]-5, -board.shape[1]+4, -1)]
    for diag in diagBoard1:
        diagStr = 'n'
        for item in diag:
            if item == 0:
                diagStr += 'o'
            elif item == player:
                diagStr += 'x'
            else:
                diagStr += 'n'
        diagStr += 'n'
        diagStrList.append(diagStr)
    for diag in diagBoard2:
        diagStr = 'n'
        for item in diag:
            if item == 0:
                diagStr += 'o'
            elif item == player:
                diagStr += 'x'
            else:
                diagStr += 'n'
        diagStr += 'n'
        diagStrList.append(diagStr)
    strList = rowStrList + colStrList + diagStrList
    return strList

def searchBoardSeq(board, sequence):
    occurances = 0
    for string in board:
        occurances += len(re.findall(sequence, string))
    return occurances

def getScore(board_computer, board_player):
    scoreComputer = 0
    scorePlayer = 0
    for item in heuristic.keys():
        weight = heuristic[item][0]
        countComputer = 0
        countPlayer = 0
        sequences = heuristic[item][1]
        for sequence in sequences:
            countComputer += searchBoardSeq(board_computer, sequence)
            countPlayer += searchBoardSeq(board_player, sequence)
        scoreComputer += countComputer * weight
        scorePlayer += countPlayer * weight
    score = scoreComputer - scorePlayer * SCORE_WEIGHT
    return score

def generateMinimaxMoves(board, computerColor, playerColor, depth):
    scenarios = dict()
    max_moves1 = set()
    max_moves2 = set()
    min_moves = set()
    alpha = float('-inf')
    beta = float('inf')
    scores1 = dict()
    scores2 = dict()

    # Find only moves that are adjacent to the moves that have been made
    threatSpace = set()
    for row in range(board.shape[0]):
        for col in range(board.shape[1]):
            if board[row][col] == EMPTY:
                possible_move = moveConvertType([row,col])
                max_moves1.add(possible_move)
            if board[row][col] != EMPTY:
                if row == 0:
                    if col == 0:
                        threatMoves = set([moveConvertType([row,col+1]),moveConvertType([row+1,col]),moveConvertType([row+1,col+1])])
                    if col == board.shape[1]-1:
                        threatMoves = set([moveConvertType([row,col-1]),moveConvertType([row+1,col]),moveConvertType([row+1,col-1])])
                    else:
                        threatMoves = set([moveConvertType([row,col-1]),moveConvertType([row,col+1]),moveConvertType([row+1,col-1]),moveConvertType([row+1,col]),moveConvertType([row+1,col+1])])
                if row == board.shape[0]-1:
                    if col == 0:
                        threatMoves = set([moveConvertType([row,col+1]),moveConvertType([row-1,col]),moveConvertType([row-1,col+1])])
                    if col == board.shape[1]-1:
                        threatMoves = set([moveConvertType([row,col-1]),moveConvertType([row-1,col]),moveConvertType([row-1,col-1])])
                    else:
                        threatMoves = set([moveConvertType([row,col-1]),moveConvertType([row,col+1]),moveConvertType([row-1,col-1]),moveConvertType([row-1,col]),moveConvertType([row-1,col+1])])
                else:
                    if col == 0:
                        threatMoves = set([moveConvertType([row-1,col]),moveConvertType([row-1,col+1]),moveConvertType([row,col+1]),moveConvertType([row+1,col]),moveConvertType([row+1,col+1])])
                    if col == board.shape[1]-1:
                        threatMoves = set([moveConvertType([row-1,col-1]),moveConvertType([row-1,col]),moveConvertType([row,col-1]),moveConvertType([row+1,col-1]),moveConvertType([row+1,col])])
                    else:
                        threatMoves = set([moveConvertType([row-1,col-1]),moveConvertType([row-1,col]),moveConvertType([row-1,col+1]),moveConvertType([row,col-1]),moveConvertType([row,col+1]),moveConvertType([row+1,col-1]),moveConvertType([row+1,col]),moveConvertType([row+1,col+1])])
                threatSpace.update(threatMoves)

    # Moves for evaluation: empty and inside the threat space
    max_moves1 = max_moves1.intersection(threatSpace)

    # special case: only last one/two squares are available on the board
    if len(max_moves1)<=2:
        print('last one or two moves open, choosing randomly')
        return moveConvertType(random.choice(max_moves1))

    # Create new boards with possible minimax moves and evaluate scenarios
    for maxmove1 in max_moves1:
        min_moves = max_moves1.copy()
        min_moves.remove(maxmove1)
        # if len(min_moves) == 0:
        #     scenarios[maxmove1] = 1
        #     break
        scenarios[maxmove1] = dict()
        for minmove in min_moves:
            max_moves2 = min_moves.copy()
            max_moves2.remove(minmove)
            scenarios[maxmove1][minmove] = dict()
            for maxmove2 in max_moves2:
                new_board = board.copy()
                max_move1 = moveConvertType(maxmove1)
                min_move = moveConvertType(minmove)
                max_move2 = moveConvertType(maxmove2)
                new_board[max_move1[0]][max_move1[1]] = computerColor
                new_board[min_move[0]][min_move[1]] = playerColor
                # convert the new board to strings
                computer_board = boardToStrings(new_board, computerColor)
                player_board = boardToStrings(new_board, playerColor)
                # if winning move available, then go for it!
                if searchBoardSeq(computer_board, WIN) != 0:
                    print('found a winning move')
                    return max_move1
                # if MIN threats to win in the next move, then block it!
                if searchBoardSeq(player_board, WIN) != 0:
                    print('threat of loosing in one move, blocking...')
                    return min_move
                # if searchBoardSeq(player_board, STRAIGHT_FOUR) != 0:
                #     print('threat of losing in two moves, preventing...')
                #     return min_move
                # new_board[max_move2[0]][max_move2[1]] = computerColor
                scenarios[maxmove1][minmove][maxmove2] = getScore(computer_board, player_board)
            # Beta pruning
                if scenarios[maxmove1][minmove][maxmove2] >= beta:
                    break
            bestMaxMove2 = max(scenarios[maxmove1][minmove].items(), key=operator.itemgetter(1))[0]
            score1 = scenarios[maxmove1][minmove][bestMaxMove2]
            beta = min(beta,score1)
            scores1[minmove] = score1
        # Alpha pruning
            if score1 <= alpha:
                break
        bestMinMove = min(scores1.items(), key=operator.itemgetter(1))[0]
        score = scores1[bestMinMove]
        alpha = max(alpha, score)
        scores2[maxmove1] = score

    if len(scenarios) == 1: # this is set for the last open move on the board
        return moveConvertType(list(scenarios.keys())[0])
    
    bestMaxMove = max(scores2.items(), key=operator.itemgetter(1))[0]
    move = moveConvertType(bestMaxMove)

    print(scores2)

    return move

def getComputerMove(board, computerColor, playerColor, depth):
    # If computer goes first, place the stone in the middle
    if not board.any():
        move = [int(len(board)/2), int(len(board)/2)]
    else:
        move = generateMinimaxMoves(board, computerColor, playerColor, depth)

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
    ''' changed arguments of the func'''
    checkboard = boardToStrings(board, who)
    if searchBoardSeq(checkboard, WIN) != 0:
        return True
    return False

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

        else:
            # Computer's turn to make a move
            print_board(the_board)
            move = getComputerMove(the_board, computerColor, playerColor, depth_of_search)
            makeMove(the_board, computerColor, move)
            if isWinner(the_board, computerColor):
                gameIsPlaying = False
                print('The computer have won!')
                break
            else:
                if isBoardFull(the_board):
                    gameIsPlaying = False
                    print('The game is a tie')
                    break
                else:
                    turn = 'player'
    return

def main():
    parser = argparse.ArgumentParser(description='Gomoku Player')
    parser.add_argument('-n', type=int, default=11, help='This option specifies the size of the board. Allowed values are from 5 to 26. The default value is 11.')
    parser.add_argument('-l', action='store_true', help='If this option is specified, the human opponent is going to play with the light colors. If the option is not specified, the human player will be playing with the dark colors. In both cases, the dark players move first.')
    parser.add_argument('-d', type=int, default=3, help='[DOESNOT DO ANYTHING, depth is set to 3] This option specifies the depth of search for Minimax algorithm. The default value is 3.')

    args = parser.parse_args()

    play_gomoku(args.n, args.l, args.d)

if __name__ == "__main__":
    main()
