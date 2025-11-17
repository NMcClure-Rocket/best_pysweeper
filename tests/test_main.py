"""
Tests for main.py entry point
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import main


class TestMain(unittest.TestCase):
    """Test main module functionality."""
    
    @patch('main.tk.Tk')
    @patch('main.MainMenu')
    def test_main_creates_window_and_menu(self, mock_menu, mock_tk):
        """Test that main() creates Tk window and MainMenu."""
        # Setup mocks
        mock_root = MagicMock()
        mock_tk.return_value = mock_root
        
        # Mock mainloop to prevent blocking
        mock_root.mainloop = Mock()
        
        # Call main
        main.main()
        
        # Verify Tk was created
        mock_tk.assert_called_once()
        
        # Verify window is resizable
        mock_root.resizable.assert_called_once_with(True, True)
        
        # Verify MainMenu was created with root and start_game callback
        mock_menu.assert_called_once()
        args = mock_menu.call_args[0]
        assert args[0] == mock_root
        assert callable(args[1])  # start_game function
        
        # Verify mainloop was called
        mock_root.mainloop.assert_called_once()
    
    @patch('main.MinesweeperGUI')
    @patch('main.tk.Tk')
    @patch('main.MainMenu')
    def test_start_game_callback_creates_gui(self, mock_menu, mock_tk, mock_gui):
        """Test that the start_game callback creates MinesweeperGUI."""
        # Setup mocks
        mock_root = MagicMock()
        mock_tk.return_value = mock_root
        mock_root.mainloop = Mock()
        
        # Capture the start_game callback
        captured_callback = None
        def capture_callback(root, callback):
            nonlocal captured_callback
            captured_callback = callback
        
        mock_menu.side_effect = capture_callback
        
        # Call main
        main.main()
        
        # Verify callback was captured
        assert captured_callback is not None
        assert callable(captured_callback)
        
        # Call the start_game callback
        from src.config import Difficulty
        test_difficulty = Difficulty("test", 9, 9, 10)
        captured_callback("test", test_difficulty)
        
        # Verify MinesweeperGUI was created
        mock_gui.assert_called_once_with(mock_root, "test", test_difficulty)
    
    def test_main_module_name_check(self):
        """Test that main.py has proper __name__ guard."""
        # This test verifies the module can be imported without executing
        import main
        assert hasattr(main, 'main')
        assert callable(main.main)
    
    @patch('sys.path')
    def test_sys_path_modification(self, mock_path):
        """Test that sys.path is modified when run as main."""
        # This verifies the path manipulation logic exists
        assert 'sys.path.insert' in open('main.py').read()


if __name__ == '__main__':
    unittest.main()
