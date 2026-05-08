"""Move parsing utilities for checkers notation."""

from src.types import Move, Player


def parse_move(notation: str) -> Move:
    """Parse a move from standard checkers notation.
    
    Format: "a1-b2" or "a1x c3" for captures
    """
    notation = notation.strip()
    
    # Handle capture notation: "a1 x c3" or "a1xc3"
    if 'x' in notation:
        parts = notation.replace('x', ' ').split()
        if len(parts) >= 3:
            from_pos = notation_to_coord(parts[0])
            to_pos = notation_to_coord(parts[2])
            return Move(
                from_pos=from_pos,
                to_pos=to_pos,
                captures=[]  # Captures computed in service
            )
    
    # Handle standard move: "a1-b2" or "a1 b2"
    parts = notation.replace('-', ' ').split()
    if len(parts) >= 2:
        from_pos = notation_to_coord(parts[0])
        to_pos = notation_to_coord(parts[1])
        return Move(
            from_pos=from_pos,
            to_pos=to_pos,
            captures=[]
        )
    
    raise ValueError(f"Invalid move notation: {notation}")


def format_move(move: Move) -> str:
    """Format a move for display."""
    from_notation = coord_to_notation(*move.from_pos)
    to_notation = coord_to_notation(*move.to_pos)
    
    if move.captures:
        capture_notations = [coord_to_notation(*c) for c in move.captures]
        return f"{from_notation} x {to_notation} (captured: {', '.join(capture_notations)})"
    
    return f"{from_notation} to {to_notation}"


def notation_to_coord(notation: str) -> tuple[int, int]:
    """Convert checkers notation (e.g., 'a1') to (row, col).
    
    Checkers uses a1 at bottom-left (black's side).
    Row 0 is top, row 7 is bottom.
    """
    notation = notation.lower().strip()
    
    if len(notation) < 2:
        raise ValueError(f"Invalid notation: {notation}")
    
    col_char = notation[0]
    row_str = notation[1:]
    
    if col_char not in 'abcdefgh':
        raise ValueError(f"Invalid column: {col_char}")
    
    col = ord(col_char) - ord('a')
    row = 7 - int(row_str)  # Invert row: a1 (row 1) -> row 7
    
    if row < 0 or row > 7:
        raise ValueError(f"Invalid row: {row_str}")
    
    return (row, col)


def coord_to_notation(row: int, col: int) -> str:
    """Convert (row, col) to checkers notation (e.g., 'a1')."""
    if not (0 <= row <= 7 and 0 <= col <= 7):
        raise ValueError(f"Invalid coordinates: ({row}, {col})")
    
    col_char = chr(ord('a') + col)
    row_num = 7 - row  # Invert back: row 7 -> 1
    
    return f"{col_char}{row_num}"
