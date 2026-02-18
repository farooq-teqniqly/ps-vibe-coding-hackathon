# Team 9: The Vibe Tribe

This is Team 9's repository for the hackathon.

## Rock Paper Scissors TUI Game 🪨📄✂️

A multiplayer Rock Paper Scissors game with a beautiful Terminal User Interface (TUI) built with Python and Rich.

### Features

- 🎮 **Multiple Game Modes**
  - Play against AI opponents with different personalities and strategies
  - Local multiplayer (two humans on the same computer)
- 🤖 **AI Opponents**
  - **Randy Random** - Easy: Chaotic and unpredictable!
  - **Cyclone Cathy** - Easy: Likes patterns and predictability
  - **Pattern Pete** - Medium: Learns your patterns and counters them
  - **Adaptive Ada** - Hard: Adapts strategy based on what's working

- 🏆 **Leaderboard System**
  - Persistent leaderboard tracked across all games
  - View top players with win rates and statistics
  - Individual player stats tracking

- 🎨 **Beautiful TUI**
  - Colorful terminal interface using Rich library
  - Emoji support for moves and results
  - Animated game flow

### Installation

1. Make sure you have Python 3.7+ installed
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### How to Play

Run the game:

```bash
python play.py
```

Or make it executable and run directly:

```bash
chmod +x play.py
./play.py
```

### Game Rules

- 🪨 Rock beats ✂️ Scissors
- 📄 Paper beats 🪨 Rock
- ✂️ Scissors beats 📄 Paper

### Project Structure

```
.
├── src/
│   ├── game.py         # Core game logic
│   ├── ai.py           # AI opponents
│   ├── leaderboard.py  # Leaderboard and persistence
│   └── main.py         # TUI interface
├── data/               # Leaderboard data (created on first run)
├── play.py             # Entry point
└── requirements.txt    # Dependencies
```

### Development

Built with:

- **Python 3.x**
- **Rich** - Beautiful terminal formatting
- **JSON** - Leaderboard persistence

---

Made with ❤️ by Team 9: The Vibe Tribe
