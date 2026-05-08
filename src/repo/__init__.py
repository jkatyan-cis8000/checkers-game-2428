"""Data access interface for board state."""

from abc import ABC, abstractmethod
from typing import Protocol
from src.types import BoardState, Move, Player


class BoardRepository(ABC):
    """Interface for board state persistence."""
    
    @abstractmethod
    def get_initial_board(self) -> BoardState:
        """Return the initial board state."""
        pass
    
    @abstractmethod
    def apply_move(self, board: BoardState, move: Move) -> BoardState:
        """Apply a move to the board and return new state."""
        pass
    
    @abstractmethod
    def check_kinging(self, board: BoardState, move: Move) -> list[tuple[int, int]]:
        """Check if any pieces were kinged by this move."""
        pass
    
    @abstractmethod
    def check_winner(self, board: BoardState) -> Player | None:
        """Check if there's a winner."""
        pass


class InMemoryBoardRepository(BoardRepository):
    """In-memory implementation of board repository."""
    
    def get_initial_board(self) -> BoardState:
        """Create initial 8x8 board with pieces."""
        from src.types import BoardState, Piece, Player
        
        grid = [[None for _ in range(8)] for _ in range(8)]
        
        # Place red pieces (top 3 rows, dark squares)
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    grid[row][col] = Piece(player=Player.RED)
        
        # Place black pieces (bottom 3 rows, dark squares)
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    grid[row][col] = Piece(player=Player.BLACK)
        
        return BoardState(grid=tuple(tuple(row) for row in grid))
    
    def apply_move(self, board: BoardState, move: Move) -> BoardState:
        """Apply move and return new board state."""
        # Convert to mutable grid
        new_grid = [list(row) for row in board.grid]
        from_pos_row, from_pos_col = move.from_pos
        to_pos_row, to_pos_col = move.to_pos
        
        piece = new_grid[from_pos_row][from_pos_col]
        new_grid[to_pos_row][to_pos_col] = piece
        new_grid[from_pos_row][from_pos_col] = None
        
        # Remove captured pieces
        for cap_row, cap_col in move.captures:
            new_grid[cap_row][cap_col] = None
        
        return BoardState(grid=tuple(tuple(row) for row in new_grid))
    
    def check_kinging(self, board: BoardState, move: Move) -> list[tuple[int, int]]:
        """Check if pieces reached opponent's back row."""
        kings_created = []
        to_pos_row, to_pos_col = move.to_pos
        
        # Check if piece reached opponent's back row
        piece = board.grid[to_pos_row][to_pos_col]
        if piece:
            if piece.player == Player.RED and to_pos_row == 7:
                kings_created.append((to_pos_row, to_pos_col))
            elif piece.player == Player.BLACK and to_pos_row == 0:
                kings_created.append((to_pos_row, to_pos_col))
        
        return kings_created
    
    def check_winner(self, board: BoardState) -> Player | None:
        """Check if there's a winner."""
        red_count = 0
        black_count = 0
        
        for row in board.grid:
            for piece in row:
                if piece:
                    if piece.player == Player.RED:
                        red_count += 1
                    elif piece.player == Player.BLACK:
                        black_count += 1
        
        if red_count == 0:
            return Player.BLACK
        elif black_count == 0:
            return Player.RED
        
        return None
