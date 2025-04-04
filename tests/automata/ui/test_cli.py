import pytest

from automata.models import InternalGameState, TurnResult


@pytest.fixture
def mock_load_game_state(monkeypatch):
    """Mock the load_game_state function."""

    # Create a mock object that we can check call counts on
    class MockLoadGameState:
        def __init__(self):
            self.call_count = 0
            self.result = InternalGameState()
            pass

        def __call__(self):
            self.call_count += 1
            return self.result

    mock_load_game_state = MockLoadGameState()
    monkeypatch.setattr("automata.ui.cli.load_game_state", mock_load_game_state)
    return mock_load_game_state


@pytest.fixture
def mock_save_game_state(monkeypatch):
    """Mock the save_game_state function."""

    class MockSaveGameState:
        def __init__(self):
            self.call_count = 0
            self.calls = []
            self.state = InternalGameState()

        def __call__(self, game_state: InternalGameState):
            self.call_count += 1
            self.calls.append(game_state)
            self.state = game_state

    mock_save = MockSaveGameState()
    monkeypatch.setattr("automata.ui.cli.save_game_state", mock_save)
    return mock_save


@pytest.fixture
def mock_play_turn(monkeypatch):
    """Mock the play_turn function."""
    result = TurnResult(
        player_choice="rock",
        computer_choice="scissors",
        outcome="win",
        reason="You win. I'll allow it this time.. Rock crushes Scissors",
    )

    # Create a mock object that we can check call counts on
    class MockPlayTurn:
        def __init__(self):
            self.call_count = 0
            self.calls = []
            self.result = result
            pass

        def __call__(self, player_choice, game_state):
            self.call_count += 1
            self.calls.append((player_choice, game_state))
            game_state.turn_history.append(player_choice)
            game_state.score += 1
            return result, game_state

    mock_play = MockPlayTurn()
    monkeypatch.setattr("automata.ui.cli.play_turn", mock_play)
    return mock_play
