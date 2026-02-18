# Setup and Testing Instructions

## Installation Instructions by Platform

### Windows Installation

1. **Install Python** (if not already installed):
   - Download Python 3.8 or later from [python.org](https://www.python.org/downloads/)
   - During installation, **check the box** "Add Python to PATH"
   - Verify installation by opening Command Prompt and running:
     ```cmd
     python --version
     ```

2. **Clone or download the project**:
   - If using Git:
     ```cmd
     git clone <repository-url>
     cd ps-vibe-coding-hackathon
     ```
   - Or download and extract the ZIP file, then navigate to the folder in Command Prompt

3. **Set up a virtual environment** (recommended):

   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

   - Your prompt should change to show `(venv)` when activated
   - To deactivate later, run: `deactivate`

4. **Install dependencies**:

   ```cmd
   pip install -r requirements.txt
   ```

5. **Run the game**:
   ```cmd
   python play.py
   ```

**Windows Troubleshooting:**

- If `python` command doesn't work, try `py` or `python3`
- If you see "script execution disabled" errors with PowerShell, use Command Prompt instead
- For emoji display issues, use Windows Terminal (available in Microsoft Store) instead of the legacy Command Prompt

### macOS Installation

1. **Install Python** (if not already installed):
   - macOS 10.15+ comes with Python 3, verify with:
     ```bash
     python3 --version
     ```
   - If needed, install via Homebrew:
     ```bash
     brew install python3
     ```
   - Or download from [python.org](https://www.python.org/downloads/)

2. **Clone or download the project**:

   ```bash
   git clone <repository-url>
   cd ps-vibe-coding-hackathon
   ```

3. **Set up a virtual environment** (recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   - Your prompt should change to show `(venv)` when activated
   - To deactivate later, run: `deactivate`

4. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

5. **Run the game**:
   ```bash
   python3 play.py
   ```

**macOS Troubleshooting:**

- If you get SSL certificate errors, run: `/Applications/Python\ 3.x/Install\ Certificates.command`
- Ensure your terminal supports UTF-8 for proper emoji display

### Linux Installation

1. **Install Python** (if not already installed):
   - **Debian/Ubuntu/Mint:**
     ```bash
     sudo apt update
     sudo apt install python3 python3-pip python3-venv
     ```
   - **Fedora/RHEL/CentOS:**
     ```bash
     sudo dnf install python3 python3-pip
     ```
   - **Arch/Manjaro:**
     ```bash
     sudo pacman -S python python-pip
     ```
   - Verify installation:
     ```bash
     python3 --version
     ```

2. **Clone or download the project**:

   ```bash
   git clone <repository-url>
   cd ps-vibe-coding-hackathon
   ```

3. **Set up a virtual environment** (recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   - Your prompt should change to show `(venv)` when activated
   - To deactivate later, run: `deactivate`

4. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

5. **Run the game**:
   ```bash
   python3 play.py
   ```

**Linux Troubleshooting:**

- If `pip` is not found, install it with your package manager (e.g., `sudo apt install python3-pip`)
- For emoji display, ensure your terminal emulator supports UTF-8 and has a font with emoji support
- If you get permission errors, don't use `sudo` with pip - use a virtual environment instead

## Quick Start (All Platforms)

Once Python is installed and you're in the project directory:

```bash
# Create virtual environment
python3 -m venv venv        # On Linux/macOS
python -m venv venv         # On Windows

# Activate virtual environment
source venv/bin/activate    # On Linux/macOS
venv\Scripts\activate       # On Windows

# Install dependencies
pip install -r requirements.txt

# Run the game
python3 play.py             # On Linux/macOS
python play.py              # On Windows
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

### 3. Test AI vs AI Battles

- Select option 3 from the main menu
- Choose **FIRST PLAYER** (any AI opponent)
- Choose **SECOND PLAYER** (any AI opponent - can be the same type!)
- Set number of games (try 10-20 for a quick demo, or 50+ for statistical analysis)
- Watch the battle unfold with real-time score updates
- View final statistics and winner
- Great combos to try:
  - Pattern Pete vs Adaptive Ada (strategic battle!)
  - Randy Random vs Cyclone Cathy (chaos vs order)
  - Adaptive Ada vs Adaptive Ada (learning AIs compete)

### 4. Test AI Tournament Mode (NEW!)

- Select option 4 from the main menu
- Choose how many AI players to compete (2-4)
- Select each AI player one by one (clear labels show who's been selected)
- Set number of games per matchup (try 5-10 for quick tournaments)
- Watch as all AIs compete in round-robin format
- View match results as they happen
- See final standings with comprehensive stats
- The champion is crowned!
- Great tournament ideas:
  - All 4 AIs competing (6 total matchups)
  - Easy vs Medium vs Hard (3 AIs, 3 matchups)
  - Battle of the adaptives (multiple Adaptive Adas)

### 5. Test Leaderboard

- Play a few games first (AI vs AI battles and tournaments won't show up here!)
- Select option 5 from the main menu
- View the leaderboard with rankings

### 6. Test Player Stats

- Select option 6 from the main menu
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
