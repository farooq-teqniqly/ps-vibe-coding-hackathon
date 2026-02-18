# Team 9: The Vibe Tribe

This is Team 9's repository for the hackathon.

## Rock Paper Scissors TUI Game 🪨📄✂️

A multiplayer Rock Paper Scissors game with a beautiful Terminal User Interface (TUI) built with Python and Rich.

### Features

- 🎮 **Multiple Game Modes**
  - Play against AI opponents with different personalities and strategies
  - Local multiplayer (two humans on the same computer)
  - **AI vs AI Battle Mode** - Watch two AIs battle it out!
  - **AI Tournament Mode** - Run round-robin tournaments with multiple AIs!
- 🤖 **AI Opponents**
  - **Randy Random** - Easy: Chaotic and unpredictable!
  - **Cyclone Cathy** - Easy: Likes patterns and predictability
  - **Pattern Pete** - Medium: Learns your patterns and counters them
  - **Adaptive Ada** - Hard: Adapts strategy based on what's working

- ⚔️ **AI vs AI Battles**
  - Select any two AI opponents to compete
  - Choose the number of games (recommended: 10-50 for meaningful results)
  - Watch the running tally update in real-time
  - See detailed statistics and winner at the end
  - Battles are NOT recorded on the leaderboard (for entertainment only!)

- 🏆 **AI Tournament Mode**
  - Select 2-4 AI players to compete
  - Round-robin format - every AI plays against every other AI
  - Customizable games per matchup
  - Real-time match results and progress tracking
  - Final standings with comprehensive statistics
  - Crowns the tournament champion!
  - Tournament results are NOT recorded on the leaderboard

- 🏆 **Leaderboard System**
  - Persistent leaderboard tracked across all games
  - View top players with win rates and statistics
  - Individual player stats tracking

- 🎨 **Beautiful TUI**
  - Colorful terminal interface using Rich library
  - Emoji support for moves and results
  - Animated game flow

### Installation

#### Prerequisites

This game requires Python 3.7 or higher. Follow the instructions below for your operating system:

#### Windows

1. **Install Python**
   - Download Python from [python.org](https://www.python.org/downloads/)
   - Run the installer and **check the box "Add Python to PATH"**
   - Verify installation by opening Command Prompt and running:
     ```cmd
     python --version
     ```

2. **Download or Clone the Repository**

   ```cmd
   git clone <repository-url>
   cd ps-vibe-coding-hackathon
   ```

   Or download and extract the ZIP file from the repository

3. **Install Dependencies**

   ```cmd
   pip install -r requirements.txt
   ```

4. **Run the Game**
   ```cmd
   python play.py
   ```

#### macOS

1. **Install Python**
   - macOS comes with Python 2.x, but you need Python 3.7+
   - **Option 1: Using Homebrew** (recommended)

     ```bash
     # Install Homebrew if you don't have it
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

     # Install Python
     brew install python3
     ```

   - **Option 2: Download from python.org**
     - Download from [python.org](https://www.python.org/downloads/)
     - Run the installer
   - Verify installation:
     ```bash
     python3 --version
     ```

2. **Download or Clone the Repository**

   ```bash
   git clone <repository-url>
   cd ps-vibe-coding-hackathon
   ```

   Or download and extract the ZIP file from the repository

3. **Install Dependencies**

   ```bash
   pip3 install -r requirements.txt
   ```

4. **Run the Game**

   ```bash
   python3 play.py
   ```

   Or make it executable and run directly:

   ```bash
   chmod +x play.py
   ./play.py
   ```

#### Linux (Ubuntu/Debian)

1. **Install Python**
   - Most Linux distributions come with Python 3 pre-installed
   - Verify installation:
     ```bash
     python3 --version
     ```
   - If Python 3.7+ is not installed:
     ```bash
     sudo apt update
     sudo apt install python3 python3-pip
     ```

2. **Download or Clone the Repository**

   ```bash
   git clone <repository-url>
   cd ps-vibe-coding-hackathon
   ```

   Or download and extract the ZIP file from the repository

3. **Install Dependencies**

   ```bash
   pip3 install -r requirements.txt
   ```

   If you get a permissions error, you can install for your user only:

   ```bash
   pip3 install --user -r requirements.txt
   ```

4. **Run the Game**

   ```bash
   python3 play.py
   ```

   Or make it executable and run directly:

   ```bash
   chmod +x play.py
   ./play.py
   ```

#### Linux (Fedora/RHEL/CentOS)

1. **Install Python**

   ```bash
   sudo dnf install python3 python3-pip
   ```

   Or for older versions:

   ```bash
   sudo yum install python3 python3-pip
   ```

2. Follow steps 2-4 from the Ubuntu/Debian instructions above

#### Troubleshooting

- **"pip: command not found"**: Try using `pip3` instead of `pip`, or `python -m pip` or `python3 -m pip`
- **Permission errors on Linux/macOS**: Use `pip3 install --user -r requirements.txt` to install packages for your user only
- **Python not found on Windows**: Make sure you checked "Add Python to PATH" during installation, or add it manually to your system PATH
- **Terminal doesn't support emojis**: The game uses emojis for a better experience. Use a modern terminal emulator:
  - **Windows**: Windows Terminal (recommended), or PowerShell 7+
  - **macOS**: iTerm2 or the built-in Terminal app
  - **Linux**: GNOME Terminal, Konsole, or most modern terminal emulators

### How to Play

Once installed, run the game using:

**Windows:**

```cmd
python play.py
```

**macOS/Linux:**

```bash
python3 play.py
```

Or on Unix-based systems (macOS/Linux), make it executable and run directly:

```bash
chmod +x play.py
./play.py
```

### Game Rules

- 🪨 Rock beats ✂️ Scissors
- 📄 Paper beats 🪨 Rock
- ✂️ Scissors beats 📄 Paper

### Game Modes Explained

**1. Play vs AI** - Test your skills against computer opponents with different difficulty levels and strategies.

**2. Play vs Human (Local)** - Challenge a friend on the same computer. Player 2 looks away while Player 1 chooses!

**3. AI vs AI Battle** - Sit back and watch the AIs duke it out! Great for:

- Testing AI strategies against each other
- Seeing which difficulty level is truly the strongest
- Entertainment and pattern analysis
- Note: These battles don't affect the leaderboard

**4. AI Tournament Mode** - Host epic tournaments between multiple AIs! Features:

- Select 2-4 AI competitors
- Round-robin format (everyone plays everyone)
- Customize games per matchup
- Track real-time progress through all matches
- View comprehensive final standings
- Perfect for determining the ultimate AI champion!
- Note: Tournament results don't affect the leaderboard

**5. View Leaderboard** - See who's dominating the competition!

**6. View Your Stats** - Check your personal win rate and game history.

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
