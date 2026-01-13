def act(observation, configuration):
    board = observation.board
    columns = configuration.columns
    return [c for c in range(columns) if board[c] == 0][0]
def my_agent(observation, configuration):
    from random import choice
    return choice([c for c in range(configuration.columns) if observation.board[c] == 0])
def smart_agent(observation, configuration):
    import numpy as np

    def drop_piece(board, col, mark, config):
        board_copy = board.copy()
        for row in range(config.rows-1, -1, -1):
            if board_copy[row * config.columns + col] == 0:
                board_copy[row * config.columns + col] = mark
                return board_copy
        return board_copy  # Si colonne pleine, mais on ne devrait pas arriver là

    def check_win(board, config):
        # Vérifie les victoires horizontales, verticales, diagonales
        rows = config.rows
        cols = config.columns
        inarow = config.inarow  # Généralement 4 pour Connect4

        # Horizontal
        for r in range(rows):
            for c in range(cols - inarow + 1):
                if all(board[r*cols + c + i] == board[r*cols + c] and board[r*cols + c] != 0 for i in range(inarow)):
                    return True

        # Vertical
        for r in range(rows - inarow + 1):
            for c in range(cols):
                if all(board[(r+i)*cols + c] == board[r*cols + c] and board[r*cols + c] != 0 for i in range(inarow)):
                    return True

        # Diagonale \
        for r in range(rows - inarow + 1):
            for c in range(cols - inarow + 1):
                if all(board[(r+i)*cols + (c+i)] == board[r*cols + c] and board[r*cols + c] != 0 for i in range(inarow)):
                    return True

        # Diagonale /
        for r in range(rows - inarow + 1):
            for c in range(inarow - 1, cols):
                if all(board[(r+i)*cols + (c-i)] == board[r*cols + c] and board[r*cols + c] != 0 for i in range(inarow)):
                    return True

        return False

    board = observation.board
    columns = configuration.columns
    rows = configuration.rows
    mark = observation.mark

    # Liste des colonnes valides
    valid_moves = [c for c in range(columns) if board[c] == 0]

    # Essaie de gagner
    for col in valid_moves:
        new_board = drop_piece(board, col, mark, configuration)
        if check_win(new_board, configuration):
            return col

    # Essaie de bloquer l'adversaire
    opponent_mark = 3 - mark
    for col in valid_moves:
        new_board = drop_piece(board, col, opponent_mark, configuration)
        if check_win(new_board, configuration):
            return col

    # Sinon, joue au centre ou aléatoirement
    center = columns // 2
    if center in valid_moves:
        return center
    import random
    return random.choice(valid_moves)
