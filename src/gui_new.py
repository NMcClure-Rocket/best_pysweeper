"""
GUI module for PySweeper using tkinter.
Enhanced with main menu, custom mode, settings, and improved scaling.
"""

import tkinter as tk
from tkinter import simpledialog, messagebox
import time
from typing import Optional, Callable

from src.config import (
    DIFFICULTIES, HEADER_HEIGHT, PADDING,
    COLORS, CELL_BG_COLORS, GameState, FONT_FAMILY, FONT_SIZE_CELL,
    FONT_SIZE_HEADER, FONT_SIZE_BUTTON,
    MAX_CELL_SIZE, MIN_CELL_SIZE, set_theme, Difficulty
)
from src.game_logic import MinesweeperGame
from src.leaderboard import Leaderboard, LeaderboardEntry


class MainMenu:
    """Main menu screen for PySweeper."""

    def __init__(self, root: tk.Tk, on_start_game: Callable):
        """
        Initialize the main menu.

        Args:
            root: The root tkinter window
            on_start_game: Callback function when starting a game
        """
        self.root = root
        self.on_start_game = on_start_game
        self.root.title("Minesweeper - Main Menu")

        self.frame = tk.Frame(root, bg=COLORS['background'], padx=50, pady=50)
        self.frame.pack(expand=True, fill=tk.BOTH)

        self._create_menu()

    def _create_menu(self):
        """Create the main menu interface."""
        # Title
        title = tk.Label(
            self.frame,
            text="PySweeper",
            font=(FONT_FAMILY, 32, 'bold'),
            bg=COLORS['background'],
            fg=COLORS['text']
        )
        title.pack(pady=(20, 40))

        # Difficulty buttons
        tk.Label(
            self.frame,
            text="Select Difficulty:",
            font=(FONT_FAMILY, 14, 'bold'),
            bg=COLORS['background'],
            fg=COLORS['text']
        ).pack(pady=(0, 10))

        for key, diff in DIFFICULTIES.items():
            btn = tk.Button(
                self.frame,
                text=f"{diff.name}\n{diff.rows}×{diff.cols}, {diff.mines} mines",
                font=(FONT_FAMILY, 12),
                width=25,
                height=2,
                command=lambda k=key: self._start_difficulty(k),
                bg=COLORS['button'],
                activebackground=COLORS['button_hover']
            )
            btn.pack(pady=5)

        # Custom mode button
        custom_btn = tk.Button(
            self.frame,
            text="Custom Game",
            font=(FONT_FAMILY, 12),
            width=25,
            height=2,
            command=self._custom_mode,
            bg=COLORS['button'],
            activebackground=COLORS['button_hover']
        )
        custom_btn.pack(pady=(15, 5))

        # Settings button
        settings_btn = tk.Button(
            self.frame,
            text="Settings",
            font=(FONT_FAMILY, 12),
            width=25,
            height=2,
            command=self._show_settings,
            bg=COLORS['button'],
            activebackground=COLORS['button_hover']
        )
        settings_btn.pack(pady=5)

        # Quit button
        quit_btn = tk.Button(
            self.frame,
            text="Quit",
            font=(FONT_FAMILY, 12),
            width=25,
            height=2,
            command=self.root.quit,
            bg=COLORS['button'],
            activebackground=COLORS['button_hover']
        )
        quit_btn.pack(pady=(15, 5))

    def _start_difficulty(self, difficulty_key: str):
        """Start a game with the selected difficulty."""
        self.frame.destroy()
        self.on_start_game(difficulty_key, DIFFICULTIES[difficulty_key])

    def _custom_mode(self):
        """Show custom game dialog."""
        CustomGameDialog(self.root, self._start_custom_game)

    def _start_custom_game(self, rows: int, cols: int, mines: int):
        """Start a custom game."""
        custom_diff = Difficulty(name='Custom', rows=rows, cols=cols, mines=mines)
        self.frame.destroy()
        self.on_start_game('custom', custom_diff)

    def _show_settings(self):
        """Show settings dialog."""
        SettingsDialog(self.root, self._on_settings_changed)

    def _on_settings_changed(self):
        """Handle settings changes - refresh menu colors."""
        self.frame.destroy()
        self.frame = tk.Frame(self.root, bg=COLORS['background'], padx=50, pady=50)
        self.frame.pack(expand=True, fill=tk.BOTH)
        self._create_menu()


