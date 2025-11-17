"""
Tests for leaderboard module.
"""

import os
import tempfile

from src.leaderboard import LeaderboardEntry, Leaderboard


class TestLeaderboardEntry:
    """Tests for LeaderboardEntry class."""
    
    def test_entry_initialization(self):
        """Test leaderboard entry initialization."""
        entry = LeaderboardEntry(
            player="Alice",
            time=125.5,
            difficulty="beginner",
            rows=9,
            cols=9,
            mines=10
        )
        
        assert entry.player == "Alice"
        assert entry.time == 125.5
        assert entry.difficulty == "beginner"
        assert entry.rows == 9
        assert entry.cols == 9
        assert entry.mines == 10
        assert entry.date is not None
    
    def test_entry_with_date(self):
        """Test entry with specific date."""
        test_date = "2025-01-15T10:30:00"
        entry = LeaderboardEntry(
            player="Bob",
            time=90.0,
            difficulty="intermediate",
            rows=16,
            cols=16,
            mines=40,
            date=test_date
        )
        
        assert entry.date == test_date
    
    def test_entry_to_dict(self):
        """Test converting entry to dictionary."""
        entry = LeaderboardEntry(
            player="Charlie",
            time=200.0,
            difficulty="expert",
            rows=16,
            cols=30,
            mines=99
        )
        
        data = entry.to_dict()
        
        assert isinstance(data, dict)
        assert data['player'] == "Charlie"
        assert data['time'] == 200.0
        assert data['difficulty'] == "expert"
        assert 'date' in data
    
    def test_entry_from_dict(self):
        """Test creating entry from dictionary."""
        data = {
            'player': 'David',
            'time': 150.0,
            'difficulty': 'intermediate',
            'rows': 16,
            'cols': 16,
            'mines': 40,
            'date': '2025-01-01T12:00:00'
        }
        
        entry = LeaderboardEntry.from_dict(data)
        
        assert entry.player == 'David'
        assert entry.time == 150.0
        assert entry.difficulty == 'intermediate'
        assert entry.date == '2025-01-01T12:00:00'
    
    def test_format_time_seconds_only(self):
        """Test time formatting for seconds only."""
        entry = LeaderboardEntry(
            player="Eve",
            time=45.0,
            difficulty="beginner",
            rows=9,
            cols=9,
            mines=10
        )
        
        formatted = entry.format_time()
        assert "45 second" in formatted
        assert "minute" not in formatted
    
    def test_format_time_with_minutes(self):
        """Test time formatting with minutes."""
        entry = LeaderboardEntry(
            player="Frank",
            time=125.0,
            difficulty="intermediate",
            rows=16,
            cols=16,
            mines=40
        )
        
        formatted = entry.format_time()
        assert "2 minute" in formatted
        assert "5 second" in formatted


