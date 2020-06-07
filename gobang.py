import os
import sys
import argparse
import numpy as np
import random
import re
import string
import operator

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

EMPTY = 0
DARK = 1
LIGHT = 2
SCORE_WEIGHT = 1.2
WIN = heuristic['five'][1][0]
STRAIGHT_FOUR = heuristic['four2open'][1][0]
STRAIGHT_THREE = heuristic['three2open'][1][0]

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
    max_moves = set()
    min_moves = set()
    alpha = float('-inf')
    beta = float('inf')
    scores = dict()
    four_threats = set()
    three_threats = set()
    four_attacks = set()
    best_moves_four = dict()
    best_moves_three = dict()

    # Find only moves that are adjacent to the moves that have been made
    threatSpace = set()
    for row in range(board.shape[0]):
        for col in range(board.shape[1]):
            if board[row][col] == EMPTY:
                possible_move = moveConvertType([row,col])
                max_moves.add(possible_move)
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
    max_moves = max_moves.intersection(threatSpace)

    # special case: only last one/two squares are available on the board
    if len(max_moves) <= 2:
        print('last one or two moves open, choosing randomly')
        return moveConvertType(random.choice(tuple(max_moves)))

    # Create new boards with possible minimax moves and evaluate scenarios
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
            computer_board = boardToStrings(new_board, computerColor)
            player_board = boardToStrings(new_board, playerColor)

            # if winning move available, then go for it!
            if searchBoardSeq(computer_board, WIN) != 0:
                print('found a winning move')
                return max_move
            # if MIN threats to win in the next move, then block it!
            if searchBoardSeq(player_board, WIN) != 0:
                print('threat of loosing in one move, blocking...')
                return min_move
            # prevent moves that yield straight fours
            if searchBoardSeq(player_board, STRAIGHT_FOUR) != 0:
                four_threats.add(moveConvertType(min_move))

            # option to make a straight four of your own
            if searchBoardSeq(computer_board, STRAIGHT_FOUR) != 0:
                four_attacks.add(moveConvertType(max_move))

            # # prevent moves that yield straight threes
            # if searchBoardSeq(player_board, STRAIGHT_THREE) != 0:
            #     three_threats.add(moveConvertType(min_move))

            scenarios[maxmove][minmove] = getScore(computer_board, player_board)
            # Alpha pruning
            if scenarios[maxmove][minmove] <= alpha:
                break

        bestMinMove = min(scenarios[maxmove].items(), key=operator.itemgetter(1))[0]
        score = scenarios[maxmove][bestMinMove]
        alpha = max(alpha, score)
        scores[maxmove] = score

    if len(four_threats) != 0:
        print('threat of a straight four in one move, preventing...')
        for threat in four_threats:
            best_moves_four[threat] = scores[threat]
        print(best_moves_four)
        bestMaxMove = max(best_moves_four.items(), key=operator.itemgetter(1))[0]
        move = moveConvertType(bestMaxMove)
        return move

    if len(four_attacks) != 0:
        print('attack of a straight four in one move, executing...')
        for attack in four_attacks:
            best_moves_four[attack] = scores[attack]
        print(best_moves_four)
        bestMaxMove = max(best_moves_four.items(), key=operator.itemgetter(1))[0]
        move = moveConvertType(bestMaxMove)
        return move

    # if len(three_threats) != 0:
    #     print('threat of a straight three in one move, preventing...')
    #     for threat in three_threats:
    #         best_moves_three[threat] = scores[threat]
    #     print(best_moves_three)
    #     bestMaxMove = max(best_moves_three.items(), key=operator.itemgetter(1))[0]
    #     move = moveConvertType(bestMaxMove)
    #     return move

    bestMaxMove = max(scores.items(), key=operator.itemgetter(1))[0]
    move = moveConvertType(bestMaxMove)
    print(scores)

    return move

def getComputerMove(board, computerColor, playerColor, depth):
    # If computer goes first, place the stone somewhere in the middle
    size = len(board)
    start = int(size - 3 - size/2)
    stop = int(size - 3)
    if not board.any():
        move = [random.randint(start, stop), random.randint(start, stop)]
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
                print_board(the_board)
                print('You have won!')
                break
            else:
                if isBoardFull(the_board):
                    print_board(the_board)
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
                print_board(the_board)
                print('The computer have won!')
                break
            else:
                if isBoardFull(the_board):
                    print_board(the_board)
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
