"""Leaderboard system with persistence."""

import json
import os
from datetime import datetime
from typing import List, Dict


class LeaderboardEntry:
    """Single entry in the leaderboard."""

    def __init__(self, player_name: str, wins: int = 0, losses: int = 0, ties: int = 0):
        self.player_name = player_name
        self.wins = wins
        self.losses = losses
        self.ties = ties
        self.last_played = datetime.now().isoformat()

    @property
    def total_games(self) -> int:
        """Total number of games played."""
        return self.wins + self.losses + self.ties

    @property
    def win_rate(self) -> float:
        """Calculate win rate as a percentage."""
        if self.total_games == 0:
            return 0.0
        return (self.wins / self.total_games) * 100

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "player_name": self.player_name,
            "wins": self.wins,
            "losses": self.losses,
            "ties": self.ties,
            "last_played": self.last_played,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "LeaderboardEntry":
        """Create from dictionary."""
        entry = cls(data["player_name"], data["wins"], data["losses"], data["ties"])
        entry.last_played = data.get("last_played", datetime.now().isoformat())
        return entry


class Leaderboard:
    """Manage game leaderboard with persistence."""

    def __init__(self, data_file: str = "data/leaderboard.json"):
        self.data_file = data_file
        self.entries: Dict[str, LeaderboardEntry] = {}
        self._ensure_data_dir()
        self.load()

    def _ensure_data_dir(self):
        """Ensure the data directory exists."""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)

    def load(self):
        """Load leaderboard from file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as f:
                    data = json.load(f)
                    self.entries = {
                        name: LeaderboardEntry.from_dict(entry_data)
                        for name, entry_data in data.items()
                    }
            except (json.JSONDecodeError, KeyError):
                # If file is corrupted, start fresh
                self.entries = {}

    def save(self):
        """Save leaderboard to file."""
        data = {name: entry.to_dict() for name, entry in self.entries.items()}
        with open(self.data_file, "w") as f:
            json.dump(data, f, indent=2)

    def get_or_create_player(self, player_name: str) -> LeaderboardEntry:
        """Get existing player or create new entry."""
        if player_name not in self.entries:
            self.entries[player_name] = LeaderboardEntry(player_name)
        return self.entries[player_name]

    def record_win(self, player_name: str):
        """Record a win for a player."""
        entry = self.get_or_create_player(player_name)
        entry.wins += 1
        entry.last_played = datetime.now().isoformat()
        self.save()

    def record_loss(self, player_name: str):
        """Record a loss for a player."""
        entry = self.get_or_create_player(player_name)
        entry.losses += 1
        entry.last_played = datetime.now().isoformat()
        self.save()

    def record_tie(self, player_name: str):
        """Record a tie for a player."""
        entry = self.get_or_create_player(player_name)
        entry.ties += 1
        entry.last_played = datetime.now().isoformat()
        self.save()

    def get_top_players(self, limit: int = 10) -> List[LeaderboardEntry]:
        """Get top players sorted by wins, then win rate."""
        sorted_entries = sorted(
            self.entries.values(), key=lambda e: (e.wins, e.win_rate), reverse=True
        )
        return sorted_entries[:limit]

    def get_player_stats(self, player_name: str) -> LeaderboardEntry:
        """Get stats for a specific player."""
        return self.get_or_create_player(player_name)
