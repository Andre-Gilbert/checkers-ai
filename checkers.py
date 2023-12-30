"""Checkers game entrypoint."""
import pygame

from checkers.constants import Board, Player
from checkers.game import CheckersGame

pygame.init()


def main() -> None:
    """Game loop."""
    game = CheckersGame(window=pygame.display.set_mode((Board.WIDTH, Board.HEIGHT)), fps=60)
    while game.run:
        # AI turn
        if game.turn == Player.AI:
            game.ai_make_move()

        # Check winner
        winner = game.winner()
        if winner is not None:
            game.show_winner(winner)
            game.reset()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.run = False

            # Human turn
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x, y = pos
                row = y // Board.SQUARE_SIZE
                col = x // Board.SQUARE_SIZE
                game.select_or_move_piece(row, col)

        # Update game user interface
        game.update()

    pygame.quit()


if __name__ == "__main__":
    main()
