"""Runtime orchestration for the Checkers game."""

from src.types import BoardState, Move, Player
from src.repo import InMemoryBoardRepository
from src.service import validate_move, apply_move, check_winner, get_valid_moves
from src.providers.move_parser import parse_move


class CheckersGame:
    """Main game controller."""
    
    def __init__(self):
        self.board = InMemoryBoardRepository().get_initial_board()
        self.current_player = Player.RED
        self.game_over = False
        self.winner = None
        self.move_history: list[Move] = []
    
    def switch_turn(self):
        """Switch to the other player."""
        self.current_player = Player.BLACK if self.current_player == Player.RED else Player.RED
    
    def try_move(self, move: Move) -> bool:
        """Attempt to make a move. Returns True if successful."""
        if self.game_over:
            return False
        
        if not validate_move(self.board, move, self.current_player):
            return False
        
        self.board = apply_move(self.board, move)
        self.move_history.append(move)
        
        # Check for winner
        self.winner = check_winner(self.board)
        if self.winner:
            self.game_over = True
        
        self.switch_turn()
        return True
    
    def get_valid_moves_for_current_player(self) -> list[Move]:
        """Get all valid moves for current player."""
        return get_valid_moves(self.board, self.current_player)
    
    def is_valid_move(self, move: Move) -> bool:
        """Check if a move is valid for current player."""
        return validate_move(self.board, move, self.current_player)
    
    def get_state(self) -> str:
        """Get current game state as string."""
        pieces = {
            Player.RED: 0,
            Player.BLACK: 0
        }
        for row in self.board.grid:
            for piece in row:
                if piece:
                    pieces[piece.player] += 1
        
        state = f"Current player: {self.current_player.value}"
        state += f"\nRed pieces: {pieces[Player.RED]}, Black pieces: {pieces[Player.BLACK]}"
        
        if self.game_over:
            state += f"\nWinner: {self.winner.value.upper()}"
        
        return state


def run_game_loop():
    """Run the interactive game loop."""
    game = CheckersGame()
    repo = InMemoryBoardRepository()
    
    # Initial display
    print("Welcome to Checkers!")
    print_game_state(game.board, game.current_player)
    
    while not game.game_over:
        print(f"\n{game.current_player.value.upper()}'s turn")
        
        valid_moves = game.get_valid_moves_for_current_player()
        
        if not valid_moves:
            print(f"No valid moves for {game.current_player.value}. Game over!")
            winner = Player.BLACK if game.current_player == Player.RED else Player.RED
            print(f"Winner: {winner.value.upper()}")
            break
        
        print(f"Valid moves: {len(valid_moves)}")
        
        # Get user input
        notation = input("Enter move (e.g., 'a1-b2' or 'a1 x c3'): ").strip()
        
        if notation.lower() in ('quit', 'exit', 'q'):
            print("Game cancelled.")
            break
        
        try:
            move = parse_move(notation)
            if game.try_move(move):
                print(f"Move: {notation}")
                print_game_state(game.board, game.current_player)
                
                if game.game_over:
                    print(f"\nWinner: {game.winner.value.upper()}")
            else:
                print("Invalid move. Try again.")
        except ValueError as e:
            print(f"Error: {e}. Try again.")
    
    print("\nGame over. Thanks for playing!")


def print_game_state(board: BoardState, current_player: Player):
    """Display the current board state."""
    print("\n  a b c d e f g h")
    print(" +-----------------+")
    
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
        print(line)
    
    print(" +-----------------+")
