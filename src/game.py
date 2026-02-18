"""Rock Paper Scissors game logic."""

from enum import Enum
from typing import List


class Move(Enum):
    """Possible moves in Rock Paper Scissors."""

    ROCK = "rock"
    PAPER = "paper"
    SCISSORS = "scissors"

    def __str__(self):
        return self.value.title()


class GameResult(Enum):
    """Result of a game round."""

    WIN = "win"
    LOSE = "lose"
    TIE = "tie"


class Game:
    """Core game logic for Rock Paper Scissors."""

    @staticmethod
    def determine_winner(player1_move: Move, player2_move: Move) -> GameResult:
        """
        Determine the winner of a round.

        Args:
            player1_move: Move made by player 1
            player2_move: Move made by player 2

        Returns:
            GameResult from player 1's perspective
        """
        if player1_move == player2_move:
            return GameResult.TIE

        winning_moves = {
            Move.ROCK: Move.SCISSORS,
            Move.PAPER: Move.ROCK,
            Move.SCISSORS: Move.PAPER,
        }

        if winning_moves[player1_move] == player2_move:
            return GameResult.WIN
        else:
            return GameResult.LOSE

    @staticmethod
    def get_move_emoji(move: Move) -> str:
        """Get emoji representation of a move."""
        emoji_map = {Move.ROCK: "🪨", Move.PAPER: "📄", Move.SCISSORS: "✂️"}
        return emoji_map[move]

    # ASCII art from https://gist.github.com/wynand1004/b5c521ea8392e9c6bfe101b025c39abe
    _ASCII_ROCK = r"""
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
"""
    _ASCII_PAPER = r"""
    _______
---'    ____)____
          ______)
          _______)
          _______)
---.__________)
"""
    _ASCII_SCISSORS = r"""
    _______
---'   ____)____
      (_____)
      (__________)
      (____)
---.__(___)
"""
    _ASCII_ART = {
        Move.ROCK: _ASCII_ROCK.strip(),
        Move.PAPER: _ASCII_PAPER.strip(),
        Move.SCISSORS: _ASCII_SCISSORS.strip(),
    }

    @staticmethod
    def get_move_ascii_art(move: Move) -> str:
        """Get full multi-line ASCII art for a move."""
        return Game._ASCII_ART[move]

    @staticmethod
    def get_move_ascii_art_lines(move: Move) -> List[str]:
        """Get ASCII art for a move as a list of lines (for side-by-side layout)."""
        return Game.get_move_ascii_art(move).splitlines()
