import engine2 as E
import chess
import ezgui

screen = ezgui.Screen(640, 720)

# colours
BLACK, BLACKBOARD = (0, 0, 0), (118, 150, 86)
WHITE, WHTIEBOARD = (255, 255, 255), (238, 238, 210)
SELECTED = (186, 202, 68)

def draw_text(text, x, y, c):
    screen.update_options(font=('freesansbold.ttf', 24))
    screen.text(text, x, y, c)


def draw_checker_board(markers=[], indicators=[], dialog=""):
    screen.update_options(background_colour=WHTIEBOARD)  # draw the board
    for i in range(64):
        x, y = i % 8, int(i / 8)
        if x % 2 == 0 and y % 2 == 1:
            screen.rect(x * 80, y * 80, 80, 80, BLACKBOARD)
        if x % 2 == 1 and y % 2 == 0:
            screen.rect(x * 80, y * 80, 80, 80, BLACKBOARD)

    screen.rect(0, 640, 640, 7, BLACK)

    '########################### menu ###########################'

    if autoplay:
        draw_text("Auto", 40, 680, (0, 255, 0))
    else:
        draw_text("Auto", 40, 680, (220, 220, 220))

    if aiwhite:
        draw_text("White", 120, 680, WHITE)
    else:
        draw_text("Black", 120, 680, BLACK)

    draw_text("Reset", 200, 680, BLACK)
    draw_text("Back", 280, 680, BLACK)
    draw_text("Flip", 360, 680, BLACK)
    draw_text(dialog, 520, 680, BLACK)

    '########################### menu ###########################'

    screen.update_options(font=('FreeSerif.ttf', 76))
    for i in markers:
        screen.circle(i[0] * 80 + 40, i[1] * 80 + 40, 20, (0, 255, 0))
    for i in indicators:
        screen.circle(i[0] * 80 + 40, i[1] * 80 + 40, 20, (255, 0, 0))

    position = board.request_board_layout(flipped)  # draw the pieces
    for y in range(len(position)):
        for x in range(len(position[y])):
            letter = str(position[y][x])
            if letter != '0':
                if (x, y) == selected:
                    if letter.isupper():
                        screen.text(chess.Piece.unicode_symbol(chess.Piece.from_symbol(letter)), x * 80 + 40, y * 80 + 40, c=(SELECTED))
                    else:
                        screen.text(chess.Piece.unicode_symbol(chess.Piece.from_symbol(letter)), x * 80 + 40, y * 80 + 40, c=(SELECTED))
                else:
                    if letter.isupper():
                        screen.text(chess.Piece.unicode_symbol(chess.Piece.from_symbol(letter)), x * 80 + 40, y * 80 + 40, c=(WHITE))
                    else:
                        screen.text(chess.Piece.unicode_symbol(chess.Piece.from_symbol(letter)), x * 80 + 40, y * 80 + 40, c=(BLACK))

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
    move = board.make_move(board.board.turn, flipped)
    board.board.push(move)
    if not flipped:
        indicators.append((int(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'].index(
            str(move)[2])), -int(str(move)[3]) + 8))
    else:
        indicators.append((-int(['a', 'b', 'c', 'd', 'e', 'f', 'g',
                                 'h'].index(str(move)[2])) + 7, int(str(move)[3]) - 1))
    draw_checker_board(indicators=indicators, dialog="Your turn")

screen.add_switch(0, 640, 80, 80, 'autoplay', default=False, Tcolour=(WHTIEBOARD), Fcolour=(BLACKBOARD))

draw_checker_board(markers, dialog="Welcome")

def main():
    if autoplay and not game_over:
        if aiwhite and board.board.turn or not aiwhite and not board.board.turn or debug_play:
            AIPlay()

def click(x, y):
    global markers, piece_coord
    mouse = (int(x / 80), int(y / 80))
    if not game_over:
        selected = mouse
        promotion = ''
        if selected in markers:  # check if clicked on piece or marker
            if markers.count(selected) > 1:
                promotion = input("Enter q, b, n, r for promotion")
            board.coor_move(piece_coord[0], -piece_coord[1] + 8, selected[0], -selected[1] + 8, flipped, promotion=promotion)
            markers.clear()
            pass
        else:
            piece_coord = mouse
            markers = board.request_piece_move(mouse[0], -mouse[1] + 8, flipped) if not flipped else board.request_piece_move(mouse[0], mouse[1] + 1, flipped)
        draw_checker_board(markers)



screen.run(main, click)

'''
while True:  # main game loop
    mouse = pygame.mouse.get_pos()
    mouse = (int(mouse[0] / 80), int(mouse[1] / 80))

    if autoplay and not game_over:
        if aiwhite and board.board.turn or not aiwhite and not board.board.turn or debug_play:
            AIPlay()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP and not game_over:  # click
            '########################### buttons ###########################'

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

            '########################### buttons ###########################'

        if event.type == pygame.KEYDOWN and not game_over:  # check if space has been pressed
            if event.key == pygame.K_SPACE:
                AIPlay()

        if event.type == QUIT:  # check if the game has been quit
            pygame.quit()
            sys.exit()

    if board.board.is_game_over():
        game_over = True
        draw_checker_board(dialog="Game over")

    pygame.display.update()
'''
