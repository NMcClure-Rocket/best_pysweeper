"""
PySweeper Game - Main Entry Point
A classic Minesweeper game with GUI and leaderboard support.
"""

import tkinter as tk
import sys
import os

# Add src directory to path if needed
if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.gui_new import MainMenu, MinesweeperGUI


def main():
    """Main function to run the game."""
    root = tk.Tk()
    
    # Configure window
    root.resizable(True, True)
    
    # Function to start game from menu
    def start_game(difficulty_key, difficulty):
        MinesweeperGUI(root, difficulty_key, difficulty)
    
    # Show main menu
    MainMenu(root, start_game)
    
    # Start the GUI event loop
    root.mainloop()


if __name__ == '__main__':
    main()
