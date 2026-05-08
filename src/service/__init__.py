"""Business logic for Checkers game."""

from src.types import BoardState, Move, Piece, Player
from src.repo import BoardRepository, InMemoryBoardRepository


def get_valid_moves(board: BoardState, player: Player, repo: BoardRepository | None = None) -> list[Move]:
    """Get all valid moves for a player."""
    if repo is None:
        repo = InMemoryBoardRepository()
    
    moves = []
    
    for row in range(8):
        for col in range(8):
            piece = board.grid[row][col]
            if piece and piece.player == player:
                piece_moves = get_piece_moves(board, (row, col), player)
                moves.extend(piece_moves)
    
    return moves


def get_piece_moves(board: BoardState, pos: tuple[int, int], player: Player) -> list[Move]:
    """Get valid moves for a single piece."""
    moves = []
    row, col = pos
    piece = board.grid[row][col]
    
    if not piece:
        return moves
    
    # Determine direction(s) piece can move
    directions = []
    if piece.player == Player.RED or piece.is_king:
        directions.append((1, -1))  # down-left
        directions.append((1, 1))   # down-right
    if piece.player == Player.BLACK or piece.is_king:
        directions.append((-1, -1))  # up-left
        directions.append((-1, 1))   # up-right
    
    for dr, dc in directions:
        # Check simple move (2 squares diagonal)
        mid_row, mid_col = row + dr, col + dc
        target_row, target_col = row + 2 * dr, col + 2 * dc
        
        # Check for capture (jump over opponent)
        if 0 <= target_row < 8 and 0 <= target_col < 8:
            mid_piece = board.grid[mid_row][mid_col]
            target_piece = board.grid[target_row][target_col]
            
            if (mid_piece and 
                mid_piece.player != player and 
                target_piece is None):
                moves.append(Move(
                    from_pos=(row, col),
                    to_pos=(target_row, target_col),
                    captures=[(mid_row, mid_col)]
                ))
        
        # Check simple move (1 square diagonal) - no capture
        simple_row, simple_col = row + dr, col + dc
        if 0 <= simple_row < 8 and 0 <= simple_col < 8:
            if board.grid[simple_row][simple_col] is None:
                moves.append(Move(
                    from_pos=(row, col),
                    to_pos=(simple_row, simple_col),
                    captures=[]
                ))
    
    return moves


def validate_move(board: BoardState, move: Move, player: Player, repo: BoardRepository | None = None) -> bool:
    """Validate if a move is legal."""
    if repo is None:
        repo = InMemoryBoardRepository()
    
    # Get all valid moves for the player
    all_moves = get_valid_moves(board, player, repo)
    
    # Check if this move is in the list
    for valid_move in all_moves:
        if (valid_move.from_pos == move.from_pos and 
            valid_move.to_pos == move.to_pos and
            set(valid_move.captures) == set(move.captures)):
            return True
    
    return False


def apply_move(board: BoardState, move: Move, repo: BoardRepository | None = None) -> BoardState:
    """Apply a move to the board."""
    if repo is None:
        repo = InMemoryBoardRepository()
    
    # First apply the basic move
    new_board = repo.apply_move(board, move)
    
    # Check for kinging
    kings = repo.check_kinging(board, move)
    if kings:
        # Convert to mutable for kinging
        grid = [list(row) for row in new_board.grid]
        for row, col in kings:
            piece = grid[row][col]
            if piece:
                grid[row][col] = Piece(player=piece.player, is_king=True)
        new_board = BoardState(grid=tuple(tuple(row) for row in grid))
    
    return new_board


def check_winner(board: BoardState, repo: BoardRepository | None = None) -> Player | None:
    """Check if there's a winner."""
    if repo is None:
        repo = InMemoryBoardRepository()
    return repo.check_winner(board)
