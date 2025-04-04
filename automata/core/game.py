from typing import Dict, List, Tuple

from automata.core.evil_computer import get_computer_choice
from automata.core.storage import save_game_state
from automata.models import InternalGameState, TurnOption, TurnResult

# Defines the rules of the game - which option beats which
GAME_RULES: Dict[TurnOption, List[TurnOption]] = {
    "rock": ["scissors", "lizard"],
    "paper": ["rock", "spock"],
    "scissors": ["paper", "lizard"],
    "lizard": ["paper", "spock"],
    "spock": ["scissors", "rock"],
}


def get_outcome_reason(*, winner: TurnOption, loser: TurnOption) -> str:
    """Get the reason for the outcome based on winner and loser choices."""
    if winner == "scissors" and loser == "paper":
        return "Scissors cuts Paper"
    if winner == "scissors" and loser == "lizard":
        return "Scissors decapitates Lizard"
    if winner == "paper" and loser == "rock":
        return "Paper covers Rock"
    if winner == "paper" and loser == "spock":
        return "Paper disproves Spock"
    if winner == "rock" and loser == "scissors":
        return "Rock crushes Scissors"
    if winner == "rock" and loser == "lizard":
        return "Rock crushes Lizard"
    if winner == "lizard" and loser == "paper":
        return "Lizard eats Paper"
    if winner == "lizard" and loser == "spock":
        return "Lizard poisons Spock"
    if winner == "spock" and loser == "scissors":
        return "Spock smashes Scissors"
    if winner == "spock" and loser == "rock":
        return "Spock vaporizes Rock"
    return "Wait. Something has gone terribly wrong."


def is_valid_turn(*, player_choice: TurnOption) -> bool:
    """Validate that the player's choice is one of the allowed options."""
    valid_options: List[TurnOption] = ["rock", "paper", "scissors", "lizard", "spock"]
    return player_choice in valid_options


def determine_turn_outcome(
    *, player_choice: TurnOption, computer_choice: TurnOption
) -> TurnResult:
    """Determine the outcome of a turn based on player and computer choices."""
    # If both choices are the same, it's a tie
    if player_choice == computer_choice:
        return TurnResult(
            player_choice=player_choice,
            computer_choice=computer_choice,
            outcome="tie",
            reason="Tie - we are both the same. How boring..",
        )

    # Check if player wins
    if computer_choice in GAME_RULES[player_choice]:
        return TurnResult(
            player_choice=player_choice,
            computer_choice=computer_choice,
            outcome="win",
            reason="You win. I'll allow it this time.. "
            + get_outcome_reason(winner=player_choice, loser=computer_choice),
        )

    # Computer wins
    return TurnResult(
        player_choice=player_choice,
        computer_choice=computer_choice,
        outcome="lose",
        reason="Ha! Victory is mine! "
        + get_outcome_reason(winner=computer_choice, loser=player_choice),
    )


def play_turn(
    *, player_choice: TurnOption, game_state: InternalGameState
) -> Tuple[TurnResult, InternalGameState]:
    """Play a turn and update the game state."""

    if not is_valid_turn(player_choice=player_choice):
        return TurnResult(
            player_choice=None,
            computer_choice=None,
            outcome="tie",
            reason="No cheating this time! Be better.",
        ), game_state

    # Get the computer's choice
    computer_choice = get_computer_choice()

    # Determine the outcome
    result = determine_turn_outcome(
        player_choice=player_choice, computer_choice=computer_choice
    )

    game_state.turn_history.append(player_choice)

    # Update the score based on the outcome
    if result.outcome == "win":
        game_state.score += 1

    elif result.outcome == "lose":
        game_state.score -= 1

    # Save the updated game state
    save_game_state(game_state)

    return result, game_state
