# Codebase Exploration Guide: Rock Paper Scissors TUI Game

## Repository Information

| Field | Value |
|-------|--------|
| **Branch** | hackathon-josh-r-rps-pre-alpha |
| **Commit** | d3b2ccc |
| **Commit Date** | 2026-02-18 14:06:14 -0500 |
| **Exploration Date** | 2026-02-18 (when this guide was generated) |

---

## 1. Title and Overview

This guide helps you understand the current implementation before making changes. Follow the sections in order to build your understanding progressively.

### What the system does

**Rock Paper Scissors TUI Game** is a terminal-based game (Team 9: The Vibe Tribe hackathon project) with:

- **Multiple game modes**: Play vs AI, Play vs Human (local), AI vs AI Battle, AI Tournament, View Leaderboard, View Your Stats.
- **Five AI opponents** with different strategies: Randy Random (Easy), Cyclone Cathy (Easy), Pattern Pete (Medium), Adaptive Ada (Hard), Mind Reader Mike (Expert).
- **Persistent leaderboard** stored in `data/leaderboard.json` (human and human-vs-AI games only; AI vs AI and tournaments are not recorded).
- **Rich TUI** using the [Rich](https://rich.readthedocs.io/) library for panels, tables, prompts, and emoji.

### Current limitations relevant to adding features

- **No automated tests** – no `test_*.py` or pytest; manual testing only.
- **Single entrypoint** – all flows go through `play.py` → `src.main.main()`.
- **Leaderboard path is fixed** – `data/leaderboard.json` is the default; config is not externalized.
- **AI list is code-defined** – `AI_OPPONENTS` in `src/ai.py`; adding an AI requires code changes.
- **`analyze_moves.py`** – one-off script with a hardcoded file path; not part of the main app flow.

---

## 2. Object Relationships

The diagram below shows how the main objects and layers relate. **Entrypoint** → **TUI/Controller** → **Domain (Game + AI)** → **Persistence (Leaderboard)**.

```mermaid
classDiagram
    direction TB

    class play_py <<entrypoint>>
    play_py : +main()

    class RockPaperScissorsGame <<controller>>
    RockPaperScissorsGame : -leaderboard Leaderboard
    RockPaperScissorsGame : -player_name str
    RockPaperScissorsGame : -player_move_history list
    RockPaperScissorsGame : -current_ai AIPlayer
    RockPaperScissorsGame : +main_menu()
    RockPaperScissorsGame : +play_vs_ai()
    RockPaperScissorsGame : +play_vs_human()
    RockPaperScissorsGame : +ai_vs_ai_battle()
    RockPaperScissorsGame : +ai_tournament()
    RockPaperScissorsGame : +view_leaderboard()
    RockPaperScissorsGame : +view_player_stats()
    RockPaperScissorsGame : +run()

    class Move <<enum>>
    Move : ROCK, PAPER, SCISSORS

    class GameResult <<enum>>
    GameResult : WIN, LOSE, TIE

    class Game <<static logic>>
    Game : +determine_winner(Move, Move) GameResult
    Game : +get_move_emoji(Move) str

    class AIPlayer <<abstract>>
    AIPlayer : +name str
    AIPlayer : +personality str
    AIPlayer : +move_history List
    AIPlayer : +make_move(opponent_history) Move
    AIPlayer : +record_move(Move)

    class RandomAI
    class CycleAI
    class PatternAI
    class AdaptiveAI
    class PsychologicalAI

    class Leaderboard <<service>>
    Leaderboard : -data_file str
    Leaderboard : -entries Dict
    Leaderboard : +load() save() record_win/loss/tie()
    Leaderboard : +get_top_players() get_player_stats()

    class LeaderboardEntry <<domain>>
    LeaderboardEntry : +player_name, wins, losses, ties
    LeaderboardEntry : +total_games, win_rate, to_dict(), from_dict()

    class leaderboard_json <<file>>
    leaderboard_json : data/leaderboard.json

    play_py --> RockPaperScissorsGame : calls main()
    RockPaperScissorsGame --> Leaderboard
    RockPaperScissorsGame --> Game
    RockPaperScissorsGame --> AIPlayer
    RockPaperScissorsGame --> Move
    RockPaperScissorsGame --> GameResult
    Game --> Move
    Game --> GameResult
    AIPlayer <|-- RandomAI
    AIPlayer <|-- CycleAI
    AIPlayer <|-- PatternAI
    AIPlayer <|-- AdaptiveAI
    AIPlayer <|-- PsychologicalAI
    AIPlayer --> Move
    Leaderboard --> LeaderboardEntry
    Leaderboard --> leaderboard_json
```

![RPS object relationships](assets/rps-object-relationships.png)

*If the image is missing, generate a PNG from `docs/exploration/assets/rps-object-relationships.mmd` using [Mermaid Live Editor](https://mermaid.live) or `@mermaid-js/mermaid-cli` (mmdc) and save it as `docs/exploration/assets/rps-object-relationships.png`.*

---

## 3. Learning Path (Progressive Sections)

### Start here: Domain models and enums

**Purpose:** The game is built on a few core types. All features touch these.

**Files to review:**

- `src/game.py` (lines 1–57): `Move`, `GameResult`, `Game` (static methods only).

**Key concepts:**

- `Move` and `GameResult` are enums. Result is from **player1’s perspective** (WIN/LOSE/TIE).
- `Game` has no instance state; `determine_winner(player1_move, player2_move)` and `get_move_emoji(move)` are the only public API.

**What to look for:**

- How ties and wins are determined (line 40–51).
- Emoji mapping (line 55–56).

**What you should understand:** You can predict the result of any (move1, move2) and know how the UI gets an emoji for a move.

---

### Next: AI layer

**Purpose:** All “vs AI” and “AI vs AI” behavior is driven by the AI module.

**Files to review:**

- `src/ai.py` (full file): `AIPlayer` base class, five concrete AIs, `AI_OPPONENTS` list, `create_ai(ai_index)`.

**Key concepts:**

- Each AI implements `make_move(opponent_history: List[Move]) -> Move` and optionally `record_move`; `AdaptiveAI` also has `record_win`/`record_loss`.
- `opponent_history` is the **other** player’s move history (what the AI uses to decide).
- `AI_OPPONENTS` is a list of dicts: `class`, `name`, `personality`, `difficulty`. Adding a new AI = new class + new dict entry.

**What to look for:**

- How `create_ai(index)` instantiates from `AI_OPPONENTS[index]["class"]` (lines 262–266).
- How `AdaptiveAI` and `PsychologicalAI` use extra state (e.g. `wins_by_move`, `opponent_last_result`).

**What you should understand:** You know where to add a new AI and how move/result history is passed in.

---

### Next: Leaderboard and persistence

**Purpose:** Human (and human-vs-AI) results are persisted here; AI-only modes do not use it.

**Files to review:**

- `src/leaderboard.py` (full file): `LeaderboardEntry`, `Leaderboard`, load/save to JSON.

**Key concepts:**

- In-memory store: `Leaderboard.entries` is `Dict[str, LeaderboardEntry]` keyed by player name.
- File: `data/leaderboard.json`; created on first write; directory created in `_ensure_data_dir()`.
- Every `record_win`/`record_loss`/`record_tie` calls `save()` (full file write).

**What to look for:**

- `get_or_create_player` (lines 80–85) and how `record_*` use it (86–105).
- Sorting in `get_top_players`: by `(wins, win_rate)` descending (107–113).

**What you should understand:** You know where stats live, how they’re updated, and that only human-involved games are recorded.

---

### Then: TUI and main controller

**Purpose:** All user interaction and game flow are in one controller class.

**Files to review:**

- `src/main.py`: `RockPaperScissorsGame` and `main()`.

**Key concepts:**

- Single `Console()` from Rich; all I/O goes through it (and `Prompt`/`IntPrompt`).
- Main loop in `run()` (lines 609–639): menu choice → dispatch to `play_vs_ai`, `play_vs_human`, `ai_vs_ai_battle`, `ai_tournament`, `view_leaderboard`, `view_player_stats`, or quit.
- For vs-AI: `get_player_name` → `select_ai_opponent` → `create_ai` → rounds loop (get move, AI move, `Game.determine_winner`, display, update leaderboard only for human games).

**What to look for:**

- Where `self.leaderboard.record_*` is called (only in `play_vs_ai` and `play_vs_human`; not in AI battle or tournament).
- How `player_move_history` is passed to `ai.make_move()` and how `AdaptiveAI` is updated (e.g. lines 211–214, 386–396).

**What you should understand:** You can trace one menu option from menu → controller method → Game/AI/Leaderboard.

---

### Finally: Entrypoint and scripts

**Purpose:** Know how the app is started and what is outside the main app.

**Files to review:**

- `play.py` (full file): adds project root to `sys.path`, imports `src.main.main`, calls `main()`.
- `analyze_moves.py`: standalone script; hardcoded path; not used by `play.py`.

**What you should understand:** `python play.py` is the only standard entrypoint; anything else (e.g. `analyze_moves.py`) is auxiliary.

---

## 4. Code Map / File References

- **play.py (lines 1–15):** Entry point; adds repo root to path and calls `src.main.main()`.
- **src/main.py (lines 19–28):** `RockPaperScissorsGame.__init__` – creates `Leaderboard()`, holds optional `player_name`, `player_move_history`, `current_ai`, `player2_name`.
- **src/main.py (lines 41–61):** `main_menu()` – shows title, Rich table of options 1–7, returns choice.
- **src/main.py (lines 166–266):** `play_vs_ai()` – get name, select AI, rounds loop (player move, AI move via `Game.determine_winner`), then leaderboard update for human.
- **src/main.py (lines 268–348):** `play_vs_human()` – two players, same round structure; both names sent to leaderboard.
- **src/main.py (lines 414–461):** `ai_vs_ai_battle()` – two AIs selected, N games, no leaderboard.
- **src/main.py (lines 463–606):** `ai_tournament()` – 2–4 AIs, round-robin matchups, games per matchup; no leaderboard.
- **src/main.py (lines 350–386, 388–412):** `view_leaderboard()`, `view_player_stats()` – read from `Leaderboard` only.
- **src/game.py (lines 6–23):** `Move` and `GameResult` enums.
- **src/game.py (lines 26–57):** `Game.determine_winner`, `Game.get_move_emoji`.
- **src/ai.py (lines 8–21):** `AIPlayer` base class – `make_move`, `record_move`.
- **src/ai.py (lines 25–267):** Concrete AIs and `AI_OPPONENTS`; `create_ai(ai_index)`.
- **src/leaderboard.py (lines 9–46):** `LeaderboardEntry` – fields, `total_games`, `win_rate`, `to_dict`, `from_dict`.
- **src/leaderboard.py (lines 48–117):** `Leaderboard` – `load`/`save`, `get_or_create_player`, `record_win`/`record_loss`/`record_tie`, `get_top_players`, `get_player_stats`.
- **analyze_moves.py (lines 1–22):** One-off script; hardcoded path; parses text for move counts; not part of main app.

---

## 5. Key Concepts

- **Player perspective:** `GameResult` is always from player1’s view (WIN = player1 wins, LOSE = player2 wins).
- **Opponent history:** In `make_move(opponent_history)`, `opponent_history` is the **other** player’s list of moves (so the AI can pattern-match or counter).
- **Leaderboard scope:** Only games where at least one human is a player are recorded; AI vs AI and tournaments are explicitly not recorded.
- **Rich TUI:** One global `Console()`; menus and prompts use `Prompt.ask`, `IntPrompt.ask`; output uses `Panel`, `Table`, `console.print`.
- **Persistence:** JSON file; one load at startup, save on every record_win/loss/tie; no caching layer beyond `Leaderboard.entries`.

---

## 6. Data Flow

1. **Startup:** `play.py` → `main()` → `RockPaperScissorsGame()` → `Leaderboard()` → `load()` reads `data/leaderboard.json` into `entries`.
2. **Menu:** User picks 1–7; `run()` dispatches to the corresponding method.
3. **Play vs AI:** Name → select AI index → `create_ai(index)` → for each round: player move (prompt) → append to `player_move_history` → `ai.make_move(player_move_history)` → `Game.determine_winner` → display → if `AdaptiveAI`, optional `record_win`. After all rounds, `leaderboard.record_win`/`record_loss`/`record_tie` for the human only → `save()`.
4. **Play vs Human:** Same idea; both names get leaderboard updates; no AI.
5. **AI vs AI / Tournament:** Only `Game.determine_winner` and in-memory scores; no leaderboard calls.
6. **View Leaderboard/Stats:** Read from `Leaderboard.get_top_players` or `get_player_stats`; no file write.

**Caching:** Leaderboard is loaded once and kept in memory; every win/loss/tie triggers a full JSON save. No other caches.

---

## 7. Questions to Answer (Checklist)

**Data flow**

- [ ] What is the exact call chain from “Play vs AI” menu to writing the result to disk?
- [ ] Where is `opponent_history` set when the human plays vs AI? When two AIs play each other?

**Caching / persistence**

- [ ] When is `data/leaderboard.json` read? When is it written?
- [ ] Which game modes never call `Leaderboard.record_*`?

**Dependencies**

- [ ] What does the project depend on (e.g. Rich)? Where is that specified?
- [ ] How is the project root made importable when running `play.py`?

**Lifecycle**

- [ ] How long does a single `RockPaperScissorsGame` instance live? A single `Leaderboard`? A single `AIPlayer` per game or per round?

**Error handling**

- [ ] What happens if `data/leaderboard.json` is missing or invalid JSON?
- [ ] How does the app handle Ctrl+C during a game?

---

## 8. Next Steps

- **Draw a sequence diagram** for one path (e.g. “Play vs AI” for 1 round) from menu to leaderboard save.
- **Add tests:** Start with `Game.determine_winner` and `LeaderboardEntry.win_rate` / `total_games`; then integration tests for one full game flow.
- **Decide feature scope:** New game mode, new AI, or leaderboard/UI changes; use the code map above to find the exact files and methods to touch.
- **Refactor if needed:** e.g. extract “play N rounds and return (p1_wins, p2_wins, ties)” to reduce duplication between vs AI, vs human, and AI vs AI.

---

## 9. Additional Resources

- [Rich documentation](https://rich.readthedocs.io/) – Console, Panel, Table, Prompt.
- Python 3.7+ (enums, type hints, f-strings).
- JSON for persistence; no database.
- Project README and SETUP.md in the repo root for run instructions and feature list.

---

## 10. Common Pitfalls to Avoid

- **Result perspective:** Passing `GameResult` to UI or leaderboard: remember it’s from player1’s perspective; for “AI won” you check `result == GameResult.LOSE` when player1 is the human (see e.g. `main.py` around 212).
- **Leaderboard in AI-only modes:** Do not call `record_win`/`record_loss`/`record_tie` in `ai_vs_ai_battle` or `ai_tournament`; the design explicitly excludes those from the leaderboard.
- **AdaptiveAI state:** In AI vs AI, both AIs get `record_win`/`record_loss`; ensure you pass the correct result from each AI’s perspective (see `main.py` 386–396).
- **Path and imports:** Running scripts from a different working directory can break `data/leaderboard.json` path (relative to cwd) and `src` imports; run from repo root and use `play.py` as entrypoint.
- **analyze_moves.py:** Contains a hardcoded path; not integrated with the app; safe to ignore or refactor if you need move-analysis features.

---

## Current vs. Future State

| Area | Current | Typical extension |
|------|---------|--------------------|
| **Tests** | None | Add unit tests for `Game`, `LeaderboardEntry`, and integration for one game flow. |
| **Config** | Leaderboard path and AI list in code | Optional config file or env for data path; plugin-style AI list if you add many AIs. |
| **Entrypoints** | Single `play.py` | Keep one entrypoint; add CLI flags (e.g. `--no-tui`) only if you introduce a non-TUI mode. |
| **New features** | Add in `main.py` (menu + new method) and/or `ai.py` (new AI class + `AI_OPPONENTS` entry); leaderboard in `leaderboard.py`. | Follow existing patterns: menu option → controller method → domain/persistence. |

---

*End of Codebase Exploration Guide.*
