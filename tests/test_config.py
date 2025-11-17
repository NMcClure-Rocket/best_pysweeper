"""
Tests for configuration module.
"""

from src.config import (
    Difficulty, DIFFICULTIES, COLOR_THEMES, GameState,
    set_theme, COLORS, CELL_BG_COLORS
)


class TestDifficulty:
    """Tests for Difficulty class."""
    
    def test_difficulty_creation(self):
        """Test creating a difficulty."""
        diff = Difficulty(name="Test", rows=10, cols=10, mines=15)
        assert diff.name == "Test"
        assert diff.rows == 10
        assert diff.cols == 10
        assert diff.mines == 15
    
    def test_difficulty_str(self):
        """Test difficulty string representation."""
        diff = Difficulty(name="Easy", rows=8, cols=8, mines=10)
        str_repr = str(diff)
        assert "Easy" in str_repr
        assert "8" in str_repr
        assert "10" in str_repr


class TestPredefinedDifficulties:
    """Tests for predefined difficulties."""
    
    def test_beginner_difficulty(self):
        """Test beginner difficulty settings."""
        assert 'beginner' in DIFFICULTIES
        diff = DIFFICULTIES['beginner']
        assert diff.name == 'Beginner'
        assert diff.rows == 9
        assert diff.cols == 9
        assert diff.mines == 10
    
    def test_intermediate_difficulty(self):
        """Test intermediate difficulty settings."""
        assert 'intermediate' in DIFFICULTIES
        diff = DIFFICULTIES['intermediate']
        assert diff.name == 'Intermediate'
        assert diff.rows == 16
        assert diff.cols == 16
        assert diff.mines == 40
    
    def test_expert_difficulty(self):
        """Test expert difficulty settings."""
        assert 'expert' in DIFFICULTIES
        diff = DIFFICULTIES['expert']
        assert diff.name == 'Expert'
        assert diff.rows == 16
        assert diff.cols == 30
        assert diff.mines == 99


class TestColorThemes:
    """Tests for color themes."""
    
    def test_classic_theme_exists(self):
        """Test classic theme is defined."""
        assert 'classic' in COLOR_THEMES
        theme = COLOR_THEMES['classic']
        assert 'background' in theme
        assert 'cell_hidden' in theme
        assert 'cell_revealed' in theme
    
    def test_dark_theme_exists(self):
        """Test dark theme is defined."""
        assert 'dark' in COLOR_THEMES
        theme = COLOR_THEMES['dark']
        assert 'background' in theme
        # Dark theme should have darker background
        assert theme['background'].lower().startswith('#')
    
    def test_all_themes_have_required_colors(self):
        """Test all themes have required color keys."""
        required_keys = [
            'background', 'cell_revealed', 'cell_hidden', 'cell_flag',
            'cell_mine', 'button', 'text', 'header'
        ]
        
        for theme_name, theme in COLOR_THEMES.items():
            for key in required_keys:
                assert key in theme, f"Theme {theme_name} missing {key}"
    
    def test_set_theme(self):
        """Test setting a theme."""
        set_theme('dark')
        assert COLORS['background'] == COLOR_THEMES['dark']['background']
        
        set_theme('classic')
        assert COLORS['background'] == COLOR_THEMES['classic']['background']
    
    def test_set_invalid_theme(self):
        """Test setting an invalid theme doesn't crash."""
        original_bg = COLORS['background']
        set_theme('nonexistent_theme')
        # Should not change colors
        assert COLORS['background'] == original_bg
    
    def test_cell_bg_colors_updated_with_theme(self):
        """Test that cell background colors are updated with theme."""
        set_theme('ocean')
        # CELL_BG_COLORS should be updated
        assert CELL_BG_COLORS[0] == COLOR_THEMES['ocean']['cell_bg_0']


class TestGameState:
    """Tests for GameState class."""
    
    def test_game_states_defined(self):
        """Test all game states are defined."""
        assert GameState.READY == 'ready'
        assert GameState.PLAYING == 'playing'
        assert GameState.WON == 'won'
        assert GameState.LOST == 'lost'
    
    def test_game_states_unique(self):
        """Test all game states are unique."""
        states = [GameState.READY, GameState.PLAYING, GameState.WON, GameState.LOST]
        assert len(states) == len(set(states))
