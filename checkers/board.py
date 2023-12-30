"""Checkers board."""
from typing import Generator

import pygame

from checkers.constants import Board, Colors, Player
from checkers.piece import CheckersPiece


class CheckersBoard:
    """Class that implements the checkers board.

    Attributes:
        board: The checkers board.
        white_pieces_remaining: The number of white pieces remaining on the board.
        num_white_kings: The number of white king pieces on the board.
        red_pieces_remaining: The number of black pieces remaining on the board.
        num_red_kings: The number of black king pieces on the board.
    """

    def __init__(self):
        self.board = self._create_board()
        self.white_pieces_remaining = Board.NUM_PIECES
        self.num_white_kings = 0
        self.red_pieces_remaining = Board.NUM_PIECES
        self.num_red_kings = 0

    def _create_board(self) -> list[list[CheckersPiece | None]]:
        """Creates a board containing the checkers pieces."""
        board = [[None for _ in range(Board.COLS)] for _ in range(Board.COLS)]
        for row in range(Board.ROWS):
            for col in range(Board.COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        board[row][col] = CheckersPiece(row, col, Player.AI)
                    elif row > 4:
                        board[row][col] = CheckersPiece(row, col, Player.HUMAN)
        return board

    def compute_heuristic(self) -> int:
        """Computes the heuristic for minimax."""
        return (
            self.white_pieces_remaining + self.num_white_kings * 2 - self.red_pieces_remaining - self.num_red_kings * 2
        )

    def get_pieces_by_color(self, color: pygame.Color) -> Generator[CheckersPiece, None, None]:
        """Yields all pieces given a color."""
        for row in self.board:
            for piece in row:
                if piece is not None and piece.color == color:
                    yield piece

    def move(self, piece: CheckersPiece, row: int, col: int) -> None:
        """Moves a piece to the row and col."""
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.update_pos(row, col)
        if row in (0, Board.ROWS - 1):
            piece.change_to_king()
            if piece.color == Player.AI:
                self.num_white_kings += 1
            else:
                self.num_red_kings += 1

    def get_piece(self, row: int, col: int) -> CheckersPiece | None:
        """Returns the piece given rol and col if it exists."""
        return self.board[row][col]

    def draw(self, window: pygame.Surface) -> None:
        """Draws the checkers board."""

        # Draw board
        window.fill(Colors.SQUARE_DARK)
        for row in range(Board.ROWS):
            for col in range(row % 2, Board.COLS, 2):
                pygame.draw.rect(
                    window,
                    Colors.SQUARE_LIGHT,
                    (row * Board.SQUARE_SIZE, col * Board.SQUARE_SIZE, Board.SQUARE_SIZE, Board.SQUARE_SIZE),
                )

        # Draw pieces
        for row in range(Board.ROWS):
            for col in range(Board.COLS):
                piece = self.board[row][col]
                if piece is not None:
                    piece.draw(window)

    def remove(self, pieces: list[CheckersPiece]) -> None:
        """Removes pieces from the board."""
        for piece in pieces:
            self.board[piece.row][piece.col] = None
            if piece is not None:
                if piece.color == Player.HUMAN:
                    self.red_pieces_remaining -= 1
                else:
                    self.white_pieces_remaining -= 1

    def winner(self) -> pygame.Color | None:
        """Returns the winner if they exist, otherwise None."""
        # Check if all pieces are blocked
        red_possible_moves = {}
        for piece in self.get_pieces_by_color(Player.HUMAN):
            red_possible_moves.update(self.get_possible_moves(piece))
        white_possible_moves = {}
        for piece in self.get_pieces_by_color(Player.AI):
            white_possible_moves.update(self.get_possible_moves(piece))

        # Check winner
        if self.red_pieces_remaining <= 0 or not red_possible_moves:
            return Player.AI
        elif self.white_pieces_remaining <= 0 or not white_possible_moves:
            return Player.HUMAN
        return None

    def get_possible_moves(self, piece: CheckersPiece) -> dict[tuple[int, int], list[CheckersPiece]]:
        """Gets all possible moves for a piece.

        Args:
            piece: The piece piece to consider.

        Returns:
            A dictionary containing the row and col the piece can be moved to and
            a list of pieces that will be removed if the piece moves to the specified
            position.
        """

        # Mapping of possible position to pieces that will be jumped over:
        # (row, col) -> [piece 1, ..., piece N]
        moves = {}
        left_col = piece.col - 1
        right_col = piece.col + 1
        row = piece.row

        # Human possible moves
        if piece.color == Player.HUMAN or piece.is_king:
            moves.update(self._move_left(row - 1, max(row - 3, -1), -1, piece.color, left_col, []))
            moves.update(self._move_right(row - 1, max(row - 3, -1), -1, piece.color, right_col, []))

        # AI possible moves
        if piece.color == Player.AI or piece.is_king:
            moves.update(self._move_left(row + 1, min(row + 3, Board.ROWS), 1, piece.color, left_col, []))
            moves.update(self._move_right(row + 1, min(row + 3, Board.ROWS), 1, piece.color, right_col, []))

        return moves

    def _move_left(
        self,
        start_row: int,
        stop_row: int,
        direction: int,
        color: pygame.color,
        col: int,
        prev_jump_over_pieces: list[CheckersPiece],
    ) -> dict[tuple[int, int], list[CheckersPiece]]:
        """Moves to the left of the checkers board.

        Args:
            start_row: The current row to consider.
            stop_row: The last row a piece can move to.
            direction: The direction to move (1, -1).
            color: The current player.
            col: The column to move to.
            prev_jump_over_pieces: A list containing the pieces to jump over.

        Returns:
            A dictionary containing the row and col the piece can be moved to and
            a list of pieces that will be removed if the piece moves to the specified
            position.
        """
        moves = {}
        jump_over_pieces = []
        for row in range(start_row, stop_row, direction):
            if col < 0:
                break

            piece = self.board[row][col]

            # Empty position
            if piece is None:
                # No more pieces that can be jumped over
                if prev_jump_over_pieces and not jump_over_pieces:
                    break
                # Set all pieces to jump over for possible move
                elif prev_jump_over_pieces:
                    moves[(row, col)] = jump_over_pieces + prev_jump_over_pieces
                # If prev pieces to jump over don't exist, only set current pieces to jump over
                else:
                    moves[(row, col)] = jump_over_pieces

                # Update row to consider next move from
                if jump_over_pieces:
                    if direction == -1:
                        row = max(row - 3, 0)
                    else:
                        row = min(row + 3, Board.ROWS)

                    # Move left and right from current position
                    moves.update(self._move_left(row + direction, row, direction, color, col - 1, jump_over_pieces))
                    moves.update(self._move_right(row + direction, row, direction, color, col + 1, jump_over_pieces))
                break
            # Piece of current player
            elif piece.color == color:
                break
            # Piece to jump over
            else:
                jump_over_pieces = [piece]
            # Move left
            col -= 1
        return moves

    def _move_right(
        self,
        start_row: int,
        stop_row: int,
        direction: int,
        color: pygame.Color,
        col: int,
        prev_jump_over_pieces: list[CheckersPiece],
    ) -> dict[tuple[int, int], list[CheckersPiece]]:
        """Moves to the right of the checkers board.

        Args:
            start_row: The current row to consider.
            stop_row: The last row a piece can move to.
            direction: The direction to move (1, -1).
            color: The current player.
            col: The column to move to.
            prev_jump_over_pieces: A list containing the pieces to jump over.

        Returns:
            A dictionary containing the row and col the piece can be moved to and
            a list of pieces that will be removed if the piece moves to the specified
            position.
        """
        moves = {}
        jump_over_pieces = []
        for row in range(start_row, stop_row, direction):
            if col >= Board.COLS:
                break

            piece = self.board[row][col]

            # Empty position
            if piece is None:
                # No more pieces that can be jumped over
                if prev_jump_over_pieces and not jump_over_pieces:
                    break
                # Set all pieces to jump over for possible move
                elif prev_jump_over_pieces:
                    moves[(row, col)] = jump_over_pieces + prev_jump_over_pieces
                # If prev pieces to jump over don't exist, only set current pieces to jump over
                else:
                    moves[(row, col)] = jump_over_pieces

                # Update row to consider next move from
                if jump_over_pieces:
                    if direction == -1:
                        row = max(row - 3, 0)
                    else:
                        row = min(row + 3, Board.ROWS)

                    # Move left and right from current position
                    moves.update(self._move_left(row + direction, row, direction, color, col - 1, jump_over_pieces))
                    moves.update(self._move_right(row + direction, row, direction, color, col + 1, jump_over_pieces))
                break
            # Piece of current player
            elif piece.color == color:
                break
            # Piece to jump over
            else:
                jump_over_pieces = [piece]
            # Move right
            col += 1
        return moves
