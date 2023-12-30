"""Checkers game."""
import pygame

from checkers.ai import AI
from checkers.board import CheckersBoard
from checkers.constants import Board, Colors, Player


class CheckersGame:
    """Class that implements the checkers game.

    Attributes:
        window: The pygame window for display.
        run: Whether the game is running.
        clock: A pygame object to help track time.
        fps: Frames per second of the game.
    """

    def __init__(self, window: pygame.Surface, fps: int):
        self._create_new_game()
        self.window = window
        self.run = True
        self.clock = pygame.time.Clock()
        self.fps = fps
        pygame.display.set_caption("Checkers AI")

    def _create_new_game(self) -> None:
        """Creates a new game state."""
        self.board = CheckersBoard()
        self.ai = AI()
        self.turn = Player.HUMAN
        self.selected_piece = None
        self.possible_moves = {}

    def update(self) -> None:
        """Updates the visual game state."""
        self.board.draw(self.window)

        # Draw possible moves
        for move in self.possible_moves:
            row, col = move
            pygame.draw.circle(
                self.window,
                Colors.GREEN,
                (col * Board.SQUARE_SIZE + Board.SQUARE_SIZE // 2, row * Board.SQUARE_SIZE + Board.SQUARE_SIZE // 2),
                15,
            )

        self.clock.tick(self.fps)
        pygame.display.update()

    def show_winner(self, winner: pygame.Color) -> None:
        """Shows the winner of the game."""
        font = pygame.font.Font(None, 36)
        text = font.render("You lost!" if winner == Player.AI else "You won!", True, (255, 255, 255))
        text_rect = text.get_rect(center=(Board.WIDTH // 2, Board.HEIGHT // 2))
        pygame.draw.rect(
            self.window,
            (0, 0, 0),
            (Board.WIDTH // 4, Board.HEIGHT // 4, Board.WIDTH // 2, Board.HEIGHT // 2),
        )
        self.window.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(3000)

    def winner(self) -> pygame.Color | None:
        """Returns the color of the game winner if they exist, otherwise None."""
        return self.board.winner()

    def reset(self) -> None:
        """Resets the game state."""
        self._create_new_game()

    def select_or_move_piece(self, row: int, col: int) -> bool:
        """Selects or moves a piece given row and col position."""
        if self.selected_piece:
            piece = self.board.get_piece(row, col)
            if self.selected_piece and piece is None and (row, col) in self.possible_moves:
                self.board.move(self.selected_piece, row, col)
                jump_over_pieces = self.possible_moves[(row, col)]
                if jump_over_pieces:
                    self.board.remove(jump_over_pieces)
                self.change_player_turn()
            else:
                self.selected_piece = None
                self.select_or_move_piece(row, col)

        piece = self.board.get_piece(row, col)
        if piece is not None and piece.color == self.turn:
            self.selected_piece = piece
            self.possible_moves = self.board.get_possible_moves(piece)
            return True

        return False

    def change_player_turn(self) -> None:
        """Changes the turn of the players."""
        self.possible_moves = {}
        self.turn = Player.HUMAN if self.turn == Player.AI else Player.AI

    def ai_make_move(self) -> None:
        """Lets the AI make a move using the minimax algorithm."""
        self.board = self.ai.make_move(self.board, Player.AI)
        self.change_player_turn()
