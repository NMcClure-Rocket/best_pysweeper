"""
Leaderboard management for Minesweeper.
Handles saving and loading high scores to/from a JSON file.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from src.config import MAX_LEADERBOARD_ENTRIES, LEADERBOARD_FILE


class LeaderboardEntry:
    """Represents a single leaderboard entry."""

    def __init__(self, player: str, time: float, difficulty: str,
                 rows: int, cols: int, mines: int, date: Optional[str] = None):
        """
        Create a leaderboard entry.

        Args:
            player: Player name/initials
            time: Time in seconds
            difficulty: Difficulty level name
            rows: Board rows
            cols: Board columns
            mines: Number of mines
            date: Date string (ISO format), auto-generated if not provided
        """
        self.player = player
        self.time = time
        self.difficulty = difficulty
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.date = date or datetime.now().isoformat()

    def to_dict(self) -> Dict:
        """Convert entry to dictionary for JSON serialization."""
        return {
            'player': self.player,
            'time': self.time,
            'difficulty': self.difficulty,
            'rows': self.rows,
            'cols': self.cols,
            'mines': self.mines,
            'date': self.date
        }

    @staticmethod
    def from_dict(data: Dict) -> 'LeaderboardEntry':
        """Create entry from dictionary."""
        return LeaderboardEntry(
            player=data['player'],
            time=data['time'],
            difficulty=data['difficulty'],
            rows=data['rows'],
            cols=data['cols'],
            mines=data['mines'],
            date=data.get('date', '')
        )

    def format_time(self) -> str:
        """Format time as minutes and seconds."""
        minutes = int(self.time // 60)
        seconds = int(self.time % 60)
        if minutes > 0:
            return f"{minutes} minute{'s' if minutes != 1 else ''} {seconds} second{'s' if seconds != 1 else ''}"
        else:
            return f"{seconds} second{'s' if seconds != 1 else ''}"


class Leaderboard:
    """Manages the game leaderboard."""

    def __init__(self, filepath: str = LEADERBOARD_FILE):
        """
        Initialize the leaderboard.

        Args:
            filepath: Path to the JSON file storing leaderboard data
        """
        self.filepath = filepath
        self.entries: Dict[str, List[LeaderboardEntry]] = {}
        self._ensure_data_directory()
        self.load()

    def _ensure_data_directory(self):
        """Ensure the data directory exists."""
        directory = os.path.dirname(self.filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

    def _get_difficulty_key(self, difficulty: str, rows: int, cols: int, mines: int) -> str:
        """Generate a unique key for a difficulty configuration."""
        return f"{difficulty}_{rows}x{cols}_{mines}"

    def add_entry(self, entry: LeaderboardEntry) -> bool:
        """
        Add an entry to the leaderboard.

        Args:
            entry: LeaderboardEntry to add

        Returns:
            True if entry was added (made it to top MAX_LEADERBOARD_ENTRIES), False otherwise
        """
        key = self._get_difficulty_key(entry.difficulty, entry.rows, entry.cols, entry.mines)

        if key not in self.entries:
            self.entries[key] = []

        # Add entry and sort by time (ascending)
        self.entries[key].append(entry)
        self.entries[key].sort(key=lambda e: e.time)

        # Keep only top entries
        made_it = len(self.entries[key]) <= MAX_LEADERBOARD_ENTRIES or \
                  entry in self.entries[key][:MAX_LEADERBOARD_ENTRIES]

        self.entries[key] = self.entries[key][:MAX_LEADERBOARD_ENTRIES]

        self.save()
        return made_it

    def get_entries(self, difficulty: str, rows: int, cols: int, mines: int) -> List[LeaderboardEntry]:
        """
        Get leaderboard entries for a specific difficulty.

        Args:
            difficulty: Difficulty level name
            rows: Board rows
            cols: Board columns
            mines: Number of mines

        Returns:
            List of LeaderboardEntry objects, sorted by time
        """
        key = self._get_difficulty_key(difficulty, rows, cols, mines)
        return self.entries.get(key, [])

    def is_high_score(self, time: float, difficulty: str, rows: int, cols: int, mines: int) -> bool:
        """
        Check if a time qualifies as a high score.

        Args:
            time: Time in seconds
            difficulty: Difficulty level name
            rows: Board rows
            cols: Board columns
            mines: Number of mines

        Returns:
            True if the time qualifies for the leaderboard
        """
        entries = self.get_entries(difficulty, rows, cols, mines)

        if len(entries) < MAX_LEADERBOARD_ENTRIES:
            return True

        return time < entries[-1].time

    def save(self):
        """Save leaderboard to JSON file."""
        data = {}
        for key, entries in self.entries.items():
            data[key] = [entry.to_dict() for entry in entries]

        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except (IOError, OSError) as e:
            print(f"Error saving leaderboard: {e}")

    def load(self):
        """Load leaderboard from JSON file."""
        if not os.path.exists(self.filepath):
            return

        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.entries = {}
            for key, entries_data in data.items():
                self.entries[key] = [LeaderboardEntry.from_dict(e) for e in entries_data]
        except (IOError, OSError, json.JSONDecodeError) as e:
            print(f"Error loading leaderboard: {e}")
            self.entries = {}
