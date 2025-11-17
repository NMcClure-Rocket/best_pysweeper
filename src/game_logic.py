"""
Core game logic for PySweeper.
Handles board generation, mine placement, cell revealing, and game state.
"""

import random
from typing import List, Optional
from src.config import GameState


class Cell:
    """Represents a single cell in the Minesweeper grid."""

    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0

    def __repr__(self):
        return f"Cell({self.row}, {self.col}, mine={self.is_mine})"


class MinesweeperGame:
    """Main game logic controller."""

    def __init__(self, rows: int, cols: int, num_mines: int):
        """
        Initialize a new Minesweeper game.

        Args:
            rows: Number of rows in the grid
            cols: Number of columns in the grid
            num_mines: Number of mines to place
        """
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self.board: List[List[Cell]] = []
        self.state = GameState.READY
        self.mines_placed = False
        self.flags_placed = 0
        self.cells_revealed = 0

        self._initialize_board()

    def _initialize_board(self):
        """Create the game board with cells."""
        self.board = [
            [Cell(row, col) for col in range(self.cols)]
            for row in range(self.rows)
        ]

    def place_mines(self, safe_row: int, safe_col: int):
        """
        Place mines on the board, avoiding the first clicked cell and its neighbors.

        Args:
            safe_row: Row of the safe cell (first click)
            safe_col: Column of the safe cell (first click)
        """
        if self.mines_placed:
            return

        # Get safe cells (first click + neighbors)
        safe_cells = set()
        safe_cells.add((safe_row, safe_col))
        for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            nr, nc = safe_row + dr, safe_col + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                safe_cells.add((nr, nc))

        # Get all possible mine positions
        all_positions = [
            (r, c) for r in range(self.rows) for c in range(self.cols)
            if (r, c) not in safe_cells
        ]

        # Place mines randomly
        mine_positions = random.sample(all_positions, min(self.num_mines, len(all_positions)))

        for row, col in mine_positions:
            self.board[row][col].is_mine = True

        # Calculate adjacent mine counts
        self._calculate_adjacent_mines()
        self.mines_placed = True
        self.state = GameState.PLAYING

    def _calculate_adjacent_mines(self):
        """Calculate the number of adjacent mines for each cell."""
        for row in range(self.rows):
            for col in range(self.cols):
                if not self.board[row][col].is_mine:
                    count = 0
                    for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < self.rows and 0 <= nc < self.cols:
                            if self.board[nr][nc].is_mine:
                                count += 1
                    self.board[row][col].adjacent_mines = count

    def reveal_cell(self, row: int, col: int) -> bool:
        """
        Reveal a cell and handle game logic.

        Args:
            row: Row of the cell to reveal
            col: Column of the cell to reveal

        Returns:
            True if the game continues, False if a mine was hit
        """
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return True

        cell = self.board[row][col]

        # Can't reveal flagged or already revealed cells
        if cell.is_flagged or cell.is_revealed:
            return True

        # First click - place mines
        if not self.mines_placed:
            self.place_mines(row, col)

        # Reveal the cell
        cell.is_revealed = True
        self.cells_revealed += 1

        # Check if mine was hit
        if cell.is_mine:
            self.state = GameState.LOST
            self._reveal_all_mines()
            return False

        # If cell has no adjacent mines, reveal neighbors recursively
        if cell.adjacent_mines == 0:
            self._reveal_neighbors(row, col)

        # Check for win condition
        self._check_win()

        return True

    def _reveal_neighbors(self, row: int, col: int):
        """Recursively reveal neighboring cells when a cell with 0 adjacent mines is revealed."""
        for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                neighbor = self.board[nr][nc]
                if not neighbor.is_revealed and not neighbor.is_flagged and not neighbor.is_mine:
                    neighbor.is_revealed = True
                    self.cells_revealed += 1
                    if neighbor.adjacent_mines == 0:
                        self._reveal_neighbors(nr, nc)

    def _reveal_all_mines(self):
        """Reveal all mines (called when game is lost)."""
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col].is_mine:
                    self.board[row][col].is_revealed = True

    def toggle_flag(self, row: int, col: int):
        """
        Toggle flag on a cell.

        Args:
            row: Row of the cell
            col: Column of the cell
        """
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return

        cell = self.board[row][col]

        # Can't flag revealed cells
        if cell.is_revealed:
            return

        if cell.is_flagged:
            cell.is_flagged = False
            self.flags_placed -= 1
        else:
            cell.is_flagged = True
            self.flags_placed += 1

    def chord_click(self, row: int, col: int) -> bool:
        """
        Chord click - reveal all non-flagged neighbors if flags match the number.
        This is called when clicking on an already revealed cell.

        Args:
            row: Row of the cell
            col: Column of the cell

        Returns:
            True if the game continues, False if a mine was hit
        """
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return True

        cell = self.board[row][col]

        # Can only chord on revealed cells with adjacent mines
        if not cell.is_revealed or cell.adjacent_mines == 0:
            return True

        # Count adjacent flags
        adjacent_flags = 0
        for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                if self.board[nr][nc].is_flagged:
                    adjacent_flags += 1

        # Only chord if flags match the number
        if adjacent_flags != cell.adjacent_mines:
            return True

        # Reveal all non-flagged neighbors
        for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                neighbor = self.board[nr][nc]
                if not neighbor.is_revealed and not neighbor.is_flagged:
                    success = self.reveal_cell(nr, nc)
                    if not success:
                        return False

        return True

    def _check_win(self):
        """Check if the player has won the game."""
        # Win condition: all non-mine cells are revealed
        total_cells = self.rows * self.cols
        cells_to_reveal = total_cells - self.num_mines

        if self.cells_revealed >= cells_to_reveal:
            self.state = GameState.WON
            # Auto-flag remaining mines
            for row in range(self.rows):
                for col in range(self.cols):
                    if self.board[row][col].is_mine and not self.board[row][col].is_flagged:
                        self.board[row][col].is_flagged = True

    def get_cell(self, row: int, col: int) -> Optional[Cell]:
        """
        Get a cell at the specified position.

        Args:
            row: Row index
            col: Column index

        Returns:
            Cell object or None if out of bounds
        """
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.board[row][col]
        return None

    def get_remaining_mines(self) -> int:
        """Get the number of remaining mines (total mines - flags placed)."""
        return self.num_mines - self.flags_placed

    def reset(self):
        """Reset the game to initial state."""
        self._initialize_board()
        self.state = GameState.READY
        self.mines_placed = False
        self.flags_placed = 0
        self.cells_revealed = 0