class CustomGameDialog:
    """Dialog for creating a custom game."""

    def __init__(self, parent: tk.Tk, callback: Callable[[int, int, int], None]):
        """
        Create a custom game dialog.

        Args:
            parent: Parent window
            callback: Function to call with (rows, cols, mines)
        """
        self.window = tk.Toplevel(parent)
        self.window.title("Custom Game")
        self.window.geometry("350x250")
        self.window.configure(bg=COLORS['background'])
        self.callback = callback

        tk.Label(
            self.window,
            text="Custom Game Setup",
            font=(FONT_FAMILY, 14, 'bold'),
            bg=COLORS['background'],
            fg=COLORS['text'],
            pady=10
        ).pack()

        # Rows input
        row_frame = tk.Frame(self.window, bg=COLORS['background'])
        row_frame.pack(pady=5)
        tk.Label(row_frame, text="Rows (5-30):", font=(FONT_FAMILY, 11),
                bg=COLORS['background'], fg=COLORS['text'], width=15, anchor='w').pack(side=tk.LEFT)
        self.rows_var = tk.StringVar(value="16")
        tk.Entry(row_frame, textvariable=self.rows_var, width=10,
                font=(FONT_FAMILY, 11)).pack(side=tk.LEFT)

        # Columns input
        col_frame = tk.Frame(self.window, bg=COLORS['background'])
        col_frame.pack(pady=5)
        tk.Label(col_frame, text="Columns (5-50):", font=(FONT_FAMILY, 11),
                bg=COLORS['background'], fg=COLORS['text'], width=15, anchor='w').pack(side=tk.LEFT)
        self.cols_var = tk.StringVar(value="16")
        tk.Entry(col_frame, textvariable=self.cols_var, width=10,
                font=(FONT_FAMILY, 11)).pack(side=tk.LEFT)

        # Mines input
        mine_frame = tk.Frame(self.window, bg=COLORS['background'])
        mine_frame.pack(pady=5)
        tk.Label(mine_frame, text="Mines:", font=(FONT_FAMILY, 11),
                bg=COLORS['background'], fg=COLORS['text'], width=15, anchor='w').pack(side=tk.LEFT)
        self.mines_var = tk.StringVar(value="40")
        tk.Entry(mine_frame, textvariable=self.mines_var, width=10,
                font=(FONT_FAMILY, 11)).pack(side=tk.LEFT)

        # Buttons
        btn_frame = tk.Frame(self.window, bg=COLORS['background'])
        btn_frame.pack(pady=20)

        tk.Button(
            btn_frame,
            text="Start Game",
            command=self._on_ok,
            font=(FONT_FAMILY, 11),
            width=12,
            bg=COLORS['button'],
            activebackground=COLORS['button_hover']
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame,
            text="Cancel",
            command=self.window.destroy,
            font=(FONT_FAMILY, 11),
            width=12,
            bg=COLORS['button'],
            activebackground=COLORS['button_hover']
        ).pack(side=tk.LEFT, padx=5)

    def _on_ok(self):
        """Validate and start the custom game."""
        try:
            rows = int(self.rows_var.get())
            cols = int(self.cols_var.get())
            mines = int(self.mines_var.get())

            if not (5 <= rows <= 30):
                messagebox.showerror("Invalid Input", "Rows must be between 5 and 30")
                return

            if not (5 <= cols <= 50):
                messagebox.showerror("Invalid Input", "Columns must be between 5 and 50")
                return

            max_mines = (rows * cols) - 9  # Leave room for first click safety
            if not (1 <= mines <= max_mines):
                messagebox.showerror("Invalid Input",
                                   f"Mines must be between 1 and {max_mines}")
                return

            self.window.destroy()
            self.callback(rows, cols, mines)

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers")


