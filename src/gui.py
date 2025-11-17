"""
GUI module for PySweeper using tkinter.
Creates the game interface matching the provided design.
"""

import tkinter as tk
from tkinter import simpledialog, messagebox
import time
from typing import Optional, Callable

from src.config import (
    DIFFICULTIES, DEFAULT_DIFFICULTY, CELL_SIZE, HEADER_HEIGHT, PADDING,
    COLORS, CELL_BG_COLORS, GameState, FONT_FAMILY, FONT_SIZE_CELL,
    FONT_SIZE_HEADER, FONT_SIZE_BUTTON
)
from src.game_logic import MinesweeperGame
from src.leaderboard import Leaderboard, LeaderboardEntry


class MinesweeperGUI:
    """Main GUI class for PySweeper."""

    def __init__(self, root: tk.Tk):
        """
        Initialize the GUI.

        Args:
            root: The root tkinter window
        """
        self.root = root
        self.root.title("Mines")

        # Game state
        self.difficulty_name = DEFAULT_DIFFICULTY
        self.difficulty = DIFFICULTIES[self.difficulty_name]
        self.game: Optional[MinesweeperGame] = None
        self.leaderboard = Leaderboard()

        # Timer state
        self.start_time: Optional[float] = None
        self.elapsed_time = 0
        self.timer_running = False
        self.timer_id: Optional[str] = None

        # UI elements
        self.buttons = []
        self.mine_counter_label: Optional[tk.Label] = None
        self.timer_label: Optional[tk.Label] = None
        self.reset_button: Optional[tk.Button] = None

        self._create_ui()
        self._new_game()

    def _create_ui(self):
        """Create the user interface."""
        # Main container
        self.main_frame = tk.Frame(self.root, bg=COLORS['background'])
        self.main_frame.pack(padx=PADDING, pady=PADDING)

        # Header
        self._create_header()

        # Game board
        self._create_board()

        # Footer with buttons
        self._create_footer()

        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _create_header(self):
        """Create the header with mine counter, reset button, and timer."""
        header = tk.Frame(self.main_frame, bg=COLORS['header'], height=HEADER_HEIGHT)
        header.pack(fill=tk.X, pady=(0, PADDING))

        # Mine counter (left)
        mine_frame = tk.Frame(header, bg=COLORS['header'])
        mine_frame.pack(side=tk.LEFT, padx=PADDING, pady=PADDING)

        tk.Label(mine_frame, text="🚩", font=(FONT_FAMILY, FONT_SIZE_HEADER),
                bg=COLORS['header']).pack(side=tk.LEFT)
        self.mine_counter_label = tk.Label(
            mine_frame, text="99/99", font=(FONT_FAMILY, FONT_SIZE_HEADER, 'bold'),
            bg=COLORS['header'], fg=COLORS['text']
        )
        self.mine_counter_label.pack(side=tk.LEFT, padx=(5, 0))

        # Reset button (center)
        self.reset_button = tk.Button(
            header, text="🚩", font=(FONT_FAMILY, 20),
            command=self._new_game, relief=tk.RAISED,
            bg=COLORS['button'], activebackground=COLORS['button_hover']
        )
        self.reset_button.pack(side=tk.LEFT, expand=True)

        # Timer (right)
        timer_frame = tk.Frame(header, bg=COLORS['header'])
        timer_frame.pack(side=tk.RIGHT, padx=PADDING, pady=PADDING)

        tk.Label(timer_frame, text="⏱", font=(FONT_FAMILY, FONT_SIZE_HEADER),
                bg=COLORS['header']).pack(side=tk.LEFT)
        self.timer_label = tk.Label(
            timer_frame, text="00:00", font=(FONT_FAMILY, FONT_SIZE_HEADER, 'bold'),
            bg=COLORS['header'], fg=COLORS['text']
        )
        self.timer_label.pack(side=tk.LEFT, padx=(5, 0))

    def _create_board(self):
        """Create the game board grid."""
        self.board_frame = tk.Frame(self.main_frame, bg=COLORS['background'])
        self.board_frame.pack()

    def _create_footer(self):
        """Create footer with action buttons."""
        footer = tk.Frame(self.main_frame, bg=COLORS['background'])
        footer.pack(fill=tk.X, pady=(PADDING, 0))

        # Play Again button
        tk.Button(
            footer, text="Play Again", font=(FONT_FAMILY, FONT_SIZE_BUTTON),
            command=self._new_game, bg=COLORS['button'],
            activebackground=COLORS['button_hover'], width=15
        ).pack(side=tk.TOP, pady=2)

        # Best Times button
        tk.Button(
            footer, text="Best Times", font=(FONT_FAMILY, FONT_SIZE_BUTTON),
            command=self._show_leaderboard, bg=COLORS['button'],
            activebackground=COLORS['button_hover'], width=15
        ).pack(side=tk.TOP, pady=2)

        # Change Difficulty button
        tk.Button(
            footer, text="Change Difficulty", font=(FONT_FAMILY, FONT_SIZE_BUTTON),
            command=self._change_difficulty, bg=COLORS['button'],
            activebackground=COLORS['button_hover'], width=15
        ).pack(side=tk.TOP, pady=2)

    def _create_board_buttons(self):
        """Create the grid of buttons for the game board."""
        # Clear existing buttons
        for widget in self.board_frame.winfo_children():
            widget.destroy()
        self.buttons = []

        # Create new buttons
        for row in range(self.difficulty.rows):
            button_row = []
            for col in range(self.difficulty.cols):
                btn = tk.Button(
                    self.board_frame,
                    width=2,
                    height=1,
                    font=(FONT_FAMILY, FONT_SIZE_CELL, 'bold'),
                    bg=COLORS['cell_hidden'],
                    relief=tk.RAISED,
                    bd=2
                )
                btn.grid(row=row, column=col, padx=1, pady=1)

                # Bind click events
                btn.bind('<Button-1>', lambda e, r=row, c=col: self._on_left_click(r, c))
                btn.bind('<Button-3>', lambda e, r=row, c=col: self._on_right_click(r, c))

                button_row.append(btn)
            self.buttons.append(button_row)

    def _new_game(self):
        """Start a new game."""
        self._stop_timer()
        self.game = MinesweeperGame(
            self.difficulty.rows,
            self.difficulty.cols,
            self.difficulty.mines
        )
        self._create_board_buttons()
        self._update_mine_counter()
        self._reset_timer()
        self._update_reset_button('🚩')

    def _on_left_click(self, row: int, col: int):
        """
        Handle left click on a cell.

        Args:
            row: Row of the clicked cell
            col: Column of the clicked cell
        """
        if self.game.state not in [GameState.READY, GameState.PLAYING]:
            return

        # Start timer on first click
        if self.game.state == GameState.READY:
            self._start_timer()

        # Reveal cell
        success = self.game.reveal_cell(row, col)
        self._update_board()

        if not success:
            # Game lost
            self._stop_timer()
            self._update_reset_button('💀')
            messagebox.showinfo("Game Over", "You hit a mine! Game Over.")
        elif self.game.state == GameState.WON:
            # Game won
            self._stop_timer()
            self._update_reset_button('😎')
            self._handle_win()

    def _on_right_click(self, row: int, col: int):
        """
        Handle right click on a cell (toggle flag).

        Args:
            row: Row of the clicked cell
            col: Column of the clicked cell
        """
        if self.game.state not in [GameState.READY, GameState.PLAYING]:
            return

        self.game.toggle_flag(row, col)
        self._update_board()
        self._update_mine_counter()

    def _update_board(self):
        """Update the visual state of all cells."""
        for row in range(self.difficulty.rows):
            for col in range(self.difficulty.cols):
                cell = self.game.get_cell(row, col)
                btn = self.buttons[row][col]

                if cell.is_revealed:
                    btn.config(relief=tk.SUNKEN)
                    if cell.is_mine:
                        btn.config(text='💣', bg=COLORS['cell_mine'], fg=COLORS['text'])
                    elif cell.adjacent_mines > 0:
                        # Get background color based on number
                        bg_color = CELL_BG_COLORS.get(cell.adjacent_mines, COLORS['cell_revealed'])
                        text_color = COLORS.get(f'cell_{cell.adjacent_mines}', COLORS['text'])
                        btn.config(
                            text=str(cell.adjacent_mines),
                            bg=bg_color,
                            fg=text_color
                        )
                    else:
                        btn.config(text='', bg=COLORS['cell_revealed'])
                elif cell.is_flagged:
                    btn.config(text='🚩', bg=COLORS['cell_flag'], relief=tk.RAISED)
                else:
                    btn.config(text='', bg=COLORS['cell_hidden'], relief=tk.RAISED)

    def _update_mine_counter(self):
        """Update the mine counter display."""
        remaining = self.game.get_remaining_mines()
        total = self.game.num_mines
        self.mine_counter_label.config(text=f"{remaining}/{total}")

    def _start_timer(self):
        """Start the game timer."""
        self.start_time = time.time()
        self.timer_running = True
        self._update_timer()

    def _stop_timer(self):
        """Stop the game timer."""
        self.timer_running = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

        if self.start_time:
            self.elapsed_time = time.time() - self.start_time

    def _reset_timer(self):
        """Reset the timer to 00:00."""
        self.start_time = None
        self.elapsed_time = 0
        self.timer_running = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        self.timer_label.config(text="00:00")

    def _update_timer(self):
        """Update the timer display."""
        if self.timer_running and self.start_time:
            elapsed = int(time.time() - self.start_time)
            minutes = elapsed // 60
            seconds = elapsed % 60
            self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
            self.timer_id = self.root.after(100, self._update_timer)

    def _update_reset_button(self, emoji: str):
        """Update the reset button emoji."""
        self.reset_button.config(text=emoji)

    def _handle_win(self):
        """Handle game win - check for high score and show congratulations."""
        # Check if it's a high score
        is_high_score = self.leaderboard.is_high_score(
            self.elapsed_time,
            self.difficulty_name,
            self.difficulty.rows,
            self.difficulty.cols,
            self.difficulty.mines
        )

        if is_high_score:
            # Ask for player name
            player_name = simpledialog.askstring(
                "Congratulations!",
                f"You won in {self._format_time(self.elapsed_time)}!\n\n"
                "You made the leaderboard! Enter your name:",
                initialvalue="NM"
            )

            if player_name:
                entry = LeaderboardEntry(
                    player=player_name[:10],  # Limit name length
                    time=self.elapsed_time,
                    difficulty=self.difficulty_name,
                    rows=self.difficulty.rows,
                    cols=self.difficulty.cols,
                    mines=self.difficulty.mines
                )
                self.leaderboard.add_entry(entry)
                messagebox.showinfo(
                    "High Score!",
                    f"Congratulations {player_name}!\n\n"
                    f"Your time: {self._format_time(self.elapsed_time)}"
                )
        else:
            messagebox.showinfo(
                "Congratulations!",
                f"You won in {self._format_time(self.elapsed_time)}!"
            )

    def _format_time(self, seconds: float) -> str:
        """Format time in seconds to mm:ss format."""
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins:02d}:{secs:02d}"

    def _show_leaderboard(self):
        """Show the leaderboard window."""
        LeaderboardWindow(self.root, self.leaderboard, self.difficulty_name,
                         self.difficulty.rows, self.difficulty.cols, self.difficulty.mines)

    def _change_difficulty(self):
        """Show difficulty selection dialog."""
        DifficultyDialog(self.root, self._on_difficulty_changed, self.difficulty_name)

    def _on_difficulty_changed(self, difficulty_name: str):
        """
        Handle difficulty change.

        Args:
            difficulty_name: Name of the new difficulty
        """
        self.difficulty_name = difficulty_name
        self.difficulty = DIFFICULTIES[difficulty_name]
        self._new_game()

    def _on_closing(self):
        """Handle window close event."""
        self._stop_timer()
        self.root.destroy()


