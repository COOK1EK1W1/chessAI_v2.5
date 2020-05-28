import chess
import numpy as np
import keras
import random
board = chess.Board()


onehot_pieces = {
    ' ': [0,0,0,0,0,0,0,0,0,0,0,0],
    'P': [1,0,0,0,0,0,0,0,0,0,0,0],     # White Pawn
    'p': [0,1,0,0,0,0,0,0,0,0,0,0],    # Black Pawn
    'N': [0,0,1,0,0,0,0,0,0,0,0,0],     # White Knight
    'n': [0,0,0,1,0,0,0,0,0,0,0,0],    # Black Knight
    'B': [0,0,0,0,1,0,0,0,0,0,0,0],     # White Bishop
    'b': [0,0,0,0,0,1,0,0,0,0,0,0],    # Black Bishop
    'R': [0,0,0,0,0,0,1,0,0,0,0,0],     # White Rook
    'r': [0,0,0,0,0,0,0,1,0,0,0,0],    # Black Rook
    'Q': [0,0,0,0,0,0,0,0,1,0,0,0],     # White Queen
    'q': [0,0,0,0,0,0,0,0,0,1,0,0],    # Black Queen
    'K': [0,0,0,0,0,0,0,0,0,0,1,0],     # White King
    'k': [0,0,0,0,0,0,0,0,0,0,0,1]     # Black King
    }

piece_values = {
    'P': 1,     # White Pawn
    'p': -1,    # Black Pawn
    'N': 3,     # White Knight
    'n': -3,    # Black Knight
    'B': 3,     # White Bishop
    'b': -3,    # Black Bishop
    'R': 5,     # White Rook
    'r': -5,    # Black Rook
    'Q': 9,     # White Queen
    'q': -9,    # Black Queen
    'K': 0,     # White King
    'k': 0     # Black King
    }

def convert_to_int(board):
    epd_string = board.epd()
    list_int = []
    for i in epd_string:
        if i == " ":
            return np.array(list_int)
        elif i != "/":
            if i in onehot_pieces:
                list_int.append(onehot_pieces[i])
            else:
                for _ in range(0, int(i)):
                    list_int.append(onehot_pieces[' '])

def get_board_score(board):
    epd_string = board.epd()
    list_int = []
    for i in epd_string:
        if i == " ":
            return sum(list_int)
        elif i != "/":
            if i in piece_values:
                list_int.append(piece_values[i])


model = keras.Sequential([
    keras.layers.Flatten(input_shape=(64, 12)),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(2)
])

model.summary()

model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adadelta(),
              metrics=['accuracy'])



for i in range(10):
    goodboard = []
    badboard = []
    for Game in range(1000):
        game_board = chess.Board()
        for i in range(random.randint(0,5)):
            game_board.push(random.choice(list(game_board.legal_moves)))

        white_boards = []
        black_boards = []
        for time in range(75):
            if game_board.is_game_over():
                break
            available_moves = game_board.legal_moves

            predict_boards = []
            for move in available_moves:
                tempboard = game_board.copy()
                tempboard.push(move)
                predict_boards.append(convert_to_int(tempboard))
            predictions = model.predict(np.array(predict_boards))

            heighest_prob = -np.Infinity
            best_move = 0

            for i, prediction in enumerate(predictions):
                if game_board.turn:
                    if prediction[0] - prediction[1] > heighest_prob:
                        heighest_prob = prediction[0] - prediction[1]
                        best_move = i

                else:
                    if prediction[1] - prediction[0] > heighest_prob:
                        heighest_prob = prediction[1] - prediction[0]
                        best_move = i
            move = list(available_moves)[best_move]
            game_board.push(move)
            if game_board.turn:
                white_boards.append(convert_to_int(game_board))
            else:
                black_boards.append(convert_to_int(game_board))

        score = get_board_score(game_board)
        if score > 0:
            goodboard += white_boards
            badboard += black_boards
        else:
            goodboard += black_boards
            badboard += white_boards
        if Game % 10 == 0:
            print(Game)



    boards = np.array(goodboard + badboard)
    print(np.shape(boards))
    labels = [[1,0] for _ in range(len(goodboard))]
    labels += [[0,1] for _ in range(len(badboard))]
    labels = np.array(labels)


    model.train_on_batch(boards, labels)
    
    print(model.evaluate(boards, labels))
model.save("model_2")