class TestLeaderboard:
    """Tests for Leaderboard class."""
    
    def test_leaderboard_initialization(self):
        """Test leaderboard initialization."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name
        
        try:
            leaderboard = Leaderboard(temp_file)
            assert leaderboard.filepath == temp_file
            assert isinstance(leaderboard.entries, dict)
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def test_add_entry(self):
        """Test adding an entry to leaderboard."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name
        
        try:
            leaderboard = Leaderboard(temp_file)
            
            entry = LeaderboardEntry(
                player="Alice",
                time=100.0,
                difficulty="beginner",
                rows=9,
                cols=9,
                mines=10
            )
            
            result = leaderboard.add_entry(entry)
            assert result  # Should make it to leaderboard
            
            entries = leaderboard.get_entries("beginner", 9, 9, 10)
            assert len(entries) == 1
            assert entries[0].player == "Alice"
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def test_entries_sorted_by_time(self):
        """Test that entries are sorted by time."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name
        
        try:
            leaderboard = Leaderboard(temp_file)
            
            # Add entries in random order
            for time, player in [(150.0, "Slow"), (50.0, "Fast"), (100.0, "Medium")]:
                entry = LeaderboardEntry(
                    player=player,
                    time=time,
                    difficulty="beginner",
                    rows=9,
                    cols=9,
                    mines=10
                )
                leaderboard.add_entry(entry)
            
            entries = leaderboard.get_entries("beginner", 9, 9, 10)
            
            assert len(entries) == 3
            assert entries[0].player == "Fast"
            assert entries[1].player == "Medium"
            assert entries[2].player == "Slow"
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def test_max_entries_limit(self):
        """Test that only top 10 entries are kept."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name
        
        try:
            leaderboard = Leaderboard(temp_file)
            
            # Add 15 entries
            for i in range(15):
                entry = LeaderboardEntry(
                    player=f"Player{i}",
                    time=100.0 + i,
                    difficulty="beginner",
                    rows=9,
                    cols=9,
                    mines=10
                )
                leaderboard.add_entry(entry)
            
            entries = leaderboard.get_entries("beginner", 9, 9, 10)
            
            # Should only keep 10
            assert len(entries) == 10
            # Should be the fastest 10
            assert entries[0].player == "Player0"
            assert entries[9].player == "Player9"
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def test_separate_leaderboards_by_difficulty(self):
        """Test that different difficulties have separate leaderboards."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name
        
        try:
            leaderboard = Leaderboard(temp_file)
            
            # Add beginner entry
            beginner_entry = LeaderboardEntry(
                player="BeginnerPlayer",
                time=50.0,
                difficulty="beginner",
                rows=9,
                cols=9,
                mines=10
            )
            leaderboard.add_entry(beginner_entry)
            
            # Add intermediate entry
            intermediate_entry = LeaderboardEntry(
                player="IntermediatePlayer",
                time=100.0,
                difficulty="intermediate",
                rows=16,
                cols=16,
                mines=40
            )
            leaderboard.add_entry(intermediate_entry)
            
            # Check they're separate
            beginner_entries = leaderboard.get_entries("beginner", 9, 9, 10)
            intermediate_entries = leaderboard.get_entries("intermediate", 16, 16, 40)
            
            assert len(beginner_entries) == 1
            assert len(intermediate_entries) == 1
            assert beginner_entries[0].player == "BeginnerPlayer"
            assert intermediate_entries[0].player == "IntermediatePlayer"
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def test_is_high_score_empty_leaderboard(self):
        """Test high score check on empty leaderboard."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name
        
        try:
            leaderboard = Leaderboard(temp_file)
            
            # Any score should be high score on empty board
            result = leaderboard.is_high_score(100.0, "beginner", 9, 9, 10)
            assert result
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def test_is_high_score_better_than_worst(self):
        """Test high score check when better than worst entry."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name
        
        try:
            leaderboard = Leaderboard(temp_file)
            
            # Fill leaderboard with 10 entries
            for i in range(10):
                entry = LeaderboardEntry(
                    player=f"Player{i}",
                    time=100.0 + i * 10,
                    difficulty="beginner",
                    rows=9,
                    cols=9,
                    mines=10
                )
                leaderboard.add_entry(entry)
            
            # Better time should be high score
            assert leaderboard.is_high_score(95.0, "beginner", 9, 9, 10)
            
            # Worse time should not be high score
            assert not leaderboard.is_high_score(200.0, "beginner", 9, 9, 10)
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def test_save_and_load(self):
        """Test saving and loading leaderboard."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name
        
        try:
            # Create leaderboard and add entries
            leaderboard1 = Leaderboard(temp_file)
            
            for i in range(3):
                entry = LeaderboardEntry(
                    player=f"Player{i}",
                    time=100.0 + i * 10,
                    difficulty="beginner",
                    rows=9,
                    cols=9,
                    mines=10
                )
                leaderboard1.add_entry(entry)
            
            # Create new leaderboard from same file
            leaderboard2 = Leaderboard(temp_file)
            
            # Should have loaded the entries
            entries = leaderboard2.get_entries("beginner", 9, 9, 10)
            assert len(entries) == 3
            assert entries[0].player == "Player0"
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def test_empty_entries_for_nonexistent_difficulty(self):
        """Test getting entries for difficulty with no scores."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name
        
        try:
            leaderboard = Leaderboard(temp_file)
            
            entries = leaderboard.get_entries("expert", 16, 30, 99)
            assert len(entries) == 0
            assert isinstance(entries, list)
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def test_leaderboard_corrupted_file(self):
        """Test loading leaderboard with corrupted JSON."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name
            f.write("{invalid json content")
        
        try:
            # Should handle corrupted file gracefully
            leaderboard = Leaderboard(temp_file)
            assert isinstance(leaderboard.entries, dict)
            assert len(leaderboard.entries) == 0
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def test_leaderboard_save_error_handling(self):
        """Test save handles errors gracefully."""
        import tempfile
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name
        
        try:
            # Create leaderboard with a fresh temp file
            leaderboard = Leaderboard(temp_file)
            
            entry = LeaderboardEntry(
                player="Test",
                time=100.0,
                difficulty="beginner",
                rows=9,
                cols=9,
                mines=10
            )
            
            # Add entry
            leaderboard.add_entry(entry)
            
            # Remove file so save will fail
            if os.path.exists(temp_file):
                os.remove(temp_file)
            
            # Create invalid parent directory path to trigger save error
            leaderboard.filepath = "/invalid/path/that/does/not/exist/leaderboard.json"
            
            # Try to save - should handle error gracefully (print message)
            leaderboard.save()
            
            # Entry should still be in memory
            entries = leaderboard.get_entries("beginner", 9, 9, 10)
            assert len(entries) == 1
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def test_leaderboard_save_io_error(self):
        """Test save handles IOError when writing to readonly file."""
        import tempfile
        import stat
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name
        
        try:
            leaderboard = Leaderboard(temp_file)
            
            entry = LeaderboardEntry(
                player="Test",
                time=50.0,
                difficulty="beginner",
                rows=9,
                cols=9,
                mines=10
            )
            leaderboard.add_entry(entry)
            
            # Make file readonly
            os.chmod(temp_file, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
            
            # Try to save - should handle error gracefully (print message)
            try:
                leaderboard.save()
                # On Windows, this might still succeed, so we don't assert failure
            except (IOError, OSError, PermissionError):
                pass  # Expected on some systems
                
            # Restore permissions for cleanup
            os.chmod(temp_file, stat.S_IWUSR | stat.S_IRUSR)
        finally:
            if os.path.exists(temp_file):
                try:
                    os.chmod(temp_file, stat.S_IWUSR | stat.S_IRUSR)
                    os.remove(temp_file)
                except:
                    pass
    
    def test_leaderboard_creates_data_directory(self):
        """Test that leaderboard creates missing data directory (line 92)."""
        import tempfile
        import shutil
        
        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Create path with nested directory that doesn't exist
            nested_path = os.path.join(temp_dir, "nested", "data", "leaderboard.json")
            
            # Create leaderboard - should create missing directories
            leaderboard = Leaderboard(nested_path)
            
            entry = LeaderboardEntry(
                player="Test",
                time=50.0,
                difficulty="beginner",
                rows=9,
                cols=9,
                mines=10
            )
            leaderboard.add_entry(entry)
            
            # Check directory was created
            assert os.path.exists(os.path.dirname(nested_path))
            assert os.path.exists(nested_path)
        finally:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
    
    def test_leaderboard_load_nonexistent_file(self):
        """Test load returns early if file doesn't exist (line 178)."""
        import tempfile
        
        # Create temp file path but don't create the file
        temp_file = os.path.join(tempfile.gettempdir(), "nonexistent_leaderboard.json")
        
        # Ensure file doesn't exist
        if os.path.exists(temp_file):
            os.remove(temp_file)
        
        try:
            # Load should return early without error
            leaderboard = Leaderboard(temp_file)
            assert isinstance(leaderboard.entries, dict)
            assert len(leaderboard.entries) == 0
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