class SettingsDialog:
    """Dialog for game settings."""

    def __init__(self, parent: tk.Tk, callback: Callable):
        """
        Create a settings dialog.

        Args:
            parent: Parent window
            callback: Function to call when settings change
        """
        self.window = tk.Toplevel(parent)
        self.window.title("Settings")
        self.window.geometry("400x350")
        self.window.configure(bg=COLORS['background'])
        self.callback = callback

        tk.Label(
            self.window,
            text="Settings",
            font=(FONT_FAMILY, 16, 'bold'),
            bg=COLORS['background'],
            fg=COLORS['text'],
            pady=15
        ).pack()

        # Color theme selection
        tk.Label(
            self.window,
            text="Color Theme:",
            font=(FONT_FAMILY, 12, 'bold'),
            bg=COLORS['background'],
            fg=COLORS['text'],
            pady=10
        ).pack()

        # Get current theme
        from src.config import CURRENT_THEME
        self.selected_theme = tk.StringVar(value=CURRENT_THEME)

        # Create radio buttons for themes
        theme_descriptions = {
            'classic': 'Classic - Traditional Windows style',
            'dark': 'Dark - Easy on the eyes',
            'ocean': 'Ocean - Blue and aqua tones',
            'forest': 'Forest - Green and earthy tones',
            'high_contrast': 'High Contrast - Maximum visibility'
        }

        for theme_key, description in theme_descriptions.items():
            rb = tk.Radiobutton(
                self.window,
                text=description,
                variable=self.selected_theme,
                value=theme_key,
                font=(FONT_FAMILY, 10),
                bg=COLORS['background'],
                fg=COLORS['text'],
                selectcolor=COLORS['button'],
                activebackground=COLORS['background'],
                pady=3
            )
            rb.pack(anchor=tk.W, padx=40)

        # Buttons
        btn_frame = tk.Frame(self.window, bg=COLORS['background'])
        btn_frame.pack(pady=25)

        tk.Button(
            btn_frame,
            text="Apply",
            command=self._apply_settings,
            font=(FONT_FAMILY, 11),
            width=12,
            bg=COLORS['button'],
            activebackground=COLORS['button_hover']
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame,
            text="Cancel",
            command=self.window.destroy,
            font=(FONT_FAMILY, 11),
            width=12,
            bg=COLORS['button'],
            activebackground=COLORS['button_hover']
        ).pack(side=tk.LEFT, padx=5)

    def _apply_settings(self):
        """Apply the selected settings."""
        new_theme = self.selected_theme.get()
        set_theme(new_theme)
        self.window.destroy()
        self.callback()
        messagebox.showinfo("Settings Applied",
                          "Theme changed! Restart the game for full effect.")


