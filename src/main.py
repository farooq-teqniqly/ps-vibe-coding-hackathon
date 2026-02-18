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
        menu.add_row("3", "🏆 View Leaderboard")
        menu.add_row("4", "📊 View Your Stats")
        menu.add_row("5", "👋 Quit")

        console.print(menu)
        choice = Prompt.ask("\nChoose an option", choices=["1", "2", "3", "4", "5"])
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
        """Display the result of a round."""
        console.print("\n" + "=" * 50)

        # Show moves
        moves_table = Table(show_header=False, box=None, padding=(0, 2))
        moves_table.add_column(justify="center")
        moves_table.add_column(justify="center")
        moves_table.add_column(justify="center")

        moves_table.add_row(
            f"[bold cyan]{player1_name}[/bold cyan]",
            "[bold]VS[/bold]",
            f"[bold yellow]{player2_name}[/bold yellow]",
        )
        moves_table.add_row(
            f"{Game.get_move_emoji(player1_move)} {player1_move}",
            "⚔️",
            f"{Game.get_move_emoji(player2_move)} {player2_move}",
        )

        console.print(moves_table)

        # Show result
        if result == GameResult.WIN:
            console.print(f"\n[bold green]🎉 {player1_name} WINS![/bold green]")
        elif result == GameResult.LOSE:
            console.print(f"\n[bold red]😢 {player2_name} WINS![/bold red]")
        else:
            console.print("\n[bold yellow]🤝 IT'S A TIE![/bold yellow]")

        console.print("=" * 50 + "\n")
        time.sleep(1.5)

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
                    self.view_leaderboard()
                elif choice == "4":
                    self.view_player_stats()
                elif choice == "5":
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
