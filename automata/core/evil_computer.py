import random
from typing import List

from automata.models import TurnOption


def get_computer_choice() -> TurnOption:
    """Generate a random choice for the computer."""
    options: List[TurnOption] = ["rock", "paper", "scissors", "lizard", "spock"]
    return random.choice(options)