class LeaderboardWindow:
    """Window to display the leaderboard."""

    def __init__(self, parent: tk.Tk, leaderboard: Leaderboard,
                 difficulty: str, rows: int, cols: int, mines: int):
        """
        Create a leaderboard window.

        Args:
            parent: Parent window
            leaderboard: Leaderboard object
            difficulty: Current difficulty name
            rows: Board rows
            cols: Board columns
            mines: Number of mines
        """
        self.window = tk.Toplevel(parent)
        self.window.title("Best Times")
        self.window.geometry("400x400")

        # Title
        difficulty_obj = DIFFICULTIES.get(difficulty)
        title_text = f"Minefield:  {rows} × {cols}, {mines} mines"
        tk.Label(
            self.window, text=title_text,
            font=(FONT_FAMILY, 12, 'bold'),
            pady=10
        ).pack()

        # Separator
        tk.Frame(self.window, height=2, bg='gray').pack(fill=tk.X, padx=20)

        # Leaderboard entries
        entries = leaderboard.get_entries(difficulty, rows, cols, mines)

        if entries:
            # Create table-like layout
            table_frame = tk.Frame(self.window)
            table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

            # Headers
            tk.Label(table_frame, text="Rank", font=(FONT_FAMILY, 10, 'bold'),
                    width=8).grid(row=0, column=0, sticky='w', pady=5)
            tk.Label(table_frame, text="Time", font=(FONT_FAMILY, 10, 'bold'),
                    width=20).grid(row=0, column=1, sticky='w', pady=5)
            tk.Label(table_frame, text="Player", font=(FONT_FAMILY, 10, 'bold'),
                    width=15).grid(row=0, column=2, sticky='w', pady=5)

            # Entries
            for i, entry in enumerate(entries, 1):
                tk.Label(table_frame, text=str(i), font=(FONT_FAMILY, 10),
                        width=8).grid(row=i, column=0, sticky='w', pady=2)
                tk.Label(table_frame, text=entry.format_time(), font=(FONT_FAMILY, 10),
                        width=20).grid(row=i, column=1, sticky='w', pady=2)
                tk.Label(table_frame, text=entry.player, font=(FONT_FAMILY, 10),
                        width=15).grid(row=i, column=2, sticky='w', pady=2)
        else:
            tk.Label(
                self.window,
                text="No scores yet!\n\nPlay a game to set a record.",
                font=(FONT_FAMILY, 11),
                pady=50
            ).pack()

        # Close button
        tk.Button(
            self.window, text="Close", command=self.window.destroy,
            font=(FONT_FAMILY, 10), width=10, bg=COLORS['button']
        ).pack(pady=10)


