"""
Configuration module for Minesweeper game.
Defines difficulty levels, colors, and game constants.
"""

from dataclasses import dataclass

@dataclass
class Difficulty:
    """Represents a game difficulty setting."""
    name: str
    rows: int
    cols: int
    mines: int

    def __str__(self):
        return f"{self.name}: {self.rows} × {self.cols}, {self.mines} mines"


# Predefined difficulty levels
DIFFICULTIES = {
    'beginner': Difficulty(name='Beginner', rows=9, cols=9, mines=10),
    'intermediate': Difficulty(name='Intermediate', rows=16, cols=16, mines=40),
    'expert': Difficulty(name='Expert', rows=16, cols=30, mines=99),
}

# Default difficulty
DEFAULT_DIFFICULTY = 'intermediate'

# UI Configuration
CELL_SIZE = 30  # Size of each cell in pixels
HEADER_HEIGHT = 60  # Height of the header section
PADDING = 10  # Padding around elements
MAX_CELL_SIZE = 40  # Maximum cell size for scaling
MIN_CELL_SIZE = 20  # Minimum cell size for scaling

# Color Themes
COLOR_THEMES = {
    'classic': {
        'background': '#FFFFFF',
        'cell_revealed': '#E0E0E0',
        'cell_hidden': '#C0C0C0',
        'cell_flag': '#FFA500',
        'cell_mine': '#808080',
        'cell_1': '#0000FF',
        'cell_2': '#008000',
        'cell_3': '#FF0000',
        'cell_4': '#000080',
        'cell_5': '#800000',
        'cell_6': '#008080',
        'cell_7': '#000000',
        'cell_8': '#808080',
        'button': '#F0F0F0',
        'button_hover': '#E0E0E0',
        'text': '#000000',
        'header': '#F5F5F5',
        'cell_bg_0': '#E0E0E0',
        'cell_bg_1': '#C8F4C8',
        'cell_bg_2': '#FFFACD',
        'cell_bg_3': '#FFD4A3',
        'cell_bg_4': '#FFB380',
        'cell_bg_5': '#FFB3BA',
    },
    'dark': {
        'background': '#1E1E1E',
        'cell_revealed': '#2D2D30',
        'cell_hidden': '#3E3E42',
        'cell_flag': '#FF6B35',
        'cell_mine': '#5A5A5F',
        'cell_1': '#569CD6',
        'cell_2': '#4EC9B0',
        'cell_3': '#CE9178',
        'cell_4': '#9CDCFE',
        'cell_5': '#C586C0',
        'cell_6': '#4FC1FF',
        'cell_7': '#DCDCAA',
        'cell_8': '#D4D4D4',
        'button': '#333337',
        'button_hover': '#3E3E42',
        'text': '#CCCCCC',
        'header': '#252526',
        'cell_bg_0': '#2D2D30',
        'cell_bg_1': '#1A3A1A',
        'cell_bg_2': '#3A3A1A',
        'cell_bg_3': '#3A2A1A',
        'cell_bg_4': '#3A1A1A',
        'cell_bg_5': '#3A1A2A',
    },
    'ocean': {
        'background': '#E8F4F8',
        'cell_revealed': '#B8D8E8',
        'cell_hidden': '#7FB3D5',
        'cell_flag': '#FF6B6B',
        'cell_mine': '#34495E',
        'cell_1': '#2C3E50',
        'cell_2': '#16A085',
        'cell_3': '#E74C3C',
        'cell_4': '#2980B9',
        'cell_5': '#8E44AD',
        'cell_6': '#27AE60',
        'cell_7': '#C0392B',
        'cell_8': '#7F8C8D',
        'button': '#AED6F1',
        'button_hover': '#85C1E9',
        'text': '#1C2833',
        'header': '#D6EAF8',
        'cell_bg_0': '#B8D8E8',
        'cell_bg_1': '#A3E4D7',
        'cell_bg_2': '#F9E79F',
        'cell_bg_3': '#FAD7A0',
        'cell_bg_4': '#F5B7B1',
        'cell_bg_5': '#D7BDE2',
    },
    'forest': {
        'background': '#F0F5E8',
        'cell_revealed': '#D5E8D4',
        'cell_hidden': '#A8D5A0',
        'cell_flag': '#FF6B35',
        'cell_mine': '#5D4E37',
        'cell_1': '#2D5016',
        'cell_2': '#228B22',
        'cell_3': '#DC143C',
        'cell_4': '#4B0082',
        'cell_5': '#8B4513',
        'cell_6': '#006400',
        'cell_7': '#000000',
        'cell_8': '#696969',
        'button': '#C8E6C9',
        'button_hover': '#A5D6A7',
        'text': '#1B5E20',
        'header': '#E8F5E9',
        'cell_bg_0': '#D5E8D4',
        'cell_bg_1': '#C8E6C9',
        'cell_bg_2': '#FFF9C4',
        'cell_bg_3': '#FFE082',
        'cell_bg_4': '#FFCC80',
        'cell_bg_5': '#FFAB91',
    },
    'high_contrast': {
        'background': '#FFFFFF',
        'cell_revealed': '#FFFFFF',
        'cell_hidden': '#000000',
        'cell_flag': '#FF0000',
        'cell_mine': '#000000',
        'cell_1': '#0000FF',
        'cell_2': '#008000',
        'cell_3': '#FF0000',
        'cell_4': '#000080',
        'cell_5': '#800000',
        'cell_6': '#008080',
        'cell_7': '#000000',
        'cell_8': '#808080',
        'button': '#EEEEEE',
        'button_hover': '#CCCCCC',
        'text': '#000000',
        'header': '#F0F0F0',
        'cell_bg_0': '#FFFFFF',
        'cell_bg_1': '#E0FFE0',
        'cell_bg_2': '#FFFFE0',
        'cell_bg_3': '#FFE0C0',
        'cell_bg_4': '#FFC0A0',
        'cell_bg_5': '#FFA0A0',
    },
}

