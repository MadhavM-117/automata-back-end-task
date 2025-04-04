import random

import pytest

from automata.core.evil_computer import get_computer_choice


@pytest.fixture
def mock_random_choice(monkeypatch):
    class MockChoice:
        def __init__(self):
            self.return_value = None
            self.called = False
            self.calls = []

        def __call__(self, choices):
            self.called = True
            self.calls.append(choices)
            return self.return_value

    mock = MockChoice()
    monkeypatch.setattr(random, "choice", mock)
    return mock


def test_get_computer_choice_returns_valid_option():
    # Test that get_computer_choice returns a valid TurnOption
    result = get_computer_choice()
    valid_options = ["rock", "paper", "scissors", "lizard", "spock"]
    assert result in valid_options


def test_get_computer_choice_uses_random_choice(mock_random_choice):
    # Test that random.choice is used to make the selection
    mock_random_choice.return_value = "rock"

    result = get_computer_choice()
    assert result == "rock"
