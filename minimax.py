import chess, copy, random, time

checked = 0

def find_best_move(position, lookahead, player, push_move, find_moves, gameover, eval_func, bias):
    global checked
    checked = 0
    start = time.time()
    print("checking")
    scores = []
    moves = find_moves(position)
    print("I" + "-" * len(moves) + "I", end="\r")
    for i, move in enumerate(moves):
        score = 0
        temp_pos = copy.deepcopy(position)
        push_move(temp_pos, move)
        inf = float("inf")
        score += bias(temp_pos)
        score += minimax(temp_pos, lookahead, -inf, inf, not player, push_move, find_moves, gameover, eval_func)
        scores.append(score)

        time_remaining = "  " + str(round((time.time() - start) * (len(moves) / (i + 1)) - (time.time() - start), 3)) + "s"
        print("I" + "#" * i + "-" * (len(moves) - i) + "I" + time_remaining, end="\r")

    print(scores, checked)
    if player:
        best_moves = [i for i in range(len(scores)) if scores[i] == max(scores)]
    else:
        best_moves = [i for i in range(len(scores)) if scores[i] == min(scores)]
    return moves[random.choice(best_moves)]

def minimax(position, depth, alpha, beta, maximizingPlayer, push_move, find_moves, gameover, eval_func):
    global checked
    if depth == 0 or gameover(position):
        checked += 1
        return eval_func(position)
    if maximizingPlayer:
        maxEval = -float("inf")
        moves = find_moves(position)
        for move in moves:
            temp_pos = copy.deepcopy(position)
            push_move(temp_pos, move)
            Eval = minimax(temp_pos, depth - 1, alpha, beta, False, push_move, find_moves, gameover, eval_func)
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
            Eval = minimax(temp_pos, depth - 1, alpha, beta, True, push_move, find_moves, gameover, eval_func)
            minEval = min(minEval, Eval)
            beta = min(beta, Eval)
            if beta >= alpha:
                break
        return minEval