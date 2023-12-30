"""Checkers AI."""
from copy import deepcopy
from typing import Generator

import pygame

from checkers.board import CheckersBoard
from checkers.constants import Board, Player
from checkers.piece import CheckersPiece


class AI:
    """Class that implements the checkers AI using the minimax algorithm.

    Attributes:
        depth: The depth the AI searches to in minimax.
    """

    def __init__(self):
        self.depth = Board.AI_DEPTH

    def make_move(self, board: CheckersBoard, player: pygame.Color) -> CheckersBoard:
        """Lets the AI make a move using the minimax algorithm.

        Args:
            board: The current board state.
            player: The AI to make a move.

        Returns:
            The new board state after using minimax.
        """
        alpha = float("-inf")
        beta = float("inf")
        return self.minimax(board, player, self.depth, alpha, beta)[1]

    def minimax(
        self,
        board: CheckersBoard,
        player: pygame.Color,
        depth: int,
        alpha: float | int,
        beta: float | int,
    ) -> tuple[int, CheckersBoard]:
        """The minimax algorithm with alpha-beta pruning.

        The algorithm explores the checkers board, applying a heuristic function to estimate
        the desirability of each possible move. By recursively selecting moves that minimize
        the maximum potential loss, the algorithm determines the optimal move for a player.

        Args:
            board: The current board state.
            player: The current player to find the best move for.
            depth: The search depth.
            alpha: The best (highest) value that the maximizing player currently knows.
            beta: The best (lowest) value that the minimizing player currently knows.

        Returns:
            The best value (highest/lowest depending on current considered player) and
            the best state of the board for the AI.
        """
        if not depth or board.winner() is not None:
            return board.compute_heuristic(), board

        # Max player
        if player == Player.AI:
            max_value = float("-inf")
            best_board = None

            # Get new board states after simulating moves
            for new_board_state in self.get_board_states(board, Player.AI):
                value = self.minimax(board, Player.HUMAN, depth - 1, alpha, beta)[0]
                max_value = max(max_value, value)
                alpha = max(alpha, value)
                if max_value == value:
                    best_board = new_board_state

                # Pruning
                if alpha >= beta:
                    break
            return max_value, best_board

        # Min player
        if player == Player.HUMAN:
            min_value = float("inf")
            best_board = None

            # Get new board states after simulating moves
            for new_board_state in self.get_board_states(board, Player.HUMAN):
                value = self.minimax(board, Player.AI, depth - 1, alpha, beta)[0]
                min_value = min(min_value, value)
                beta = min(beta, value)
                if min_value == value:
                    best_board = new_board_state

                # Pruning
                if alpha >= beta:
                    break
            return min_value, best_board

    def get_board_states(self, board: CheckersBoard, color: pygame.Color) -> Generator[CheckersBoard, None, None]:
        """Gets possible board states using simulation.

        Args:
            board: The current board state.
            color: The current player to consider.

        Yields:
            A new board state after simulating a move.
        """
        for piece in board.get_pieces_by_color(color):
            possible_moves = board.get_possible_moves(piece)

            # Simulate all possible moves
            for move, jump_over_pieces in possible_moves.items():
                temp_board = deepcopy(board)  # Modify board state on copy
                temp_piece = temp_board.get_piece(piece.row, piece.col)
                new_board = self.simulate_move(temp_board, temp_piece, move, jump_over_pieces)
                yield new_board

    def simulate_move(
        self,
        board: CheckersBoard,
        piece: CheckersPiece,
        move: tuple[int, int],
        jump_over_pieces: list[CheckersPiece],
    ) -> CheckersBoard:
        """Simulates a move on the board.

        Args:
            board: The current board state.
            piece: The current piece to consider moving.
            move: The position to move the given piece.
            jump_over_pieces: A list of pieces to jump over.

        Returns:
            The new board state.
        """
        row, col = move
        board.move(piece, row, col)
        if jump_over_pieces:
            board.remove(jump_over_pieces)
        return board
