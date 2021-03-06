import time
import random
import chess
import weights

import timeit

# turn true == white


class ChessAi:
    def __init__(self, lookahead):
        self.board = chess.Board()
        self.depth = lookahead

    def request_board_layout(self, flipped):
        b = []
        l = self.board.fen().split(" ")[0].split("/")[:8]
        for line in l:
            row = []
            for i in line:
                if ord(i) in range(49, 57):
                    for _ in range(int(i)):
                        row.append(0)
                else:
                    row.append(i)
            if flipped:
                row.reverse()
            b.append(row)
        if flipped:
            b.reverse()
        return b

    def request_piece_move(self, x, y, flipped):
        columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        moves = self.board.legal_moves
        marker_location = []
        for move in moves:
            X, Y = int(columns.index(str(move)[0])), int(str(move)[1])
            if X == x and Y == y and not flipped:
                marker_location.append(
                    (int(columns.index(str(move)[2])), -int(str(move)[3]) + 8))
            if -X + 7 == x and Y == y and flipped:
                marker_location.append(
                    (-int(columns.index(str(move)[2])) + 7, int(str(move)[3]) - 1))
        return marker_location

    def coor_move(self, X, Y, x, y, flipped, promotion=""):
        columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        if not flipped:
            self.board.push(chess.Move.from_uci(
                str(columns[X] + str(Y) + str(columns[x] + str(y) + promotion))))
        if flipped:
            self.board.push(chess.Move.from_uci(str(
                columns[-X + 7] + str(-Y + 9) + str(columns[-x + 7] + str(-y + 9) + promotion))))

    def makemove(self, player, flipped):
        start = time.time()
        print("checking")
        depth = self.depth
        scores = []
        score = 0

        board_matrix = make_matrix(self.board)
        board_score = evalboard(self.board)
        movesa = self.board.legal_moves
        print([str(i) for i in list(movesa)])
        print("I" + "-" * len(list(movesa)) + "I", end="\r")
        for i, move in enumerate(movesa):
            
            newboardscore = evalmove(self.board, board_score, board_matrix, move)
            newboardmatrix = matrixmove(self.board, board_matrix, move)
            
            score = 0
            

            sanmove = str(self.board.san(move))
            self.board.push(move)
            score += 100 * ("#" in sanmove and player) - 100 * ("#" in sanmove and not player)
            score += 0.5 * ("+" in sanmove and player) - 0.5 * ("+" in sanmove and not player)
            score += minimax(self.board, depth, -float("inf"), float("inf"), not player, newboardscore, newboardmatrix)
            scores.append(score)
            self.board.pop()
            
            time_remaining = "  " + str(round((time.time() - start) * (len(list(movesa)) / (i + 1)) - (time.time() - start), 3)) + "s   "
            print("I" + "#" * (i + 1) + "-" * (len(list(movesa)) - i - 1) + "I" + time_remaining, end="\r")
        print([str(i) for i in scores], min(scores))
        if player:
            x = [i for i in range(len(scores)) if scores[i] == max(scores)]
        else:
            x = [i for i in range(len(scores)) if scores[i] == min(scores)]
        return list(self.board.legal_moves)[random.choice(x)]

def matrixmove(source, source_matrix, move):
    move = str(move)
    columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    x1 = columns.index(move[0])
    y1 = -int(move[1]) + 8
    x2 = columns.index(move[2])
    y2 = -int(move[3]) + 8

    newmatrix = [i[:] for i in source_matrix]
    newmatrix[y1][x1] = '.'
    newmatrix[y2][x2] = source_matrix[y1][x1]
    return newmatrix

def evalmove(source, source_score, source_matrix, move):
    move = str(move)
    columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    x1 = columns.index(move[0])
    y1 = -int(move[1]) + 8
    x2 = columns.index(move[2])
    y2 = -int(move[3]) + 8

    newscore = source_score
    prevpiece = source_matrix[y2][x2]

    newscore -= (weights.piecevalues[prevpiece] + weights.positionweights[prevpiece][y2][x2]) * (prevpiece != '.')
    piecename = source_matrix[y1][x1]

    newscore += weights.positionweights[piecename][y2][x2] - weights.positionweights[piecename][y1][x1]
    return newscore


def evalboard(source):  # higher score for white
    print("hyello")
    matrix = make_matrix(source)
    peicetotal = 0
    if source.is_game_over():
        if source.turn:
            peicetotal -= 10
        else:
            peicetotal += 10
    else:
        for y in range(len(matrix)):
            for x in range(len(matrix[y])):
                piece = matrix[y][x]
                peicetotal += weights.piecevalues[piece] + weights.positionweights[piece][y][x]
    return peicetotal

def make_matrix(board):
    pgn = board.epd()
    foo = []
    pieces = pgn.split(" ", 1)[0]
    rows = pieces.split("/")
    for row in rows:
        foo2 = []
        for thing in row:
            if thing.isdigit():
                for i in range(0, int(thing)):
                    foo2.append('.')
            else:
                foo2.append(thing)
        foo.append(foo2)
    return foo

def minimax(board, depth, alpha, beta, maximizingPlayer, boardscore, board_matrix):
    if board.is_game_over():
        return boardscore
    if maximizingPlayer:
        maxEval = -9999
        for i, move in enumerate(board.legal_moves):
            newboardscore = evalmove(board, boardscore, board_matrix, move)
            if depth-1 == 0:
                Eval = newboardscore
            else:
                newboardmatrix = matrixmove(board, board_matrix, move)
                board.push(move)
                Eval = minimax(board, depth - 1, alpha, beta, False, newboardscore, newboardmatrix)
                board.pop()
            maxEval = max(maxEval, Eval)
            alpha = max(alpha, Eval)
            if beta <= alpha:
                break
        return maxEval
    else:
        minEval = 9999
        for i, move in enumerate(board.legal_moves):
            newboardscore = evalmove(board, boardscore, board_matrix, move)
            if depth-1 == 0:
                Eval = newboardscore
            else:
                newboardmatrix = matrixmove(board, board_matrix, move)
                board.push(move)
                Eval = minimax(board, depth - 1, alpha, beta, True, newboardscore, newboardmatrix)
                board.pop()
            minEval = min(minEval, Eval)
            beta = min(beta, Eval)
            if beta <= alpha:
                break
        return minEval
