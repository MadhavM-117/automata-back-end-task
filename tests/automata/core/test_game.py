import pytest

from automata.core.game import (
    GAME_RULES,
    determine_turn_outcome,
    get_outcome_reason,
    is_valid_turn,
    play_turn,
)
from automata.models import InternalGameState


@pytest.fixture
def mock_save_game_state(monkeypatch):
    calls = []

    def mock_save(game_state):
        calls.append(game_state)

    monkeypatch.setattr("automata.core.game.save_game_state", mock_save)
    return calls


@pytest.fixture
def mock_computer_choice(monkeypatch):
    class MockChoice:
        def __init__(self):
            self.return_value = None
            self.called = False

        def __call__(self):
            self.called = True
            return self.return_value

    mock = MockChoice()
    monkeypatch.setattr("automata.core.game.get_computer_choice", mock)
    return mock


def test_is_valid_turn():
    # Test valid turns
    assert is_valid_turn(player_choice="rock") is True
    assert is_valid_turn(player_choice="paper") is True
    assert is_valid_turn(player_choice="scissors") is True
    assert is_valid_turn(player_choice="lizard") is True
    assert is_valid_turn(player_choice="spock") is True

    # Test invalid turns
    assert is_valid_turn(player_choice="invalid") is False  # type: ignore


@pytest.mark.parametrize(
    "winner,loser,expected_reason",
    [
        ("scissors", "paper", "Scissors cuts Paper"),
        ("scissors", "lizard", "Scissors decapitates Lizard"),
        ("paper", "rock", "Paper covers Rock"),
        ("paper", "spock", "Paper disproves Spock"),
        ("rock", "scissors", "Rock crushes Scissors"),
        ("rock", "lizard", "Rock crushes Lizard"),
        ("lizard", "paper", "Lizard eats Paper"),
        ("lizard", "spock", "Lizard poisons Spock"),
        ("spock", "scissors", "Spock smashes Scissors"),
        ("spock", "rock", "Spock vaporizes Rock"),
        ("rock", "paper", "Wait. Something has gone terribly wrong."),
    ],
)
def test_get_outcome_reason(winner, loser, expected_reason):
    assert get_outcome_reason(winner=winner, loser=loser) == expected_reason


def test_determine_turn_outcome_tie():
    # Test tie scenario
    result = determine_turn_outcome(player_choice="rock", computer_choice="rock")
    assert result.outcome == "tie"
    assert result.player_choice == "rock"
    assert result.computer_choice == "rock"
    assert result.reason == "Tie - we are both the same. How boring.."


@pytest.mark.parametrize(
    "player_choice,computer_choice",
    [(player, computer) for player, beats in GAME_RULES.items() for computer in beats],
)
def test_determine_turn_outcome_win(player_choice, computer_choice):
    result = determine_turn_outcome(
        player_choice=player_choice, computer_choice=computer_choice
    )
    assert result.outcome == "win"
    assert result.player_choice == player_choice
    assert result.computer_choice == computer_choice
    assert "You win" in result.reason
    assert (
        get_outcome_reason(winner=player_choice, loser=computer_choice) in result.reason
    )


@pytest.mark.parametrize(
    "player_choice,computer_choice",
    [(player, computer) for computer, beats in GAME_RULES.items() for player in beats],
)
def test_determine_turn_outcome_lose(player_choice, computer_choice):
    result = determine_turn_outcome(
        player_choice=player_choice, computer_choice=computer_choice
    )
    assert result.outcome == "lose"
    assert result.player_choice == player_choice
    assert result.computer_choice == computer_choice
    assert "Ha! Victory is mine!" in result.reason
    assert (
        get_outcome_reason(winner=computer_choice, loser=player_choice) in result.reason
    )


def test_play_turn_invalid_choice(mock_save_game_state, mock_computer_choice):
    # Test playing with an invalid choice
    game_state = InternalGameState(score=0, turn_history=[])
    result, updated_state = play_turn(player_choice="invalid", game_state=game_state)  # type: ignore

    assert result.player_choice is None
    assert result.computer_choice is None
    assert result.outcome == "tie"
    assert result.reason == "No cheating this time! Be better."
    assert updated_state == game_state  # State should not change
    assert not mock_computer_choice.called  # Computer choice should not be called
    assert len(mock_save_game_state) == 0  # State should not be saved


def test_play_turn_win(mock_save_game_state, mock_computer_choice):
    # Test playing and winning
    mock_computer_choice.return_value = "scissors"
    game_state = InternalGameState(score=0, turn_history=[])

    result, updated_state = play_turn(player_choice="rock", game_state=game_state)

    assert result.outcome == "win"
    assert updated_state.score == 1  # Score should increment
    assert updated_state.turn_history == ["rock"]  # Turn should be recorded
    assert mock_computer_choice.called  # Computer choice should be called
    assert len(mock_save_game_state) == 1  # State should be saved
    assert (
        mock_save_game_state[0] == updated_state
    )  # Saved state should match updated state


def test_play_turn_lose(mock_save_game_state, mock_computer_choice):
    # Test playing and losing
    mock_computer_choice.return_value = "paper"
    game_state = InternalGameState(score=0, turn_history=[])

    result, updated_state = play_turn(player_choice="rock", game_state=game_state)

    assert result.outcome == "lose"
    assert updated_state.score == -1  # Score should decrement
    assert updated_state.turn_history == ["rock"]  # Turn should be recorded
    assert mock_computer_choice.called  # Computer choice should be called
    assert len(mock_save_game_state) == 1  # State should be saved
    assert (
        mock_save_game_state[0] == updated_state
    )  # Saved state should match updated state


def test_play_turn_tie(mock_save_game_state, mock_computer_choice):
    # Test playing and tying
    mock_computer_choice.return_value = "rock"
    game_state = InternalGameState(score=0, turn_history=[])

    result, updated_state = play_turn(player_choice="rock", game_state=game_state)

    assert result.outcome == "tie"
    assert updated_state.score == 0  # Score should not change
    assert updated_state.turn_history == ["rock"]  # Turn should be recorded
    assert mock_computer_choice.called  # Computer choice should be called
    assert len(mock_save_game_state) == 1  # State should be saved
    assert (
        mock_save_game_state[0] == updated_state
    )  # Saved state should match updated state
