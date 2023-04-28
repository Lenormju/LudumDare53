# Example file showing a basic pygame "game loop"
import pygame
from pygame.locals import MOUSEBUTTONDOWN
from typing import Optional, List

# pygame setup
pygame.init()
screen = pygame.display.set_mode((120, 120))
clock = pygame.time.Clock()
running = True

circle = pygame.image.load("assets/circle.png")
circle_box = circle.get_rect()
cross = pygame.image.load("assets/cross.png")
cross_box = cross.get_rect()
empty = pygame.image.load("assets/empty.png")
empty_box = empty.get_rect()

board: List[List[Optional[int]]] = []

def reset_board():
    global board
    board = [
        [None, None, None],
        [None, None, None],
        [None, None, None],
    ]

reset_board()

player_turn = 2

def is_winner() -> Optional[int]:
    line_1_winner = (board[0][0] == board[0][1] == board[0][2])
    line_2_winner = (board[1][0] == board[1][1] == board[1][2])
    line_3_winner = (board[2][0] == board[2][1] == board[2][2])
    col_1_winner = (board[0][0] == board[1][0] == board[2][0])
    col_2_winner = (board[0][1] == board[1][1] == board[2][1])
    col_3_winner = (board[0][2] == board[1][2] == board[2][2])
    diag_1_winner = (board[0][0] == board[1][1] == board[2][2])
    diag_2_winner = (board[0][2] == board[1][1] == board[2][0])
    if line_1_winner:
        return board[0][0]
    elif line_2_winner:
        return board[1][0]
    elif line_3_winner:
        return board[2][0]
    elif col_1_winner:
        return board[0][0]
    elif col_2_winner:
        return board[0][1]
    elif col_3_winner:
        return board[0][2]
    elif diag_1_winner:
        return board[0][0]
    elif diag_2_winner:
        return board[0][2]
    else:
        return None

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    for line_num in range(3):
        for col_num in range(3):
            cell_val = board[line_num][col_num]
            image = (
                empty if cell_val is None
                else circle if cell_val == 1
                else cross if cell_val == 2
                else None
            )
            screen.blit(image, (col_num*40, line_num*40))

    left, middle, right = pygame.mouse.get_pressed()
    if left:
        print(left, middle, right)
        x, y = pygame.mouse.get_pos()
        print(x, y)
        line_numer = y // 40
        col_number = x // 40
        print(line_numer, col_number)
        if board[line_numer][col_number] is None:
            if player_turn == 1:
                board[line_numer][col_number] = 1
                player_turn = 2
            elif player_turn == 2:
                board[line_numer][col_number] = 2
                player_turn = 1
            else:
                raise RuntimeError("invalid player_turn")

            if winner := is_winner():
                reset_board()

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
