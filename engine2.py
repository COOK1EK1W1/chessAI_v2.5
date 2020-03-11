import chess
import minimax as MM

# turn true == white
values = {"p": -1, "n": -3, "b": -3, "r": -5, "q": -9,
          "P": 1, "N": 3, "B": 3, "R": 5, "Q": 9, "k": 0, "K": 0}


class ChessAi:
    def __init__(self, lookahead):
        self.board = chess.Board()
        self.depth = lookahead

    def request_board_layout(self, flipped):
        b = []
        lines = self.board.fen().split(" ")[0].split("/")[:8]
        for line in lines:
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

    def make_move(self, player, flipped):
        print(player)
        move = MM.find_best_move(self.board, self.depth, player, chess.Board.push, lambda position: list(
            position.legal_moves), chess.Board.is_game_over, evalboard, bias)
        return move


def evalboard(source):  # higher score for white
    pieces = source.piece_map()
    pieces = list(pieces.values())
    peicetotal = 0
    if source.is_game_over():
        if source.turn:
            peicetotal -= 10
        else:
            peicetotal += 10
    else:
        for piece in pieces:
            peicetotal += values[str(piece)]
    return peicetotal


def bias(position):
    score = 0
    if position.is_checkmate():
        if not position.turn:
            score += float("inf")
        else:
            score -= float("inf")
    if position.is_check():
        if not position.turn:
            score += 0.5
        else:
            score -= 0.5
    return score
