import os
import sys


def _set_token():
    # TODO: Why Windows environment variables are not working?
    with open("genius_token.txt", "r") as f:
        GENIUS_TOKEN = f.read()
    os.environ["GENIUS_TOKEN"] = GENIUS_TOKEN


def get_token():
    _set_token()
    try:
        GENIUS_TOKEN = os.environ["GENIUS_TOKEN"]
        print(f"TOKEN: {GENIUS_TOKEN}")
        return GENIUS_TOKEN
    except KeyError:
        # I cannot share my token, sorry not sorry
        print("Please set the environment variable GENIUS_TOKEN")
        sys.exit(1)


if __name__ == "__main__":
    _set_token()
