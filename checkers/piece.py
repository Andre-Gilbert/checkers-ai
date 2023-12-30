"""Checkers piece."""
from dataclasses import dataclass

import pygame

from checkers.constants import Board, Colors, Piece


class CheckersPiece:
    """Class that implements a checkers piece.

    Attributes:
        row: The row the piece is placed at.
        col: The col the piece is placed at.
        color: The color of the piece.
        is_king: Whether the piece is a king.
        coordinate: The coordinate (x, y) of the piece.
    """

    @dataclass
    class Coordinate:
        """Class that implements the center coordinate of the piece."""

        x: int = 0
        y: int = 0

        def calculate_center_pos(self, row: int, col: int) -> None:
            self.x = Board.SQUARE_SIZE * col + Board.SQUARE_SIZE // 2
            self.y = Board.SQUARE_SIZE * row + Board.SQUARE_SIZE // 2

    def __init__(self, row: int, col: int, color: pygame.Color):
        self.row = row
        self.col = col
        self.color = color
        self.is_king = False
        self.coordinate = self.Coordinate()
        self.coordinate.calculate_center_pos(row, col)

    def change_to_king(self) -> None:
        """Changes the piece to a king piece."""
        self.is_king = True

    def draw(self, window: pygame.Surface) -> None:
        """Draws the piece."""
        radius = Board.SQUARE_SIZE // 2 - Piece.PADDING
        pygame.draw.circle(window, Colors.GREY, (self.coordinate.x, self.coordinate.y), radius + Piece.OUTLINE)
        pygame.draw.circle(window, self.color, (self.coordinate.x, self.coordinate.y), radius)
        if self.is_king:
            window.blit(
                Piece.CROWN,
                (self.coordinate.x - Piece.CROWN.get_width() // 2, self.coordinate.y - Piece.CROWN.get_height() // 2),
            )

    def update_pos(self, row: int, col: int) -> None:
        """Updates the position of the piece."""
        self.row = row
        self.col = col
        self.coordinate.calculate_center_pos(row, col)

    def __repr__(self) -> str:
        return str(self.color)