class DifficultyDialog:
    """Dialog for selecting game difficulty."""

    def __init__(self, parent: tk.Tk, callback: Callable[[str], None],
                 current_difficulty: str):
        """
        Create a difficulty selection dialog.

        Args:
            parent: Parent window
            callback: Function to call with selected difficulty
            current_difficulty: Currently selected difficulty
        """
        self.window = tk.Toplevel(parent)
        self.window.title("Change Difficulty")
        self.window.geometry("300x200")
        self.callback = callback

        tk.Label(
            self.window,
            text="Select Difficulty:",
            font=(FONT_FAMILY, 12, 'bold'),
            pady=10
        ).pack()

        # Radio buttons for each difficulty
        self.selected = tk.StringVar(value=current_difficulty)

        for key, diff in DIFFICULTIES.items():
            rb = tk.Radiobutton(
                self.window,
                text=f"{diff.name} ({diff.rows}×{diff.cols}, {diff.mines} mines)",
                variable=self.selected,
                value=key,
                font=(FONT_FAMILY, 10),
                pady=5
            )
            rb.pack(anchor=tk.W, padx=30)

        # OK button
        tk.Button(
            self.window,
            text="OK",
            command=self._on_ok,
            font=(FONT_FAMILY, 10),
            width=10,
            bg=COLORS['button']
        ).pack(pady=15)

    def _on_ok(self):
        """Handle OK button click."""
        self.callback(self.selected.get())
        self.window.destroy()
