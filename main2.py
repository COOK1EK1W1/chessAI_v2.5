import pygame
import sys
import engine2 as E
import chess
from pygame.locals import *

pygame.init()

DISPLAYSURF = pygame.display.set_mode((640, 720), 0, 32)

pygame.display.set_caption('Albert the chess ai')
font = pygame.font.Font('FreeSerif.ttf', 76)

# colours
BLACK, BLACKBOARD = (0, 0, 0), (118, 150, 86)
WHITE, WHTIEBOARD = (0, 0, 0), (238, 238, 210)
SELECTED = (186, 202, 68)


def draw_checker_board(markers=[], indicators=[], dialog=""):
    DISPLAYSURF.fill(WHTIEBOARD)  # draw the board
    for i in range(64):
        x, y = i % 8, int(i / 8)
        if x % 2 == 0 and y % 2 == 1:
            pygame.draw.rect(DISPLAYSURF, BLACKBOARD, (x * 80, y * 80, 80, 80))
        if x % 2 == 1 and y % 2 == 0:
            pygame.draw.rect(DISPLAYSURF, BLACKBOARD, (x * 80, y * 80, 80, 80))

    pygame.draw.rect(DISPLAYSURF, BLACK, (0, 640, 640, 7))

    # draw text for the buttons
    font = pygame.font.Font('freesansbold.ttf', 24)
    if autoplay:
        text = font.render("Auto", True, (0, 255, 0))
    else:
        text = font.render("Auto", True, (220, 220, 220))
    textRect = text.get_rect()
    textRect.center = (40, 680)
    DISPLAYSURF.blit(text, textRect)

    if aiwhite:
        text = font.render("White", True, WHITE)
    else:
        text = font.render("Black", True, BLACK)
    textRect = text.get_rect()
    textRect.center = (120, 680)
    DISPLAYSURF.blit(text, textRect)

    text = font.render("Reset", True, BLACK)
    textRect = text.get_rect()
    textRect.center = (200, 680)
    DISPLAYSURF.blit(text, textRect)

    text = font.render("Back", True, BLACK)
    textRect = text.get_rect()
    textRect.center = (280, 680)
    DISPLAYSURF.blit(text, textRect)

    text = font.render("Flip", True, BLACK)
    textRect = text.get_rect()
    textRect.center = (360, 680)
    DISPLAYSURF.blit(text, textRect)

    text = font.render(dialog, True, BLACK)
    textRect = text.get_rect()
    textRect.center = (520, 680)
    DISPLAYSURF.blit(text, textRect)

    font = pygame.font.Font('FreeSerif.ttf', 76)  # draw the markers
    for i in markers:
        pygame.draw.circle(DISPLAYSURF, (0, 255, 0),
                           (i[0] * 80 + 40, i[1] * 80 + 40), 20)
    for i in indicators:
        pygame.draw.circle(DISPLAYSURF, (255, 0, 0),
                           (i[0] * 80 + 40, i[1] * 80 + 40), 20)

    position = board.request_board_layout(flipped)  # draw the pieces
    for y in range(len(position)):
        for x in range(len(position[y])):
            letter = str(position[y][x])

            if letter != '0':
                if (x, y) == selected:
                    if letter.isupper():
                        text = font.render(chess.Piece.unicode_symbol(
                            chess.Piece.from_symbol(letter)), True, SELECTED)
                    else:
                        text = font.render(chess.Piece.unicode_symbol(
                            chess.Piece.from_symbol(letter)), True, SELECTED)
                else:
                    if letter.isupper():
                        text = font.render(chess.Piece.unicode_symbol(
                            chess.Piece.from_symbol(letter)), True, WHITE)
                    else:
                        text = font.render(chess.Piece.unicode_symbol(
                            chess.Piece.from_symbol(letter)), True, BLACK)
                textRect = text.get_rect()
                textRect.center = (x * 80 + 40, y * 80 + 40)
                DISPLAYSURF.blit(text, textRect)


board = E.ChessAi(lookahead=3)

markers = []
selected = ()
making_move = False

needupdate = 1
game_over = False
autoplay = False
flipped = False
aiwhite = False
debug_play = False


def AIPlay():
    indicators = []
    move = board.makemove(board.board.turn, flipped)
    board.board.push(move)
    if not flipped:
        indicators.append((int(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'].index(
            str(move)[2])), -int(str(move)[3]) + 8))
    else:
        indicators.append((-int(['a', 'b', 'c', 'd', 'e', 'f', 'g',
                                 'h'].index(str(move)[2])) + 7, int(str(move)[3]) - 1))
    draw_checker_board(indicators=indicators, dialog="Your turn")


draw_checker_board(markers, dialog="Welcome")
while True:  # main game loop
    mouse = pygame.mouse.get_pos()
    mouse = (int(mouse[0] / 80), int(mouse[1] / 80))

    if autoplay:
        if aiwhite and board.board.turn or not aiwhite and not board.board.turn or debug_play:
            if not game_over:
                AIPlay()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP and not game_over:  # click
            selected = mouse
            promotion = ''
            if selected in markers:  # check if clicked on piece or marker
                if markers.count(selected) > 1:
                    promotion = input("Enter q, b, n, r for promotion")
                board.coor_move(piece_coord[0], -piece_coord[1] + 8,
                                selected[0], -selected[1] + 8, flipped, promotion=promotion)
                markers.clear()
                pass
            else:
                piece_coord = mouse
                if not flipped:
                    markers = board.request_piece_move(
                        mouse[0], -mouse[1] + 8, flipped)
                else:
                    markers = board.request_piece_move(
                        mouse[0], mouse[1] + 1, flipped)
            draw_checker_board(markers)

            ########################### buttons ###########################

            if selected == (0, 8):
                if autoplay:
                    autoplay = False
                    draw_checker_board(markers, dialog="Autoplay off")
                else:
                    autoplay = True
                    draw_checker_board(markers, dialog="Autoplay on")

            if selected == (1, 8):
                if aiwhite:
                    aiwhite = False
                    draw_checker_board(markers, dialog="Ai playing Black")
                else:
                    aiwhite = True
                    draw_checker_board(markers, dialog="Ai playing White")

            if selected == (4, 8):
                if flipped:
                    flipped = False
                    draw_checker_board(markers, dialog="flipped")
                else:
                    flipped = True
                    draw_checker_board(markers, dialog="flipped")

            if selected == (2, 8):
                board.board = chess.Board()
                draw_checker_board()

            if selected == (3, 8):
                if len(board.board.move_stack) > 0:
                    board.board.pop()
                    draw_checker_board()
                else:
                    draw_checker_board(dialog="Cannot go back")
            selected = (9, 9)

            ########################### buttons ###########################

        if event.type == pygame.KEYDOWN and not game_over:  # check if space has been pressed
            if event.key == pygame.K_SPACE:
                AIPlay()
            if event.key == pygame.K_p:
                print(board.board.fen())
            if event.key == pygame.K_q:
                board.board = chess.Board(input("enter starting position"))

        if event.type == QUIT:  # check if the game has been quit
            pygame.quit()
            sys.exit()

    if board.board.is_game_over():
        game_over = True
        draw_checker_board(dialog="Game over")

    pygame.display.update()
