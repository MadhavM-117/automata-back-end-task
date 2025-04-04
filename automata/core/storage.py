import tempfile
import traceback
from os import path

from pydantic import ValidationError

from automata.logging import get_logger
from automata.models import InternalGameState

logger = get_logger("storage")


def get_state_file_path() -> str:
    return path.join(tempfile.gettempdir(), "automata-game_state.json")


def load_game_state() -> InternalGameState:
    state_file = get_state_file_path()
    game_state = InternalGameState()

    if path.exists(state_file):
        with open(get_state_file_path()) as file:
            content = file.read()
            try:
                game_state = InternalGameState.model_validate_json(content)
            except ValidationError:
                logger.warning(
                    f"Failed to load game state from file. {traceback.format_exc()}"
                )
            except Exception:
                logger.warning(f"Unexpected error. {traceback.format_exc()}")

    return game_state


def save_game_state(*, game_state: InternalGameState) -> None:
    state_file = get_state_file_path()
    with open(state_file, "w") as file:
        try:
            file.write(game_state.model_dump_json())
            file.flush()
        except Exception:
            logger.error(
                f"Unexpected error while saving state. {traceback.format_exc()}"
            )
