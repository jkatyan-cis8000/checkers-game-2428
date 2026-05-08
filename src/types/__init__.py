"""Pure type definitions for the Checkers game."""

from enum import Enum
from dataclasses import dataclass


class Player(Enum):
    """Player colors."""
    RED = 'red'
    BLACK = 'black'


@dataclass(frozen=True)
class Piece:
    """A checker piece."""
    player: Player
    is_king: bool = False

    def __repr__(self) -> str:
        symbol = 'K' if self.is_king else ''
        return f"{self.player.value[0].upper()}{symbol}"


@dataclass(frozen=True)
class Move:
    """A move from one position to another."""
    from_pos: tuple[int, int]
    to_pos: tuple[int, int]
    captures: list[tuple[int, int]] = None

    def __post_init__(self):
        if self.captures is None:
            object.__setattr__(self, 'captures', [])


@dataclass(frozen=True)
class BoardState:
    """Immutable board state."""
    grid: tuple[tuple[Piece | None, ...], ...]

    def __len__(self) -> int:
        return len(self.grid)

    def __getitem__(self, index) -> tuple[Piece | None, ...]:
        return self.grid[index]
