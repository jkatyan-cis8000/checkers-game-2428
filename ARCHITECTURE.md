# ARCHITECTURE.md

Written by team-lead before spawning teammates. This is the shared blueprint —
teammates read it to understand what they are building and how their module fits.

## Module Structure

- `src/types/__init__.py`: Core types - Player, Piece, BoardState, Move
- `src/config/__init__.py`: Constants - BOARD_SIZE, PLAYER_COLORS
- `src/repo/__init__.py`: Board state persistence interface
- `src/service/__init__.py`: Game logic - validate move, capture logic, kinging
- `src/providers/__init__.py`: Parsing utilities for move notation
- `src/utils/__init__.py`: Pure helpers - coordinate conversion
- `src/runtime/__init__.py`: Game loop orchestration
- `src/ui/__init__.py`: CLI interface - display board, accept moves

## Interfaces

### types.py
- `Player`: Enum (RED, BLACK)
- `Piece`: dataclass - player: Player, is_king: bool
- `BoardState`: 8x8 grid of Piece | None
- `Move`: dataclass - from_pos: tuple[int, int], to_pos: tuple[int, int], captures: list[tuple[int, int]]

### config.py
- `BOARD_SIZE = 8`
- `PLAYER_COLORS = {Player.RED: 'R', Player.BLACK: 'B'}`

### service.py
- `validate_move(board, move, current_player) -> bool`
- `apply_move(board, move) -> BoardState`
- `check_kinging(board, move) -> list[tuple[int, int]]` - returns kings created
- `check_winner(board) -> Player | None`

### providers/move_parser.py
- `parse_move(notation: str) -> Move` - converts "a1-b2" style notation
- `format_move(move: Move) -> str` - converts Move to notation for display

### utils/__init__.py
- `coord_to_notation(row: int, col: int) -> str` - "a1", "h8"
- `notation_to_coord(notation: str) -> tuple[int, int]`

### ui/__init__.py
- `display_board(board: BoardState)` - ASCII art board
- `get_user_move(current_player: Player) -> str` - prompts for notation
- `print_game_state(board, current_player, kings)`

## Shared Data Structures

```
Player = RED | BLACK
Piece = {player: Player, is_king: bool}
BoardState = list[list[Piece | None]]  # 8x8
Move = {from_pos: (row, col), to_pos: (row, col), captures: list[(row, col)]}
```

## External Dependencies

None - pure Python standard library.

## Layer Dependency Flow

```
types → config → repo → service → runtime → ui
                 ↑                    ↑
              providers           providers
                 ↑                    ↑
               utils               utils
```