class MinesweeperGUI:
    """Main GUI class for Minesweeper game."""

    def __init__(self, root: tk.Tk, difficulty_key: str, difficulty: Difficulty):
        """
        Initialize the game GUI.

        Args:
            root: The root tkinter window
            difficulty_key: Key for the difficulty
            difficulty: Difficulty object
        """
        self.root = root
        self.root.title("Mines")

        # Get screen dimensions for scaling
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Game state
        self.difficulty_name = difficulty_key
        self.difficulty = difficulty
        self.game: Optional[MinesweeperGame] = None
        self.leaderboard = Leaderboard()

        # Calculate optimal cell size
        self.cell_size = self._calculate_cell_size(screen_width, screen_height)

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
        self.main_frame: Optional[tk.Frame] = None
        self.board_frame: Optional[tk.Frame] = None

        # Window state
        self.is_fullscreen = False

        self._create_ui()
        self._new_game()

        # Center window
        self._center_window()

        # Bind fullscreen toggle
        self.root.bind('<F11>', lambda e: self._toggle_fullscreen())
        self.root.bind('<Escape>', lambda e: self._exit_fullscreen())

    def _calculate_cell_size(self, screen_width: int, screen_height: int) -> int:
        """Calculate optimal cell size based on screen and board dimensions."""
        # Reserve space for UI elements
        available_width = screen_width - 100
        available_height = screen_height - 200

        # Calculate cell size based on board
        width_based = available_width // self.difficulty.cols
        height_based = available_height // self.difficulty.rows

        # Use the smaller dimension and clamp to min/max
        optimal_size = min(width_based, height_based)
        return max(MIN_CELL_SIZE, min(MAX_CELL_SIZE, optimal_size))

    def _center_window(self):
        """Center the window on screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'+{x}+{y}')

    def _toggle_fullscreen(self):
        """Toggle fullscreen mode."""
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes('-fullscreen', self.is_fullscreen)

    def _exit_fullscreen(self):
        """Exit fullscreen mode."""
        if self.is_fullscreen:
            self.is_fullscreen = False
            self.root.attributes('-fullscreen', False)

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
                bg=COLORS['header'], fg=COLORS['text']).pack(side=tk.LEFT)
        self.mine_counter_label = tk.Label(
            mine_frame, text="99/99", font=(FONT_FAMILY, FONT_SIZE_HEADER, 'bold'),
            bg=COLORS['header'], fg=COLORS['text']
        )
        self.mine_counter_label.pack(side=tk.LEFT, padx=(5, 0))

        # Reset button (center)
        self.reset_button = tk.Button(
            header, text="🚩", font=(FONT_FAMILY, 20),
            command=self._new_game, relief=tk.RAISED,
            bg=COLORS['button'], activebackground=COLORS['button_hover'],
            fg=COLORS['text']
        )
        self.reset_button.pack(side=tk.LEFT, expand=True)

        # Timer (right)
        timer_frame = tk.Frame(header, bg=COLORS['header'])
        timer_frame.pack(side=tk.RIGHT, padx=PADDING, pady=PADDING)

        tk.Label(timer_frame, text="⏱", font=(FONT_FAMILY, FONT_SIZE_HEADER),
                bg=COLORS['header'], fg=COLORS['text']).pack(side=tk.LEFT)
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

        # Main Menu button
        tk.Button(
            footer, text="Main Menu", font=(FONT_FAMILY, FONT_SIZE_BUTTON),
            command=self._return_to_menu, bg=COLORS['button'],
            activebackground=COLORS['button_hover'], fg=COLORS['text'], width=15
        ).pack(side=tk.TOP, pady=2)

        # Play Again button
        tk.Button(
            footer, text="Play Again", font=(FONT_FAMILY, FONT_SIZE_BUTTON),
            command=self._new_game, bg=COLORS['button'],
            activebackground=COLORS['button_hover'], fg=COLORS['text'], width=15
        ).pack(side=tk.TOP, pady=2)

        # Best Times button
        tk.Button(
            footer, text="Best Times", font=(FONT_FAMILY, FONT_SIZE_BUTTON),
            command=self._show_leaderboard, bg=COLORS['button'],
            activebackground=COLORS['button_hover'], fg=COLORS['text'], width=15
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
                    font=(FONT_FAMILY, min(FONT_SIZE_CELL, self.cell_size // 2), 'bold'),
                    bg=COLORS['cell_hidden'],
                    fg=COLORS['text'],
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

        cell = self.game.get_cell(row, col)

        # If cell is already revealed, try chord clicking
        if cell.is_revealed:
            if self.game.state == GameState.READY:
                return
            success = self.game.chord_click(row, col)
            self._update_board()
            if not success:
                self._stop_timer()
                self._update_reset_button('💀')
                messagebox.showinfo("Game Over", "You hit a mine! Game Over.")
            elif self.game.state == GameState.WON:
                self._stop_timer()
                self._update_reset_button('😎')
                self._handle_win()
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
                    btn.config(text='🚩', bg=COLORS['cell_flag'], fg=COLORS['text'], relief=tk.RAISED)
                else:
                    btn.config(text='', bg=COLORS['cell_hidden'], fg=COLORS['text'], relief=tk.RAISED)

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

    def _return_to_menu(self):
        """Return to main menu."""
        self._stop_timer()
        self.main_frame.destroy()
        self.root.unbind('<F11>')
        self.root.unbind('<Escape>')
        # Show main menu
        MainMenu(self.root, self._restart_with_difficulty)

    def _restart_with_difficulty(self, difficulty_key: str, difficulty: Difficulty):
        """Restart the game with a new difficulty."""
        self.difficulty_name = difficulty_key
        self.difficulty = difficulty

        # Recalculate cell size
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.cell_size = self._calculate_cell_size(screen_width, screen_height)

        # Recreate UI
        self._create_ui()
        self._new_game()
        self._center_window()

        # Re-bind fullscreen
        self.root.bind('<F11>', lambda e: self._toggle_fullscreen())
        self.root.bind('<Escape>', lambda e: self._exit_fullscreen())

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
        self.window.configure(bg=COLORS['background'])

        # Title
        title_text = f"Minefield:  {rows} × {cols}, {mines} mines"
        tk.Label(
            self.window, text=title_text,
            font=(FONT_FAMILY, 12, 'bold'),
            bg=COLORS['background'],
            fg=COLORS['text'],
            pady=10
        ).pack()

        # Separator
        tk.Frame(self.window, height=2, bg='gray').pack(fill=tk.X, padx=20)

        # Leaderboard entries
        entries = leaderboard.get_entries(difficulty, rows, cols, mines)

        if entries:
            # Create table-like layout
            table_frame = tk.Frame(self.window, bg=COLORS['background'])
            table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

            # Headers
            tk.Label(table_frame, text="Rank", font=(FONT_FAMILY, 10, 'bold'),
                    bg=COLORS['background'], fg=COLORS['text'], width=8).grid(row=0, column=0, sticky='w', pady=5)
            tk.Label(table_frame, text="Time", font=(FONT_FAMILY, 10, 'bold'),
                    bg=COLORS['background'], fg=COLORS['text'], width=20).grid(row=0, column=1, sticky='w', pady=5)
            tk.Label(table_frame, text="Player", font=(FONT_FAMILY, 10, 'bold'),
                    bg=COLORS['background'], fg=COLORS['text'], width=15).grid(row=0, column=2, sticky='w', pady=5)

            # Entries
            for i, entry in enumerate(entries, 1):
                tk.Label(table_frame, text=str(i), font=(FONT_FAMILY, 10),
                        bg=COLORS['background'], fg=COLORS['text'], width=8).grid(row=i, column=0, sticky='w', pady=2)
                tk.Label(table_frame, text=entry.format_time(), font=(FONT_FAMILY, 10),
                        bg=COLORS['background'], fg=COLORS['text'], width=20).grid(row=i, column=1, sticky='w', pady=2)
                tk.Label(table_frame, text=entry.player, font=(FONT_FAMILY, 10),
                        bg=COLORS['background'], fg=COLORS['text'], width=15).grid(row=i, column=2, sticky='w', pady=2)
        else:
            tk.Label(
                self.window,
                text="No scores yet!\n\nPlay a game to set a record.",
                font=(FONT_FAMILY, 11),
                bg=COLORS['background'],
                fg=COLORS['text'],
                pady=50
            ).pack()

        # Close button
        tk.Button(
            self.window, text="Close", command=self.window.destroy,
            font=(FONT_FAMILY, 10), width=10, bg=COLORS['button'],
            activebackground=COLORS['button_hover'], fg=COLORS['text']
        ).pack(pady=10)
