import numpy as np
import pygame as py

import math
from pygame.constants import K_LEFT, K_RETURN, K_RIGHT, KEYDOWN, QUIT

WHITE = (255, 255, 255)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 6
COL_COUNT = 7

def create_board():
    board = np.zeros((ROW_COUNT,COL_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def winning_move(board, piece):
    #Check horizontal
    for c in range(COL_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    #Check vertical
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    #Check positive diagonal
    for c in range(COL_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    #Check negative diagonal
    for c in range(COL_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def draw_board(board):
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):
            py.draw.rect(screen, WHITE, (c*SIZE, r*SIZE+SIZE, SIZE, SIZE))
            py.draw.circle(screen, BLACK, (int(c*SIZE+SIZE/2), int(r*SIZE+SIZE+SIZE/2)),RADIUS)
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):           
            if board[r][c] == 1:
                py.draw.circle(screen, RED, (int(c*SIZE+SIZE/2), height + SIZE - int(r*SIZE+SIZE+SIZE/2)),RADIUS)
            elif board[r][c] == 2:
                py.draw.circle(screen, YELLOW, (int(c*SIZE+SIZE/2), height + SIZE - int(r*SIZE+SIZE+SIZE/2)),RADIUS)
    py.display.update()

py.init()

board = create_board()

game_over = False
turn = 0
SIZE = 100
width = COL_COUNT * SIZE
height = (ROW_COUNT + 1) * SIZE

size = (width, height)
RADIUS = int(SIZE/2-5)

screen = py.display.set_mode(size)

draw_board(board)
myFont = py.font.SysFont("monospace", 75)

posStart = int(SIZE/2)
posx = posStart

while not game_over:

    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()

        """if event.type == py.MOUSEMOTION:
            py.draw.rect(screen, BLACK, (0,0, width, SIZE))
            posx = event.pos[0]
            if turn == 0:
                py.draw.circle(screen, RED, (posx, int(SIZE/2)), RADIUS)
            else:
                py.draw.circle(screen, YELLOW, (posx, int(SIZE/2)), RADIUS)
        py.display.update()"""

    #py.draw.rect(screen, BLACK, (0,0, width, SIZE))
    #Ask Player 1 Input
        #if turn == 0:
        if posx == posStart: 
            if turn == 0:
                py.draw.circle(screen, RED, (posStart, int(SIZE/2)), RADIUS)
            elif turn == 1:
                py.draw.circle(screen, YELLOW, (posStart, int(SIZE/2)), RADIUS)

        if event.type == py.KEYDOWN:
            if turn == 0:
                if event.key == py.K_d and not posx == COL_COUNT*SIZE-int(SIZE/2):
                    py.draw.circle(screen, BLACK, (posx, int(SIZE/2)), RADIUS)
                    posx = posx + SIZE
                    py.draw.circle(screen, RED, (posx, int(SIZE/2)), RADIUS)

                elif event.key == py.K_a and not posx == int(SIZE/2):
                    py.draw.circle(screen, BLACK, (posx, int(SIZE/2)), RADIUS)
                    posx = posx - SIZE
                    py.draw.circle(screen, RED, (posx, int(SIZE/2)), RADIUS)

                elif event.key == py.K_RETURN:
                    col = int(math.floor(posx/SIZE))
                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col , 1)
                        turn = 1
                        py.draw.circle(screen, YELLOW, (posx, int(SIZE/2)), RADIUS)
                        if winning_move(board, 1):
                            label = myFont.render("Player 1 wins!", 1, RED)
                            screen.blit(label, (40, 10))
                            game_over = True
                            

            elif turn == 1:
                if event.key == py.K_d and not posx == COL_COUNT*SIZE-int(SIZE/2):
                    py.draw.circle(screen, BLACK, (posx, int(SIZE/2)), RADIUS)
                    posx = posx + SIZE
                    py.draw.circle(screen, YELLOW, (posx, int(SIZE/2)), RADIUS)

                elif event.key == py.K_a and not posx == int(SIZE/2):
                    py.draw.circle(screen, BLACK, (posx, int(SIZE/2)), RADIUS)
                    posx = posx - SIZE
                    py.draw.circle(screen, YELLOW, (posx, int(SIZE/2)), RADIUS)

                elif event.key == py.K_RETURN:
                    col = int(math.floor(posx/SIZE))
                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col , 2)
                        turn = 0
                        py.draw.circle(screen, RED, (posx, int(SIZE/2)), RADIUS)
                        if winning_move(board, 2):
                            label = myFont.render("Player 2 wins!", 2, YELLOW)
                            screen.blit(label, (40, 10))
                            game_over = True
                            
        draw_board(board)
       
        if game_over:
            py.time.wait(3000)
       