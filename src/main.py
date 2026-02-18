"""Main TUI application for Rock Paper Scissors."""

import time
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.table import Table
from rich import box
from typing import Optional

from src.game import Game, Move, GameResult
from src.ai import AI_OPPONENTS, create_ai, AIPlayer, AdaptiveAI
from src.leaderboard import Leaderboard


console = Console()


class RockPaperScissorsGame:
    """Main game controller."""

    def __init__(self):
        self.leaderboard = Leaderboard()
        self.player_name: Optional[str] = None
        self.player_move_history = []
        self.current_ai: Optional[AIPlayer] = None
        self.player2_name: Optional[str] = None

    def show_title(self):
        """Display game title."""
        console.clear()
        title = """
╦═╗┌─┐┌─┐┬┌─  ╔═╗┌─┐┌─┐┌─┐┬─┐  ╔═╗┌─┐┬┌─┐┌─┐┌─┐┬─┐┌─┐
╠╦╝│ ││  ├┴┐  ╠═╝├─┤├─┘├┤ ├┬┘  ╚═╗│  │└─┐└─┐│ │├┬┘└─┐
╩╚═└─┘└─┘┴ ┴  ╩  ┴ ┴┴  └─┘┴└─  ╚═╝└─┘┴└─┘└─┘└─┘┴└─└─┘
        """
        console.print(
            Panel(title, style="bold cyan", subtitle="Team 9: The Vibe Tribe")
        )

    def main_menu(self):
        """Display main menu and get user choice."""
        self.show_title()

        menu = Table(show_header=False, box=box.ROUNDED, style="cyan")
        menu.add_column("Option", style="bold")
        menu.add_column("Description")

        menu.add_row("1", "🤖 Play vs AI")
        menu.add_row("2", "👥 Play vs Human (Local)")
        menu.add_row("3", "🤖⚔️🤖 Watch AI vs AI Battle")
        menu.add_row("4", "🏆🤖 AI Tournament Mode")
        menu.add_row("5", "🏆 View Leaderboard")
        menu.add_row("6", "📊 View Your Stats")
        menu.add_row("7", "👋 Quit")

        console.print(menu)
        choice = Prompt.ask(
            "\nChoose an option", choices=["1", "2", "3", "4", "5", "6", "7"]
        )
        return choice

    def get_player_name(self) -> str:
        """Get or confirm player name."""
        if self.player_name:
            use_same = Prompt.ask(
                f"\nWelcome back, [bold]{self.player_name}[/bold]! Continue as this player?",
                choices=["y", "n"],
                default="y",
            )
            if use_same == "y":
                return self.player_name

        name = Prompt.ask("\n[bold cyan]Enter your name[/bold cyan]")
        self.player_name = name
        return name

    def select_ai_opponent(self) -> int:
        """Let player select an AI opponent."""
        console.clear()
        self.show_title()

        console.print("\n[bold cyan]Choose Your Opponent:[/bold cyan]\n")

        table = Table(show_header=True, box=box.ROUNDED, style="cyan")
        table.add_column("#", style="bold", width=3)
        table.add_column("Name", style="bold yellow")
        table.add_column("Difficulty", style="bold")
        table.add_column("Personality")

        for i, ai in enumerate(AI_OPPONENTS):
            difficulty_color = {"Easy": "green", "Medium": "yellow", "Hard": "red"}.get(
                ai["difficulty"], "white"
            )

            table.add_row(
                str(i + 1),
                ai["name"],
                f"[{difficulty_color}]{ai['difficulty']}[/{difficulty_color}]",
                ai["personality"],
            )

        console.print(table)

        choice = IntPrompt.ask(
            "\nSelect opponent", choices=[str(i + 1) for i in range(len(AI_OPPONENTS))]
        )
        return choice - 1

    def get_move_choice(self, player_name: str) -> Move:
        """Get player's move choice."""
        console.print(f"\n[bold]{player_name}[/bold], choose your move:")
        console.print("1. 🪨 Rock")
        console.print("2. 📄 Paper")
        console.print("3. ✂️  Scissors")

        choice = Prompt.ask("Your choice", choices=["1", "2", "3"])

        move_map = {"1": Move.ROCK, "2": Move.PAPER, "3": Move.SCISSORS}
        return move_map[choice]

    def display_round_result(
        self,
        player1_name: str,
        player1_move: Move,
        player2_name: str,
        player2_move: Move,
        result: GameResult,
    ):
        """Display the result of a round with side-by-side ASCII art."""
        console.print("\n" + "=" * 50)

        # Side-by-side ASCII art: left = player1 name + art, center = VS, right = player2 name + art
        lines1 = Game.get_move_ascii_art_lines(player1_move)
        lines2 = Game.get_move_ascii_art_lines(player2_move)
        width = 20  # fixed width per art block for alignment
        max_lines = max(len(lines1), len(lines2))
        while len(lines1) < max_lines:
            lines1.append("")
        while len(lines2) < max_lines:
            lines2.append("")

        # Names row (above the art)
        console.print(f"  [bold cyan]{player1_name}[/bold cyan]     [bold]VS[/bold]     [bold yellow]{player2_name}[/bold yellow]")
        # Art lines
        for i in range(max_lines):
            left = (lines1[i] if i < len(lines1) else "").ljust(width)
            right = (lines2[i] if i < len(lines2) else "").ljust(width)
            console.print(f"  {left}     [bold]VS[/bold]     {right}")

        # Show result
        if result == GameResult.WIN:
            console.print(f"\n[bold green]🎉 {player1_name} WINS![/bold green]")
        elif result == GameResult.LOSE:
            console.print(f"\n[bold red]😢 {player2_name} WINS![/bold red]")
        else:
            console.print("\n[bold yellow]🤝 IT'S A TIE![/bold yellow]")

        console.print("=" * 50 + "\n")
        time.sleep(5)

    def play_vs_ai(self):
        """Play against an AI opponent."""
        player_name = self.get_player_name()
        ai_index = self.select_ai_opponent()
        self.current_ai = create_ai(ai_index)

        console.clear()
        self.show_title()

        ai_info = AI_OPPONENTS[ai_index]
        console.print(
            Panel(
                f'[bold yellow]{ai_info["name"]}[/bold yellow] says:\n"{ai_info["personality"]}"',
                title="Your Opponent",
                style="yellow",
            )
        )

        rounds = IntPrompt.ask("\nHow many rounds?", default=3)

        player_wins = 0
        ai_wins = 0
        ties = 0

        for round_num in range(1, rounds + 1):
            console.clear()
            self.show_title()
            console.print(f"\n[bold]Round {round_num}/{rounds}[/bold]")
            console.print(
                f"Score: [cyan]{player_name}: {player_wins}[/cyan] | [yellow]{self.current_ai.name}: {ai_wins}[/yellow] | Ties: {ties}"
            )

            # Player makes move
            player_move = self.get_move_choice(player_name)
            self.player_move_history.append(player_move)

            # AI makes move
            ai_move = self.current_ai.make_move(self.player_move_history)
            self.current_ai.record_move(ai_move)

            # Determine result
            result = Game.determine_winner(player_move, ai_move)

            # Update adaptive AI
            if isinstance(self.current_ai, AdaptiveAI):
                if result == GameResult.LOSE:  # AI won
                    self.current_ai.record_win(ai_move)

            # Display result
            self.display_round_result(
                player_name, player_move, self.current_ai.name, ai_move, result
            )

            # Update scores
            if result == GameResult.WIN:
                player_wins += 1
            elif result == GameResult.LOSE:
                ai_wins += 1
            else:
                ties += 1

        # Final results
        console.clear()
        self.show_title()
        console.print("\n[bold cyan]GAME OVER![/bold cyan]\n")

        results_table = Table(show_header=True, box=box.ROUNDED)
        results_table.add_column("Player", style="bold")
        results_table.add_column("Wins", justify="center")
        results_table.add_column("Result", justify="center")

        if player_wins > ai_wins:
            results_table.add_row(
                player_name, str(player_wins), "[bold green]WINNER! 🎉[/bold green]"
            )
            results_table.add_row(
                self.current_ai.name, str(ai_wins), "[red]Loser[/red]"
            )
            self.leaderboard.record_win(player_name)
        elif ai_wins > player_wins:
            results_table.add_row(player_name, str(player_wins), "[red]Loser[/red]")
            results_table.add_row(
                self.current_ai.name,
                str(ai_wins),
                "[bold green]WINNER! 🎉[/bold green]",
            )
            self.leaderboard.record_loss(player_name)
        else:
            results_table.add_row(
                player_name, str(player_wins), "[yellow]Draw[/yellow]"
            )
            results_table.add_row(
                self.current_ai.name, str(ai_wins), "[yellow]Draw[/yellow]"
            )
            self.leaderboard.record_tie(player_name)

        console.print(results_table)
        console.print(f"\nTies: {ties}")

        Prompt.ask("\nPress Enter to continue")

    def play_vs_human(self):
        """Play against another human locally."""
        console.clear()
        self.show_title()

        player1_name = self.get_player_name()
        player2_name = Prompt.ask("\n[bold cyan]Enter Player 2's name[/bold cyan]")

        rounds = IntPrompt.ask("\nHow many rounds?", default=3)

        player1_wins = 0
        player2_wins = 0
        ties = 0

        for round_num in range(1, rounds + 1):
            console.clear()
            self.show_title()
            console.print(f"\n[bold]Round {round_num}/{rounds}[/bold]")
            console.print(
                f"Score: [cyan]{player1_name}: {player1_wins}[/cyan] | [yellow]{player2_name}: {player2_wins}[/yellow] | Ties: {ties}"
            )

            # Player 1 makes move
            player1_move = self.get_move_choice(player1_name)

            console.print(
                "\n[bold red]Player 2's turn... Player 1 look away![/bold red]"
            )
            time.sleep(1)

            # Player 2 makes move
            player2_move = self.get_move_choice(player2_name)

            # Determine result
            result = Game.determine_winner(player1_move, player2_move)

            # Display result
            self.display_round_result(
                player1_name, player1_move, player2_name, player2_move, result
            )

            # Update scores
            if result == GameResult.WIN:
                player1_wins += 1
            elif result == GameResult.LOSE:
                player2_wins += 1
            else:
                ties += 1

        # Final results
        console.clear()
        self.show_title()
        console.print("\n[bold cyan]GAME OVER![/bold cyan]\n")

        results_table = Table(show_header=True, box=box.ROUNDED)
        results_table.add_column("Player", style="bold")
        results_table.add_column("Wins", justify="center")
        results_table.add_column("Result", justify="center")

        if player1_wins > player2_wins:
            results_table.add_row(
                player1_name, str(player1_wins), "[bold green]WINNER! 🎉[/bold green]"
            )
            results_table.add_row(player2_name, str(player2_wins), "[red]Loser[/red]")
            self.leaderboard.record_win(player1_name)
            self.leaderboard.record_loss(player2_name)
        elif player2_wins > player1_wins:
            results_table.add_row(player1_name, str(player1_wins), "[red]Loser[/red]")
            results_table.add_row(
                player2_name, str(player2_wins), "[bold green]WINNER! 🎉[/bold green]"
            )
            self.leaderboard.record_loss(player1_name)
            self.leaderboard.record_win(player2_name)
        else:
            results_table.add_row(
                player1_name, str(player1_wins), "[yellow]Draw[/yellow]"
            )
            results_table.add_row(
                player2_name, str(player2_wins), "[yellow]Draw[/yellow]"
            )
            self.leaderboard.record_tie(player1_name)
            self.leaderboard.record_tie(player2_name)

        console.print(results_table)
        console.print(f"\nTies: {ties}")

        Prompt.ask("\nPress Enter to continue")

    def view_leaderboard(self):
        """Display the leaderboard."""
        console.clear()
        self.show_title()

        console.print("\n[bold cyan]🏆 LEADERBOARD 🏆[/bold cyan]\n")

        top_players = self.leaderboard.get_top_players(10)

        if not top_players:
            console.print(
                "[yellow]No games played yet! Be the first to compete![/yellow]"
            )
        else:
            table = Table(show_header=True, box=box.ROUNDED, style="cyan")
            table.add_column("Rank", style="bold", width=6)
            table.add_column("Player", style="bold yellow")
            table.add_column("Wins", justify="center")
            table.add_column("Losses", justify="center")
            table.add_column("Ties", justify="center")
            table.add_column("Total", justify="center")
            table.add_column("Win Rate", justify="center")

            for i, entry in enumerate(top_players, 1):
                rank_emoji = {1: "🥇", 2: "🥈", 3: "🥉"}.get(i, f"{i}.")
                table.add_row(
                    rank_emoji,
                    entry.player_name,
                    str(entry.wins),
                    str(entry.losses),
                    str(entry.ties),
                    str(entry.total_games),
                    f"{entry.win_rate:.1f}%",
                )

            console.print(table)

        Prompt.ask("\nPress Enter to continue")

    def view_player_stats(self):
        """View stats for the current player."""
        if not self.player_name:
            player_name = self.get_player_name()
        else:
            player_name = self.player_name

        console.clear()
        self.show_title()

        stats = self.leaderboard.get_player_stats(player_name)

        console.print(f"\n[bold cyan]📊 Stats for {player_name}[/bold cyan]\n")

        stats_table = Table(show_header=False, box=box.ROUNDED, style="cyan")
        stats_table.add_column("Stat", style="bold")
        stats_table.add_column("Value", justify="right")

        stats_table.add_row("Games Played", str(stats.total_games))
        stats_table.add_row("Wins", f"[green]{stats.wins}[/green]")
        stats_table.add_row("Losses", f"[red]{stats.losses}[/red]")
        stats_table.add_row("Ties", f"[yellow]{stats.ties}[/yellow]")
        stats_table.add_row("Win Rate", f"{stats.win_rate:.1f}%")

        console.print(stats_table)

        Prompt.ask("\nPress Enter to continue")

    def ai_vs_ai_battle(self):
        """Watch two AI opponents battle each other."""
        console.clear()
        self.show_title()

        console.print("\n[bold cyan]⚔️  AI vs AI BATTLE ARENA ⚔️[/bold cyan]\n")
        console.print("[yellow]Select two AI opponents to battle![/yellow]\n")

        # Select first AI
        console.print("[bold green]🥊 SELECT FIRST PLAYER:[/bold green]")
        ai1_index = self.select_ai_opponent()
        ai1 = create_ai(ai1_index)
        ai1_config = AI_OPPONENTS[ai1_index]

        # Select second AI
        console.clear()
        self.show_title()
        console.print("\n[bold cyan]⚔️  AI vs AI BATTLE ARENA ⚔️[/bold cyan]\n")
        console.print(
            f"[green]✓ First Player: {ai1.name} ({ai1_config['difficulty']})[/green]\n"
        )
        console.print("[bold yellow]🥊 SELECT SECOND PLAYER:[/bold yellow]")
        ai2_index = self.select_ai_opponent()
        ai2 = create_ai(ai2_index)
        ai2_config = AI_OPPONENTS[ai2_index]

        # Get number of games
        console.clear()
        self.show_title()
        console.print("\n[bold cyan]⚔️  AI vs AI BATTLE ARENA ⚔️[/bold cyan]\n")

        matchup_panel = Panel(
            f"[bold green]{ai1.name}[/bold green] ({ai1_config['difficulty']})\n"
            f"     VS\n"
            f"[bold yellow]{ai2.name}[/bold yellow] ({ai2_config['difficulty']})",
            title="The Matchup",
            style="cyan",
        )
        console.print(matchup_panel)

        num_games = IntPrompt.ask("\nHow many games should they play?", default=10)

        # Initialize stats
        ai1_wins = 0
        ai2_wins = 0
        ties = 0
        ai1_history = []
        ai2_history = []

        # Battle time!
        console.clear()
        self.show_title()
        console.print(f"\n[bold cyan]⚔️  {ai1.name} vs {ai2.name} ⚔️[/bold cyan]\n")
        console.print("[yellow]Battle commencing...[/yellow]\n")
        time.sleep(1)

        # Create results table
        results_display = Table(
            show_header=True, box=box.ROUNDED, style="cyan", title="Battle Results"
        )
        results_display.add_column("Game", justify="center", style="bold", width=6)
        results_display.add_column(ai1.name, justify="center", style="green")
        results_display.add_column("Result", justify="center", width=10)
        results_display.add_column(ai2.name, justify="center", style="yellow")
        results_display.add_column("Score", justify="center", width=12)

        for game_num in range(1, num_games + 1):
            # AI 1 makes move
            ai1_move = ai1.make_move(ai2_history)
            ai1.record_move(ai1_move)
            ai1_history.append(ai1_move)

            # AI 2 makes move
            ai2_move = ai2.make_move(ai1_history)
            ai2.record_move(ai2_move)
            ai2_history.append(ai2_move)

            # Determine winner
            result = Game.determine_winner(ai1_move, ai2_move)

            # Update adaptive AIs
            if isinstance(ai1, AdaptiveAI):
                if result == GameResult.WIN:
                    ai1.record_win(ai1_move)
                elif result == GameResult.LOSE:
                    ai1.record_loss(ai1_move)
            if isinstance(ai2, AdaptiveAI):
                if result == GameResult.LOSE:  # AI2 won
                    ai2.record_win(ai2_move)
                elif result == GameResult.WIN:  # AI2 lost
                    ai2.record_loss(ai2_move)

            # Update scores
            if result == GameResult.WIN:
                ai1_wins += 1
                result_text = "[bold green]WIN[/bold green]"
            elif result == GameResult.LOSE:
                ai2_wins += 1
                result_text = "[bold red]LOSS[/bold red]"
            else:
                ties += 1
                result_text = "[yellow]TIE[/yellow]"

            # Add row to results
            score_text = f"{ai1_wins}-{ai2_wins}-{ties}"
            results_display.add_row(
                f"#{game_num}",
                f"{Game.get_move_emoji(ai1_move)} {ai1_move}",
                result_text,
                f"{Game.get_move_emoji(ai2_move)} {ai2_move}",
                score_text,
            )

            # Update display every game
            console.clear()
            self.show_title()
            console.print(f"\n[bold cyan]⚔️  {ai1.name} vs {ai2.name} ⚔️[/bold cyan]\n")
            console.print(results_display)

            # Show current score prominently
            score_panel = Panel(
                f"[bold green]{ai1.name}: {ai1_wins}[/bold green]  |  "
                f"[bold yellow]{ai2.name}: {ai2_wins}[/bold yellow]  |  "
                f"Ties: {ties}",
                title=f"Score After Game {game_num}/{num_games}",
                style="cyan",
            )
            console.print(score_panel)

            # Pause briefly between games (shorter for more games)
            pause_time = 0.5 if num_games > 20 else 0.8 if num_games > 10 else 1.2
            time.sleep(pause_time)

        # Final summary
        console.clear()
        self.show_title()
        console.print("\n[bold cyan]⚔️  BATTLE COMPLETE! ⚔️[/bold cyan]\n")

        # Determine winner
        if ai1_wins > ai2_wins:
            winner_text = f"[bold green]🎉 {ai1.name} WINS THE BATTLE! 🎉[/bold green]"
        elif ai2_wins > ai1_wins:
            winner_text = (
                f"[bold yellow]🎉 {ai2.name} WINS THE BATTLE! 🎉[/bold yellow]"
            )
        else:
            winner_text = "[bold cyan]🤝 IT'S A DRAW! 🤝[/bold cyan]"

        console.print(Panel(winner_text, style="bold"))

        # Final stats table
        final_stats = Table(
            show_header=True, box=box.ROUNDED, style="cyan", title="Final Statistics"
        )
        final_stats.add_column("AI Fighter", style="bold")
        final_stats.add_column("Wins", justify="center")
        final_stats.add_column("Losses", justify="center")
        final_stats.add_column("Ties", justify="center")
        final_stats.add_column("Win Rate", justify="center")

        ai1_total = ai1_wins + ai2_wins + ties
        ai1_win_rate = (ai1_wins / ai1_total * 100) if ai1_total > 0 else 0
        ai2_win_rate = (ai2_wins / ai1_total * 100) if ai1_total > 0 else 0

        final_stats.add_row(
            f"{ai1.name} ({ai1_config['difficulty']})",
            f"[green]{ai1_wins}[/green]",
            f"[red]{ai2_wins}[/red]",
            str(ties),
            f"{ai1_win_rate:.1f}%",
        )
        final_stats.add_row(
            f"{ai2.name} ({ai2_config['difficulty']})",
            f"[green]{ai2_wins}[/green]",
            f"[red]{ai1_wins}[/red]",
            str(ties),
            f"{ai2_win_rate:.1f}%",
        )

        console.print("\n")
        console.print(final_stats)

        # Fun fact about the battle
        total_rounds = ai1_wins + ai2_wins + ties
        if ties > total_rounds * 0.3:
            console.print(
                "\n[yellow]💭 These AIs think alike! High number of ties.[/yellow]"
            )
        elif abs(ai1_wins - ai2_wins) <= 2:
            console.print(
                "\n[yellow]💭 What a close battle! Nearly evenly matched.[/yellow]"
            )
        elif ai1_wins > ai2_wins * 2 or ai2_wins > ai1_wins * 2:
            console.print(
                "\n[yellow]💭 Complete domination! One AI had the perfect strategy.[/yellow]"
            )

        console.print(
            "\n[dim]Note: AI battles are not recorded on the leaderboard.[/dim]"
        )

        Prompt.ask("\nPress Enter to return to main menu")

    def ai_tournament(self):
        """Run a round-robin AI tournament."""
        console.clear()
        self.show_title()

        console.print("\n[bold cyan]🏆 AI TOURNAMENT MODE 🏆[/bold cyan]\n")
        console.print(
            "[yellow]Select AI players to compete in a round-robin tournament![/yellow]"
        )
        console.print("[dim]Each AI will play against every other AI.[/dim]\n")

        # Select number of participants
        num_participants = IntPrompt.ask(
            "How many AI players should compete?", choices=["2", "3", "4"], default=4
        )

        # Select AI participants
        selected_ais = []
        selected_indices = []

        for i in range(num_participants):
            console.clear()
            self.show_title()
            console.print("\n[bold cyan]🏆 AI TOURNAMENT MODE 🏆[/bold cyan]\n")

            if selected_ais:
                console.print("[bold green]Selected Players:[/bold green]")
                for j, ai_info in enumerate(selected_ais, 1):
                    console.print(f"  {j}. {ai_info['name']} ({ai_info['difficulty']})")
                console.print()

            console.print(f"[bold yellow]SELECT PLAYER #{i + 1}:[/bold yellow]\n")

            # Show available AIs (excluding already selected)
            table = Table(show_header=True, box=box.ROUNDED, style="cyan")
            table.add_column("#", style="bold", width=3)
            table.add_column("Name", style="bold yellow")
            table.add_column("Difficulty", style="bold")
            table.add_column("Personality")

            available_choices = []
            for idx, ai in enumerate(AI_OPPONENTS):
                if idx not in selected_indices:
                    difficulty_color = {
                        "Easy": "green",
                        "Medium": "yellow",
                        "Hard": "red",
                    }.get(ai["difficulty"], "white")
                    table.add_row(
                        str(idx + 1),
                        ai["name"],
                        f"[{difficulty_color}]{ai['difficulty']}[/{difficulty_color}]",
                        ai["personality"],
                    )
                    available_choices.append(str(idx + 1))

            console.print(table)

            choice = IntPrompt.ask("\nSelect AI player", choices=available_choices)
            ai_index = choice - 1
            selected_indices.append(ai_index)
            selected_ais.append(AI_OPPONENTS[ai_index])

        # Get number of games per matchup
        console.clear()
        self.show_title()
        console.print("\n[bold cyan]🏆 AI TOURNAMENT MODE 🏆[/bold cyan]\n")

        console.print("[bold green]Tournament Participants:[/bold green]")
        for i, ai_info in enumerate(selected_ais, 1):
            console.print(f"  {i}. {ai_info['name']} ({ai_info['difficulty']})")
        console.print()

        games_per_matchup = IntPrompt.ask("How many games per matchup?", default=10)

        # Calculate total matches
        total_matches = (num_participants * (num_participants - 1)) // 2
        total_games = total_matches * games_per_matchup

        console.print(
            f"\n[yellow]Tournament will consist of {total_matches} matchups ({total_games} total games)[/yellow]"
        )
        time.sleep(2)

        # Initialize tournament stats
        tournament_stats = {}
        for ai_info in selected_ais:
            tournament_stats[ai_info["name"]] = {
                "wins": 0,
                "losses": 0,
                "ties": 0,
                "matches_played": 0,
            }

        # Run all matchups
        matchup_num = 0
        for i in range(len(selected_ais)):
            for j in range(i + 1, len(selected_ais)):
                matchup_num += 1
                ai1_info = selected_ais[i]
                ai2_info = selected_ais[j]

                # Create AI instances
                ai1 = create_ai(selected_indices[i])
                ai2 = create_ai(selected_indices[j])

                console.clear()
                self.show_title()
                console.print(
                    f"\n[bold cyan]🏆 TOURNAMENT - Match {matchup_num}/{total_matches} 🏆[/bold cyan]\n"
                )

                matchup_panel = Panel(
                    f"[bold green]{ai1.name}[/bold green] ({ai1_info['difficulty']})\n"
                    f"     VS\n"
                    f"[bold yellow]{ai2.name}[/bold yellow] ({ai2_info['difficulty']})",
                    title="Current Matchup",
                    style="cyan",
                )
                console.print(matchup_panel)
                console.print("\n[yellow]Playing games...[/yellow]\n")
                time.sleep(1)

                # Play games for this matchup
                ai1_wins = 0
                ai2_wins = 0
                ties = 0
                ai1_history = []
                ai2_history = []

                for game_num in range(games_per_matchup):
                    # AI 1 makes move
                    ai1_move = ai1.make_move(ai2_history)
                    ai1.record_move(ai1_move)
                    ai1_history.append(ai1_move)

                    # AI 2 makes move
                    ai2_move = ai2.make_move(ai1_history)
                    ai2.record_move(ai2_move)
                    ai2_history.append(ai2_move)

                    # Determine winner
                    result = Game.determine_winner(ai1_move, ai2_move)

                    # Update adaptive AIs
                    if isinstance(ai1, AdaptiveAI):
                        if result == GameResult.WIN:
                            ai1.record_win(ai1_move)
                        elif result == GameResult.LOSE:
                            ai1.record_loss(ai1_move)
                    if isinstance(ai2, AdaptiveAI):
                        if result == GameResult.LOSE:  # AI2 won
                            ai2.record_win(ai2_move)
                        elif result == GameResult.WIN:  # AI2 lost
                            ai2.record_loss(ai2_move)

                    # Update scores
                    if result == GameResult.WIN:
                        ai1_wins += 1
                    elif result == GameResult.LOSE:
                        ai2_wins += 1
                    else:
                        ties += 1

                # Update tournament stats
                tournament_stats[ai1.name]["wins"] += ai1_wins
                tournament_stats[ai1.name]["losses"] += ai2_wins
                tournament_stats[ai1.name]["ties"] += ties
                tournament_stats[ai1.name]["matches_played"] += 1

                tournament_stats[ai2.name]["wins"] += ai2_wins
                tournament_stats[ai2.name]["losses"] += ai1_wins
                tournament_stats[ai2.name]["ties"] += ties
                tournament_stats[ai2.name]["matches_played"] += 1

                # Show matchup result
                console.print(f"[bold green]{ai1.name}:[/bold green] {ai1_wins} wins")
                console.print(f"[bold yellow]{ai2.name}:[/bold yellow] {ai2_wins} wins")
                console.print(f"[dim]Ties: {ties}[/dim]")

                if ai1_wins > ai2_wins:
                    console.print(
                        f"\n[bold green]✓ {ai1.name} wins this matchup![/bold green]"
                    )
                elif ai2_wins > ai1_wins:
                    console.print(
                        f"\n[bold yellow]✓ {ai2.name} wins this matchup![/bold yellow]"
                    )
                else:
                    console.print(f"\n[dim]Draw in this matchup![/dim]")

                time.sleep(2)

        # Display final tournament standings
        console.clear()
        self.show_title()
        console.print("\n[bold cyan]🏆 TOURNAMENT FINAL STANDINGS 🏆[/bold cyan]\n")

        # Sort by wins, then by win rate
        standings = []
        for name, stats in tournament_stats.items():
            total_games = stats["wins"] + stats["losses"] + stats["ties"]
            win_rate = (stats["wins"] / total_games * 100) if total_games > 0 else 0
            standings.append(
                {
                    "name": name,
                    "wins": stats["wins"],
                    "losses": stats["losses"],
                    "ties": stats["ties"],
                    "total": total_games,
                    "win_rate": win_rate,
                }
            )

        standings.sort(key=lambda x: (x["wins"], x["win_rate"]), reverse=True)

        # Display standings table
        standings_table = Table(
            show_header=True, box=box.ROUNDED, style="cyan", title="Final Standings"
        )
        standings_table.add_column("Rank", style="bold", width=6)
        standings_table.add_column("Player", style="bold yellow")
        standings_table.add_column("Wins", justify="center", style="green")
        standings_table.add_column("Losses", justify="center", style="red")
        standings_table.add_column("Ties", justify="center")
        standings_table.add_column("Total", justify="center")
        standings_table.add_column("Win Rate", justify="center")

        for i, player in enumerate(standings, 1):
            rank_emoji = {1: "🥇", 2: "🥈", 3: "🥉", 4: "4th"}.get(i, f"{i}.")
            standings_table.add_row(
                rank_emoji,
                player["name"],
                str(player["wins"]),
                str(player["losses"]),
                str(player["ties"]),
                str(player["total"]),
                f"{player['win_rate']:.1f}%",
            )

        console.print(standings_table)

        # Announce winner
        winner = standings[0]
        console.print(
            f"\n[bold green]🎉 TOURNAMENT CHAMPION: {winner['name']}! 🎉[/bold green]"
        )
        console.print(
            f"[green]With {winner['wins']} wins and a {winner['win_rate']:.1f}% win rate![/green]"
        )

        console.print(
            "\n[dim]Note: Tournament results are not recorded on the leaderboard.[/dim]"
        )

        Prompt.ask("\nPress Enter to return to main menu")

    def run(self):
        """Main game loop."""
        while True:
            try:
                choice = self.main_menu()

                if choice == "1":
                    self.play_vs_ai()
                elif choice == "2":
                    self.play_vs_human()
                elif choice == "3":
                    self.ai_vs_ai_battle()
                elif choice == "4":
                    self.ai_tournament()
                elif choice == "5":
                    self.view_leaderboard()
                elif choice == "6":
                    self.view_player_stats()
                elif choice == "7":
                    console.clear()
                    console.print(
                        "\n[bold cyan]Thanks for playing! See you next time! 👋[/bold cyan]\n"
                    )
                    break
            except KeyboardInterrupt:
                console.print("\n\n[yellow]Game interrupted. Goodbye![/yellow]\n")
                break


def main():
    """Entry point."""
    game = RockPaperScissorsGame()
    game.run()


if __name__ == "__main__":
    main()
