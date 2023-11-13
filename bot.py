"""
The Brandeis Quant Club ML/AI Competition (November 2023)

Author: @Ephraim Zimmerman
Email: quants@brandeis.edu
Website: brandeisquantclub.com; quants.devpost.com

Description:

For any technical issues or questions please feel free to reach out to
the "on-call" hackathon support member via email at quants@brandeis.edu

Website/GitHub Repository:
You can find the latest updates, documentation, and additional resources for this project on the
official website or GitHub repository: https://github.com/EphraimJZimmerman/chess_hackathon_23

License:
This code is open-source and released under the MIT License. See the LICENSE file for details.
"""

import random
import chess
import time
from collections.abc import Iterator
from contextlib import contextmanager
import test_bot


@contextmanager
def game_manager() -> Iterator[None]:
    """Creates context for game."""

    print("===== GAME STARTED =====")
    ping: float = time.perf_counter()
    try:
        # DO NOT EDIT. This will be replaced w/ judging context manager.
        yield
    finally:
        pong: float = time.perf_counter()
        total = pong - ping
        print(f"Total game time = {total:.3f} seconds")
    print("===== GAME ENDED =====")


class Bot:
    def __init__(self, fen=None):
        self.board = chess.Board(
            fen if fen else "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    def check_move_is_legal(self, initial_position, new_position) -> bool:
        """
            To check if, from an initial position, the new position is valid.

            Args:
                initial_position (str): The starting position given chess notation.
                new_position (str): The new position given chess notation.

            Returns:
                bool: If this move is legal
        """

        return chess.Move.from_uci(initial_position + new_position) in self.board.legal_moves

    def next_move(self) -> str:
        """
            The main call and response loop for playing a game of chess.

            Returns:
                str: The current location and the next move.
        """

        # Assume that you are playing an arbitrary game. This function, which is
        # the core "brain" of the bot, should return the next move in any circumstance.

        # move = str(random.choice([_ for _ in self.board.legal_moves]))
        # print("My move: " + move)
        # return move

        # Max depth of the tree, larger depth = more move predictions
        max_depth = 4
        move, _ = self.minimax(self.board, max_depth,
                               float("-inf"), float("inf"), True)
        return move.uci()

    # Minimax with alpha-beta pruning
    # Developed and modified based on the abstractions from the below website:
    # https://www.youtube.com/watch?v=l-hh51ncgDI
    def minimax(self, board, depth, alpha, beta, is_maximizing):
        if depth == 0 or board.is_game_over():
            return None, self.evaluate_board(board)
        if is_maximizing:
            max_eval = float("-inf")
            best_move = None
            for move in board.legal_moves:
                board.push(move)
                cur_eval = self.minimax(
                    board, depth - 1, alpha, beta, False)[1]
                board.pop()
                if cur_eval > max_eval:
                    max_eval = cur_eval
                    best_move = move
                alph = max(alpha, cur_eval)
                if beta <= alpha:
                    break
                return best_move, max_eval
        else:
            # Minimizing
            min_eval = float("inf")
            best_move = None
            for move in board.legal_moves:
                board.push(move)
                cur_eval = self.minimax(board, depth - 1, alpha, beta, True)[1]
                board.pop()
                if cur_eval < min_eval:
                    min_eval = cur_eval
                    best_move = move
                beta = min(beta, cur_eval)
                if beta <= alpha:
                    break
            return best_move, min_eval

    def evaluate_board(self, board):
        # Chess piece values reference: https://www.chess.com/terms/chess-piece-value
        # King does not have point value, so initilize it to 0
        # Simple evaluation based on the number of live piece on each side
        # White side favor maximizing evalution point
        # Black side favors minimizing evalution point
        piece_values = {chess.PAWN: 1, chess.KNIGHT: 3,
                        chess.BISHOP: 3, chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 0}
        value = 0
        for (piece, piece_value) in piece_values.items():
            value += len(board.pieces(piece, chess.WHITE)) * piece_value
            value -= len(board.pieces(piece, chess.BLACK)) * piece_value
        return value


# Add promotion stuff
if __name__ == "__main__":

    chess_bot = Bot()  # you can enter a FEN here, like Bot("...")
    with game_manager():

        """

        Feel free to make any adjustments as you see fit. The desired outcome 
        is to generate the next best move, regardless of whether the bot 
        is controlling the white or black pieces. The code snippet below 
        serves as a useful testing framework from which you can begin 
        developing your strategy.

        """

        playing = True

        while playing:
            if chess_bot.board.turn:
                chess_bot.board.push_san(test_bot.get_move(chess_bot.board))
            else:
                chess_bot.board.push_san(chess_bot.next_move())
            print(chess_bot.board, end="\n\n")

            if chess_bot.board.is_game_over():
                if chess_bot.board.is_stalemate():
                    print("Is stalemate")
                elif chess_bot.board.is_insufficient_material():
                    print("Is insufficient material")

                # EX: Outcome(termination=<Termination.CHECKMATE: 1>, winner=True)
                print(chess_bot.board.outcome())

                playing = False
