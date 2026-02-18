# Setup and Testing Instructions

## Quick Start

1. Install dependencies:

   ```bash
   pip3 install -r requirements.txt
   ```

   Or if you prefer using a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   pip install -r requirements.txt
   ```

2. Run the game:
   ```bash
   python3 play.py
   ```

## Testing the Features

### 1. Test AI Gameplay

- Select option 1 from the main menu
- Enter your name
- Choose an AI opponent (try all 4!)
- Play a few rounds to see different AI strategies

### 2. Test Local Multiplayer

- Select option 2 from the main menu
- Enter Player 1's name
- Enter Player 2's name
- Play rounds (players take turns choosing)

### 3. Test Leaderboard

- Play a few games first
- Select option 3 from the main menu
- View the leaderboard with rankings

### 4. Test Player Stats

- Select option 4 from the main menu
- View your personal statistics

## AI Opponents

1. **Randy Random** (Easy) - Makes completely random moves
2. **Cyclone Cathy** (Easy) - Cycles through Rock → Paper → Scissors
3. **Pattern Pete** (Medium) - Analyzes your move history and counters your most common move
4. **Adaptive Ada** (Hard) - Learns which moves work best and uses them more often

## Data Persistence

- Leaderboard data is saved in `data/leaderboard.json`
- Data persists between game sessions
- You can view/edit the JSON file directly if needed

## Troubleshooting

If you get import errors:

```bash
pip3 install --upgrade rich
```

If the game doesn't display colors/emojis properly, ensure your terminal supports UTF-8 and emojis.
