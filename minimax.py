import copy
import random


def find_best_move(position, lookahead, player, push_move, find_moves, gameover, eval_func):
    print("checking")
    scores = []
    moves = find_moves(position)
    print("I" + "-" * len(moves) + "I", end="\r")
    for i, move in enumerate(moves):
        print("I" + "#" * i, end="\r")
        temp_pos = copy.deepcopy(position)
        push_move(temp_pos, move)
        inf = float("inf")
        scores.append(minimax(temp_pos, lookahead, -inf, inf,
                              not player, push_move, find_moves, gameover, eval_func))
    print(scores)
    if not player:
        x = [i for i in range(len(scores)) if scores[i] == max(scores)]
    else:
        x = [i for i in range(len(scores)) if scores[i] == min(scores)]
    return moves[random.choice(x)]


def minimax(position, depth, alpha, beta, maximizingPlayer, push_move, find_moves, gameover, eval_func):
    if depth == 0 or gameover(position):
        return eval_func(position)
    if maximizingPlayer:
        maxEval = -float("inf")
        moves = find_moves(position)
        for move in moves:
            temp_pos = copy.deepcopy(position)
            push_move(temp_pos, move)
            Eval = minimax(temp_pos, depth - 1, alpha, beta, False,
                           push_move, find_moves, gameover, eval_func)
            maxEval = max(maxEval, Eval)
            alpha = max(alpha, Eval)
            if beta <= alpha:
                break
        return maxEval
    else:
        minEval = float("inf")
        moves = find_moves(position)
        for move in moves:
            temp_pos = copy.deepcopy(position)
            push_move(temp_pos, move)
            Eval = minimax(temp_pos, depth - 1, alpha, beta, True,
                           push_move, find_moves, gameover, eval_func)
            minEval = min(minEval, Eval)
            alpha = min(alpha, Eval)
            if beta >= alpha:
                break
        return minEval
