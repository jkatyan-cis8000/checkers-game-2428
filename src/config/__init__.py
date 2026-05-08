"""Configuration constants for the Checkers game."""

from src.types import Player

# Board dimensions
BOARD_SIZE = 8

# Player representation symbols
PLAYER_SYMBOLS = {
    Player.RED: 'r',
    Player.BLACK: 'b',
}

KING_SYMBOLS = {
    Player.RED: 'R',
    Player.BLACK: 'B',
}

# Initial board setup
INITIAL_BOARD = """
r r r r
  r r r r
r r r r
        
b b b b
  b b b b
b b b b
"""
