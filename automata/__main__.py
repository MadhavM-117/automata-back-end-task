import sys
import time

from automata.logging import setup_logging
from automata.ui.cli import start_game


def main():
    setup_logging()
    try:
        start_game()
    except KeyboardInterrupt:
        print("\nOh. Did you want to leave? Too bad!")
        time.sleep(2)
        try:
            start_game()
        except KeyboardInterrupt:
            print("\nWell, Goodbye to you too!")
            sys.exit(0)
    except Exception:
        print(
            "\nWe seem to have run into a tiny bug. We'll be right back with the exterminators."
        )
        sys.exit(0)


if __name__ == "__main__":
    main()

