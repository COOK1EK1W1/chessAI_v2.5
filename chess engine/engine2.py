import time
import random
import chess

# turn true == white
values = {"p": 1, "n": 3, "b": 3, "r": 5, "q": 9, "P": -
          1, "N": -3, "B": -3, "R": -5, "Q": -9, "k": 0, "K": 0}


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
        print(str([str(move) for move in self.board.legal_moves]))
        print("I" + "-" * len(list(self.board.legal_moves)) + "I", end="\r")
        for i, move in enumerate(self.board.legal_moves):
            time_remaining = "  " + str(round((time.time() - start) * (
                len(list(self.board.legal_moves)) / (i + 1)) - (time.time() - start), 3)) + "s"
            print("I" + "#" * i + "-" * (len(list(self.board.legal_moves)
                                             ) - i) + "I" + time_remaining, end="\r")
            score = 0
            tempboard = self.board.copy()
            tempboard.push(move)
            sanmove = str(self.board.san(move))
            if "#" in sanmove:
                if player:
                    score += 100
                else:
                    score -= 100
            if "+" in sanmove:
                if player:
                    score += 0.5
                else:
                    score -= 0.5
            score += minimax(tempboard, depth, -float("inf"),
                             float("inf"), not player)
            scores.append(score)
        print(scores, sum(scores) / len(scores))
        if player:
            x = [i for i in range(len(scores)) if scores[i] == max(scores)]
        else:
            x = [i for i in range(len(scores)) if scores[i] == min(scores)]
        return list(self.board.legal_moves)[random.choice(x)]


def evalboard(source):  # higher score for white
    pieces = source.piece_map()
    pieces = list(pieces.values())
    peicetotal = 0
    if source.is_game_over() and source.turn:
        if source.turn:
            peicetotal -= 10
        else:
            peicetotal += 10
    else:
        for piece in pieces:
            peicetotal -= values[str(piece)]
    return peicetotal


def minimax(board, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or board.is_game_over():
        return evalboard(board)
    if maximizingPlayer:
        maxEval = -float("inf")
        for move in board.legal_moves:
            tempboard = board.copy()
            tempboard.push(move)
            Eval = minimax(tempboard, depth - 1, alpha, beta, False)
            maxEval = max(maxEval, Eval)
            alpha = max(alpha, Eval)
            if beta <= alpha:
                break
        return maxEval
    else:
        minEval = float("inf")
        for move in board.legal_moves:
            tempboard = board.copy()
            tempboard.push(move)
            Eval = minimax(tempboard, depth - 1, alpha, beta, True)
            minEval = min(minEval, Eval)
            beta = min(beta, Eval)
            if beta <= alpha:
                break
        return minEval
