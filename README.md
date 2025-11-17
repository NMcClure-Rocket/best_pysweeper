# PySweeper Game

A classic Minesweeper game implementation in Python with a modern GUI, customizable themes, and local leaderboard system.

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Tests](https://github.com/NMcClure-Rocket/best_pysweeper/workflows/Tests/badge.svg)
![Pylint](https://github.com/NMcClure-Rocket/best_pysweeper/workflows/Pylint/badge.svg)
![Coverage](https://img.shields.io/badge/coverage-98%25-brightgreen.svg)

## Features

- **Classic Minesweeper**: Left-click to reveal, right-click to flag
- **Chord Clicking**: Click revealed numbers to auto-reveal neighbors when flags match
- **Multiple Difficulties**: Beginner, Intermediate, Expert, plus Custom mode
- **5 Color Themes**: Classic, Dark, Ocean, Forest, and High Contrast
- **Fullscreen Support**: Press F11 for immersive gameplay
- **Local Leaderboard**: Top 10 times saved for each difficulty
- **Smart Scaling**: Automatically adjusts to your screen size
- **Safe First Click**: Guaranteed safe first move

## Quick Start

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/NMcClure-Rocket/best_pysweeper.git
   cd best_pysweeper
   ```

2. **Install dependencies** (optional - only needed for development):
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game**:
   ```bash
   python main.py
   ```

### Requirements

- Python 3.8 or higher
- tkinter (usually included with Python)

#### Installing tkinter (if needed)

- **Windows/macOS**: Already included with Python
- **Linux**:
  ```bash
  # Ubuntu/Debian
  sudo apt-get install python3-tk
  
  # Fedora/RHEL
  sudo yum install python3-tkinter
  ```

## How to Play

### Main Menu
- **Select Difficulty**: Choose Beginner (9×9), Intermediate (16×16), or Expert (16×30)
- **Custom Game**: Create your own board size (5-30 rows × 5-50 cols) and mine count
- **Settings**: Change color themes
- **View Leaderboard**: See top scores for each difficulty

### Game Controls
- **Left Click**: Reveal a cell
- **Right Click**: Place/remove a flag
- **Chord Click**: Left-click a revealed number to auto-reveal neighbors (when adjacent flags match the number)
- **F11**: Toggle fullscreen mode
- **Escape**: Exit fullscreen

### Gameplay Tips
1. **Numbers** indicate how many mines are adjacent (including diagonals)
2. **Flag cells** you think contain mines (right-click)
3. **Chord clicking**: Once you've flagged all mines around a number, click the number to reveal remaining neighbors
4. **First click is always safe** - mines are placed after your first move
5. **Empty cells** (no adjacent mines) automatically reveal surrounding cells

### Winning
Reveal all non-mine cells to win! Your time is recorded if you make the top 10 leaderboard.

## Color Themes

Switch themes in the Settings menu:

- **Classic** - Traditional Windows Minesweeper style
- **Dark** - Easy on the eyes for long sessions
- **Ocean** - Calming blue and aqua tones
- **Forest** - Natural green and earthy colors
- **High Contrast** - Maximum visibility

## Leaderboard

- Top 10 times saved for each difficulty configuration
- Separate leaderboards for different board sizes
- Stored locally in `data/leaderboard.json`
- Enter your name (up to 10 characters) when you make the board!

---

## For Developers

### Project Structure

```
best_pysweeper/
├── main.py                  # Entry point
├── src/                     # Source code
│   ├── config.py           # Configuration & themes
│   ├── game_logic.py       # Core game engine
│   ├── leaderboard.py      # Score management
│   └── gui_new.py          # GUI implementation
├── tests/                   # Test suite (98% coverage)
│   ├── test_config.py
│   ├── test_game_logic.py
│   ├── test_leaderboard.py
│   └── test_main.py
├── .github/workflows/       # CI/CD pipelines
├── requirements.txt         # Dependencies
└── pyproject.toml          # Project config
```

### Architecture

**Modular Design** for easy maintenance and testing:

- **`config.py`**: Centralized configuration, color themes, difficulty settings
- **`game_logic.py`**: Pure game logic with `Cell` and `MinesweeperGame` classes (GUI-independent)
- **`leaderboard.py`**: JSON-based score persistence with `LeaderboardEntry` and `Leaderboard` classes
- **`gui_new.py`**: Tkinter-based UI with `MainMenu`, `MinesweeperGUI`, and dialog classes

### Testing

```bash
# Run all tests (67 tests)
pytest

# Run with coverage report (98% coverage)
pytest --cov

# View HTML coverage report
pytest --cov --cov-report=html
# Open htmlcov/index.html in browser
```

### Code Quality

```bash
# Run pylint (score > 8.0 required)
pylint src/

# Check specific file
pylint src/game_logic.py
```

### CI/CD

GitHub Actions automatically runs on push/PR:
- Tests on Ubuntu, Windows, macOS
- Python 3.8-3.12 compatibility
- >95% test coverage requirement
- Pylint score >8.0 requirement

### Customization

#### Adding New Themes

Edit `src/config.py` and add to `COLOR_THEMES`:

```python
COLOR_THEMES = {
    'mytheme': {
        'background': '#1a1a1a',
        'cell_revealed': '#2d2d2d',
        'cell_hidden': '#3a3a3a',
        'cell_border': '#4a4a4a',
        'text': '#ffffff',
        'flag': '#ff0000',
        'mine': '#ff0000',
        'header_bg': '#0d0d0d',
        'header_text': '#ffffff',
        # Add colors for numbers 1-8
        'num_1': '#0000ff',
        # ... etc
    }
}
```

#### Modifying Difficulties

Edit `src/config.py`:

```python
DIFFICULTIES = {
    'beginner': Difficulty(name='Beginner', rows=9, cols=9, mines=10),
    'mydifficulty': Difficulty(name='Insane', rows=25, cols=50, mines=200),
}
```

#### Adjusting UI Scaling

Modify constants in `src/config.py`:

```python
MIN_CELL_SIZE = 20  # Minimum cell size (pixels)
MAX_CELL_SIZE = 40  # Maximum cell size (pixels)
CELL_SIZE = 30      # Default cell size
```

## Troubleshooting

**Game doesn't start**:
- Verify Python 3.8+: `python --version`
- Test tkinter: `python -m tkinter`
- Check tkinter installation (see Requirements section)

**Leaderboard not saving**:
- Ensure write permissions in project directory
- Verify `data/` folder can be created

**Tests failing**:
- Install test dependencies: `pip install -r requirements.txt`
- Ensure Python 3.8 or higher

**Performance issues**:
- Use smaller board sizes
- Try a different color theme
- Disable fullscreen mode

## License

MIT License - see project for details

## Author

**NM** - [NMcClure-Rocket](https://github.com/NMcClure-Rocket)

## Contributing

Contributions welcome! 

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Run tests: `pytest`
5. Commit changes (`git commit -m 'Add AmazingFeature'`)
6. Push to branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

Please ensure:
- All tests pass
- Coverage remains >95%
- Pylint score >8.0
- Code follows existing style

---

**Enjoy playing Minesweeper!** 💣🚩
