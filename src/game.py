"""Rock Paper Scissors game logic."""

from enum import Enum


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
