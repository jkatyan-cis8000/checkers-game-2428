"""UI module for CLI interface."""

from src.types import BoardState, Player
from src.providers.move_parser import coord_to_notation


def display_board(board: BoardState) -> str:
    """Render the board as ASCII art."""
    output = []
    output.append("  a b c d e f g h")
    output.append(" +-----------------+")
    
    for row_idx, row in enumerate(board.grid):
        row_num = 8 - row_idx
        line = f"{row_num}|"
        for piece in row:
            if piece is None:
                line += " ."
            else:
                symbol = piece.__repr__()
                line += f" {symbol}"
        line += " |"
        output.append(line)
    
    output.append(" +-----------------+")
    return "\n".join(output)


def display_game_info(current_player: Player, red_count: int, black_count: int) -> str:
    """Display game info."""
    output = []
    output.append(f"Current player: {current_player.value.upper()}")
    output.append(f"Red pieces: {red_count}, Black pieces: {black_count}")
    return "\n".join(output)


def get_user_input(prompt: str) -> str:
    """Get input from user."""
    return input(prompt).strip()


def print_message(message: str):
    """Print a message to the user."""
    print(message)
