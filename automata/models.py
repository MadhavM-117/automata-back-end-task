from typing import List, Literal, Optional, TypeAlias

from pydantic import BaseModel

TurnOption: TypeAlias = Literal["rock", "paper", "scissors", "lizard", "spock"]
TurnOutcome: TypeAlias = Literal["win", "lose", "tie"]


class DisplayGameState(BaseModel):
    username: Optional[str] = None
    score: int = 0


class InternalGameState(DisplayGameState):
    turn_history: List[TurnOption] = []


class TurnResult(BaseModel):
    player_choice: TurnOption
    computer_choice: TurnOption
    outcome: TurnOutcome
    reason: str
