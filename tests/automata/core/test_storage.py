import tempfile

import pytest

from automata.core.storage import get_state_file_path, load_game_state, save_game_state
from automata.models import InternalGameState


@pytest.fixture
def mock_path_exists(monkeypatch):
    def set_exists(value):
        def mock_exists(path):
            return value

        monkeypatch.setattr("automata.core.storage.path.exists", mock_exists)

    return set_exists


@pytest.fixture
def mock_open_file(monkeypatch):
    class MockFile:
        def __init__(self, path, mode="r"):
            self.path = path
            self.mode = mode
            self.closed = False
            self.file_content = ""
            self.written_content = []

        def __enter__(self):
            return self

        def __exit__(self, *args):
            self.closed = True

        def read(self):
            return self.file_content

        def write(self, content):
            self.written_content.append(content)

    mock_file = MockFile("")

    def mock_open(path, mode="r"):
        mock_file.path = path
        mock_file.mode = mode
        return mock_file

    monkeypatch.setattr("builtins.open", mock_open)

    return mock_file


@pytest.fixture
def mock_logger(monkeypatch):
    class MockLogger:
        def __init__(self):
            self.warning_calls = []
            self.error_calls = []

        def warning(self, message):
            self.warning_calls.append(message)

        def error(self, message):
            self.error_calls.append(message)

    logger = MockLogger()
    monkeypatch.setattr("automata.core.storage.logger", logger)
    return logger


def test_get_state_file_path():
    # Test that the file path is in the temp directory
    file_path = get_state_file_path()
    assert file_path.startswith(tempfile.gettempdir())
    assert file_path.endswith("automata-game_state.json")


def test_load_game_state_file_not_exists(mock_path_exists):
    # Test loading when file doesn't exist
    mock_path_exists(False)
    state = load_game_state()

    # Should return default state
    assert state.score == 0
    assert state.turn_history == []
    assert state.username is None


def test_load_game_state_valid_file(mock_path_exists, mock_open_file):
    # Test loading valid state from file
    mock_path_exists(True)

    # Set the file content
    json_content = (
        '{"score": 5, "turn_history": ["rock", "paper"], "username": "testuser"}'
    )
    mock_open_file.file_content = json_content

    state = load_game_state()

    # Should return loaded state
    assert state.score == 5
    assert state.turn_history == ["rock", "paper"]
    assert state.username == "testuser"


def test_load_game_state_invalid_json(mock_path_exists, mock_open_file, mock_logger):
    # Test loading with invalid JSON file
    mock_path_exists(True)

    # Set invalid file content
    mock_open_file.file_content = "invalid json"

    state = load_game_state()

    # Should return default state and log warning
    assert state.score == 0
    assert state.turn_history == []
    assert state.username is None
    assert len(mock_logger.warning_calls) == 1


def test_save_game_state(mock_open_file):
    # Test saving game state
    state = InternalGameState(
        score=10, turn_history=["rock", "paper", "scissors"], username="player1"
    )
    save_game_state(game_state=state)

    # Check that the correct JSON was written
    assert len(mock_open_file.written_content) == 1
    expected_json = state.model_dump_json()
    assert mock_open_file.written_content[0] == expected_json


def test_save_game_state_exception(mock_open_file, mock_logger):
    def write(self, content):
        raise Exception("test")

    mock_open_file.write = write
    # Test exception handling when saving state
    state = InternalGameState(score=10, turn_history=["rock"], username="player1")
    save_game_state(game_state=state)

    # Should log error
    assert len(mock_logger.error_calls) == 1
