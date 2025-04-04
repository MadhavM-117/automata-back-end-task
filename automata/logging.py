import logging
import os
import tempfile
from datetime import datetime
from typing import Optional


def get_log_file_path():
    date = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    temp_dir = tempfile.gettempdir()
    return os.path.join(temp_dir, f"automata-logs_{date}.log")


def setup_logging(log_file=None, log_level=logging.ERROR):
    """
    Set up a logger with the given name, log file and level
    """
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)

    file_handler = logging.FileHandler(log_file or get_log_file_path())
    file_handler.setLevel(logging.DEBUG)

    logging.basicConfig(
        format="[%(asctime)s] automata/%(name)s/%(levelname)s: %(message)s",
        handlers=[stream_handler, file_handler],
    )


def get_logger(name="core", level: Optional[int | str] = None):
    """
    Get a logger with the given name
    """
    logger = logging.getLogger(name)

    if level:
        logger.setLevel(level)

    return logger
