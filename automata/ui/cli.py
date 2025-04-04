import os
import shutil
import sys
from typing import List, Literal, Optional, Union, cast

from automata.core.game import play_turn
from automata.core.storage import load_game_state, save_game_state
from automata.logging import get_logger
from automata.models import InternalGameState, TurnOption

logger = get_logger("ui")

VALID_OPTIONS: List[TurnOption] = ["rock", "paper", "scissors", "lizard", "spock"]


def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def get_screen_width() -> int:
    cols, _ = shutil.get_terminal_size()
    return min(cols, 75)


def print_title() -> None:
    """Print the game title."""
    width = get_screen_width()
    print("\n" + "=" * width)
    print(f"{'ROCK, PAPER, SCISSORS, LIZARD, SPOCK':^{width}}")
    print("=" * width + "\n")


def print_options() -> None:
    """Print the available options."""
    print("\nChoose your move:")
    for i, option in enumerate(VALID_OPTIONS, 1):
        print(f"{i}. {option.capitalize()}")

    print("\nGame Options")
    print("R. Restart Game")
    print("L. Log out of Game")
    print("Q. Quit Game")


def print_score(game_state: InternalGameState) -> None:
    """Print the current score."""
    username = game_state.username or "Player"
    print(f"Hello {username},")
    print(f"\nScore: {game_state.score}")
    print(f"Rounds played: {len(game_state.turn_history)}")


def get_player_choice() -> Optional[Union[TurnOption, Literal["restart", "log_out"]]]:
    """Get the player's choice from input."""
    while True:
        choice = input("\nEnter your choice (1-5, R, L, Q): ").strip().lower()

        if choice == "q":
            print("\nThanks for playing! Goodbye.")
            sys.exit(0)

        if choice == "l":
            return "log_out"

        if choice == "r":
            return "restart"

        if choice.isdigit() and 1 <= int(choice) <= 5:
            return VALID_OPTIONS[int(choice) - 1]

        clear_screen()
        print("Invalid choice. Please try again.")
        print_options()


def ask_for_username(current_username: Optional[str]) -> str:
    """Ask the user for a username."""
    default = current_username or "Player"
    username = input(f"\nEnter your username [{default}]: ").strip()
    return username if username else default


def log_out_of_game() -> InternalGameState:
    """log_out the game, and start as a new user"""
    username = ask_for_username(None)
    new_state = InternalGameState(username=username, score=0, turn_history=[])
    save_game_state(new_state)
    return new_state


def restart_game(game_state: InternalGameState) -> InternalGameState:
    """Restart the game with a fresh state, but same user"""
    username = game_state.username or ask_for_username(None)
    new_state = InternalGameState(username=username, score=0, turn_history=[])
    save_game_state(new_state)
    return new_state


def display_result(result_text: str) -> None:
    """Display the result of the turn with some visual emphasis."""
    print("\n" + "-" * get_screen_width())
    print(result_text)
    print("-" * get_screen_width())
    input("\nPress Enter to continue...")


def start_game() -> None:
    """Start the game and manage the main game loop."""
    # Load existing game state or create a new one
    game_state = load_game_state()

    # If this is a new game, ask for username
    if not game_state.username:
        game_state.username = ask_for_username(None)
        save_game_state(game_state)

    while True:
        clear_screen()
        print_title()
        print_score(game_state)
        print_options()

        player_choice = get_player_choice()

        # Restart the game if requested
        if player_choice == "restart":
            game_state = restart_game(game_state)
            continue

        # Log out of the game if requested
        if player_choice == "log_out":
            game_state = log_out_of_game()
            continue

        player_choice = cast(TurnOption, player_choice)
        # Play the turn and get the result
        result, game_state = play_turn(
            player_choice=player_choice, game_state=game_state
        )

        # Display the result
        result_message = (
            f"      Your choice: {result.player_choice}\n"
            f"Computer's choice: {result.computer_choice}\n\n"
            f"{result.reason}"
        )
        display_result(result_message)
