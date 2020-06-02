import os
import sys
import argparse
import numpy as np
import random
import re
import string

EMPTY = 0
DARK = 1
LIGHT = 2


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

def isMoveIllegal(board, move):
    # Check if the player's input move is legal
    illegal_flag = True
    if board[move[0]][move[1]] == 0:
        illegal_flag = False
    return illegal_flag

def getPlayerMove():
    playerInput = input()
    playerMove = re.split('(\d+)', playerInput)
    letters = playerMove[0].split(' ')
    col = string.ascii_lowercase.index(letters[-1])
    row = int(playerMove[1])-1
    move = [row, col]
    line = 'Move played: ' + letters[-1] + playerMove[1] + '\n'
    sys.stdout.write(line)
    sys.stdout.flush()
    return move

def getComputerMove(board, computerColor):

    #### MINIMAX Algorithm ####

    ###########################

    ####   RANDOM CHOICE   ####
    possible_moves = np.argwhere(board == EMPTY)
    move = random.choice(possible_moves)
    ###########################

    letter = string.ascii_lowercase[move[1]]
    number = move[0]+1
    move_output = str(letter)+str(number)
    line = 'Move played: ' + move_output + '\n'
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


def play_gomoku(board_size, light_player_flag):

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
            move = getPlayerMove()
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
            # Computer's turn to make a move
            move = getComputerMove(the_board, computerColor)
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
    args = parser.parse_args()

    play_gomoku(args.n, args.l)

if __name__ == "__main__":
    main()
