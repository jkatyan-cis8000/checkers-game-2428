"""Pure utility functions for the Checkers game."""


def is_dark_square(row: int, col: int) -> bool:
    """Check if a square is dark (playable)."""
    return (row + col) % 2 == 1


def get_distance(from_pos: tuple[int, int], to_pos: tuple[int, int]) -> tuple[int, int]:
    """Get the distance between two positions."""
    from_row, from_col = from_pos
    to_row, to_col = to_pos
    return (to_row - from_row, to_col - from_col)


def are_adjacent(pos1: tuple[int, int], pos2: tuple[int, int]) -> bool:
    """Check if two positions are adjacent (1 square away)."""
    dr, dc = get_distance(pos1, pos2)
    return abs(dr) == 1 and abs(dc) == 1


def are_diagonal(pos1: tuple[int, int], pos2: tuple[int, int]) -> bool:
    """Check if two positions are diagonal."""
    dr, dc = get_distance(pos1, pos2)
    return abs(dr) == abs(dc)


def is_valid_position(row: int, col: int) -> bool:
    """Check if position is within board bounds."""
    return 0 <= row <= 7 and 0 <= col <= 7
