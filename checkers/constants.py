"""Game constants."""
import pygame


class Piece:
    """Checkers piece."""

    PADDING = 16
    OUTLINE = 1
    CROWN = pygame.transform.scale(pygame.image.load("assets/crown.png"), (40, 40))


class Board:
    """Checkers board."""

    WIDTH = 800
    HEIGHT = 800
    ROWS = 8
    COLS = 8
    SQUARE_SIZE = WIDTH // ROWS
    NUM_PIECES = 12
    AI_DEPTH = 5


class Colors:
    """Checkers colors."""

    SQUARE_LIGHT = pygame.Color(239, 233, 227)
    SQUARE_DARK = pygame.Color(122, 175, 129)
    GREEN = pygame.Color(144, 238, 144)
    GREY = pygame.Color(96, 120, 84)


class Player:
    """Checkers player."""

    AI = pygame.Color(238, 223, 188)
    HUMAN = pygame.Color(204, 61, 70)
