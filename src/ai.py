"""AI opponents with different strategies and personalities."""

import random
from typing import List
from src.game import Move


class AIPlayer:
    """Base class for AI players."""

    def __init__(self, name: str, personality: str):
        self.name = name
        self.personality = personality
        self.move_history: List[Move] = []

    def make_move(self, opponent_history: List[Move]) -> Move:
        """Make a move based on AI strategy."""
        raise NotImplementedError

    def record_move(self, move: Move):
        """Record a move to history."""
        self.move_history.append(move)


class RandomAI(AIPlayer):
    """AI that makes random moves."""

    def make_move(self, opponent_history: List[Move]) -> Move:
        return random.choice(list(Move))


class PatternAI(AIPlayer):
    """AI that tries to detect patterns in opponent's moves."""

    def make_move(self, opponent_history: List[Move]) -> Move:
        if len(opponent_history) < 2:
            return random.choice(list(Move))

        # Look for the most common opponent move
        move_counts = {move: opponent_history.count(move) for move in Move}
        most_common = max(move_counts.keys(), key=lambda m: move_counts[m])

        # Counter the most common move
        counters = {
            Move.ROCK: Move.PAPER,
            Move.PAPER: Move.SCISSORS,
            Move.SCISSORS: Move.ROCK,
        }
        return counters[most_common]


class CycleAI(AIPlayer):
    """AI that cycles through moves predictably."""

    def __init__(self, name: str, personality: str):
        super().__init__(name, personality)
        self.cycle = [Move.ROCK, Move.PAPER, Move.SCISSORS]
        self.index = 0

    def make_move(self, opponent_history: List[Move]) -> Move:
        move = self.cycle[self.index]
        self.index = (self.index + 1) % len(self.cycle)
        return move


class AdaptiveAI(AIPlayer):
    """AI that adapts based on opponent patterns and adjusts strategy dynamically."""

    def __init__(self, name: str, personality: str):
        super().__init__(name, personality)
        self.wins_by_move = {Move.ROCK: 0, Move.PAPER: 0, Move.SCISSORS: 0}
        self.losses_by_move = {Move.ROCK: 0, Move.PAPER: 0, Move.SCISSORS: 0}

    def make_move(self, opponent_history: List[Move]) -> Move:
        # Early game: random exploration
        if len(opponent_history) < 3:
            return random.choice(list(Move))

        # Analyze opponent's recent pattern (last 5-10 moves)
        recent_window = min(10, len(opponent_history))
        recent_moves = opponent_history[-recent_window:]

        # Count opponent's recent moves
        move_counts = {move: recent_moves.count(move) for move in Move}

        # Find opponent's most frequent recent move
        most_common = max(move_counts.keys(), key=lambda m: move_counts[m])

        # Counter map
        counters = {
            Move.ROCK: Move.PAPER,
            Move.PAPER: Move.SCISSORS,
            Move.SCISSORS: Move.ROCK,
        }

        # Calculate success rate for each move
        success_rates = {}
        for move in Move:
            total_uses = self.wins_by_move[move] + self.losses_by_move[move]
            if total_uses > 0:
                success_rates[move] = self.wins_by_move[move] / total_uses
            else:
                success_rates[move] = 0.5  # Neutral for unused moves

        # Strategy: 70% counter opponent's pattern, 30% use best performing move
        if random.random() < 0.7:
            # Counter the opponent's most common recent move
            return counters[most_common]
        else:
            # Use move with best historical success rate
            best_move = max(success_rates.keys(), key=lambda m: success_rates[m])
            # Add randomization if success rates are similar (within 10%)
            if max(success_rates.values()) - min(success_rates.values()) < 0.1:
                return random.choice(list(Move))
            return best_move

    def record_win(self, winning_move: Move):
        """Record a winning move to adjust strategy."""
        self.wins_by_move[winning_move] += 1

    def record_loss(self, losing_move: Move):
        """Record a losing move to avoid it."""
        self.losses_by_move[losing_move] += 1


# AI opponents with personalities
AI_OPPONENTS: List[dict] = [
    {
        "class": RandomAI,
        "name": "Randy Random",
        "personality": "Chaotic and unpredictable! I just go with my gut feeling.",
        "difficulty": "Easy",
    },
    {
        "class": CycleAI,
        "name": "Cyclone Cathy",
        "personality": "I like patterns and predictability... or do I?",
        "difficulty": "Easy",
    },
    {
        "class": PatternAI,
        "name": "Pattern Pete",
        "personality": "I'm always watching, learning your every move!",
        "difficulty": "Medium",
    },
    {
        "class": AdaptiveAI,
        "name": "Adaptive Ada",
        "personality": "I learn from my mistakes and adapt to crush you!",
        "difficulty": "Hard",
    },
]


def create_ai(ai_index: int) -> AIPlayer:
    """Create an AI opponent by index."""
    ai_config = AI_OPPONENTS[ai_index]
    ai_class = ai_config["class"]
    return ai_class(ai_config["name"], ai_config["personality"])