# Default theme
DEFAULT_THEME = 'classic'
CURRENT_THEME = DEFAULT_THEME

# Active colors (will be set from theme)
COLORS = COLOR_THEMES[DEFAULT_THEME].copy()

# Cell background colors by number (for backward compatibility)
CELL_BG_COLORS = {
    0: COLORS['cell_bg_0'],
    1: COLORS['cell_bg_1'],
    2: COLORS['cell_bg_2'],
    3: COLORS['cell_bg_3'],
    4: COLORS['cell_bg_4'],
    5: COLORS['cell_bg_5'],
}

def set_theme(theme_name: str):
    """Set the active color theme. Updates COLORS dict in place."""
    global CURRENT_THEME
    if theme_name in COLOR_THEMES:
        CURRENT_THEME = theme_name
        # Update existing dicts in place rather than replacing them
        COLORS.clear()
        COLORS.update(COLOR_THEMES[theme_name])

        # Update cell background colors
        CELL_BG_COLORS[0] = COLORS['cell_bg_0']
        CELL_BG_COLORS[1] = COLORS['cell_bg_1']
        CELL_BG_COLORS[2] = COLORS['cell_bg_2']
        CELL_BG_COLORS[3] = COLORS['cell_bg_3']
        CELL_BG_COLORS[4] = COLORS['cell_bg_4']
        CELL_BG_COLORS[5] = COLORS['cell_bg_5']

# Game states
class GameState:
    """Enum-like class for game states."""
    READY = 'ready'
    PLAYING = 'playing'
    WON = 'won'
    LOST = 'lost'

# Leaderboard configuration
MAX_LEADERBOARD_ENTRIES = 10
LEADERBOARD_FILE = 'data/leaderboard.json'

# Fonts
FONT_FAMILY = 'Arial'
FONT_SIZE_CELL = 14
FONT_SIZE_HEADER = 12
FONT_SIZE_BUTTON = 10
