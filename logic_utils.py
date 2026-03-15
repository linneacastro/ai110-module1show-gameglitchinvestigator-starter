import random
from typing import Any, Callable, Iterable, MutableMapping


DIFFICULTY_SETTINGS = {
    "Easy": {"range": (1, 20), "attempts": 8},
    "Normal": {"range": (1, 50), "attempts": 6},
    "Hard": {"range": (1, 100), "attempts": 5},
}


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    settings = DIFFICULTY_SETTINGS.get(difficulty, DIFFICULTY_SETTINGS["Normal"])
    return settings["range"]


def get_attempt_limit_for_difficulty(difficulty: str) -> int:
    """Return the maximum number of attempts for a difficulty."""
    settings = DIFFICULTY_SETTINGS.get(difficulty, DIFFICULTY_SETTINGS["Normal"])
    return settings["attempts"]


def get_guess_input_key(difficulty: str, game_number: int) -> str:
    """Return a unique text input key for the current game instance."""
    return f"guess_input_{difficulty}_{game_number}"


def new_game_state(
    difficulty: str,
    previous_game_number: int = 0,
    randint_func: Callable[[int, int], int] | None = None,
):
    """Return fresh game state for a new round."""
    low, high = get_range_for_difficulty(difficulty)
    random_number = randint_func or random.randint

    return {
        "secret": random_number(low, high),
        "attempts": 0,
        "score": 0,
        "status": "playing",
        "history": [],
        "game_number": previous_game_number + 1,
    }


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def is_duplicate_guess(guess: int, history: Iterable[Any]) -> bool:
    """Return True if a numeric guess has already been seen in history."""
    for previous in history:
        try:
            if int(previous) == int(guess):
                return True
        except (TypeError, ValueError):
            continue
    return False


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    guess_value = int(guess)
    secret_value = int(secret)

    if guess_value == secret_value:
        return "Win", "🎉 Correct!"

    if guess_value > secret_value:
        return "Too High", "📉 Go LOWER!"

    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score


def apply_guess(
    raw_guess: str,
    game_state: MutableMapping[str, Any],
    attempt_limit: int,
):
    """
    Apply one guess to game state and return structured result metadata.

    Returns a dict with keys:
    - kind: one of "error", "duplicate", "continue", "won", "lost"
    - message: user-facing message for "error" and "duplicate"
    - hint_message: user-facing hint after valid guesses
    - outcome: logical outcome label, e.g. "Win", "Too High", "Too Low"
    """
    ok, guess_int, err = parse_guess(raw_guess)
    if not ok:
        return {
            "kind": "error",
            "message": err,
            "hint_message": None,
            "outcome": None,
        }

    history = game_state.setdefault("history", [])
    if is_duplicate_guess(guess_int, history):
        return {
            "kind": "duplicate",
            "message": (
                f"You already guessed {guess_int}. "
                "Please enter a number you have not guessed before."
            ),
            "hint_message": None,
            "outcome": None,
        }

    history.append(guess_int)
    game_state["attempts"] = int(game_state.get("attempts", 0)) + 1

    outcome, hint_message = check_guess(guess_int, game_state["secret"])
    game_state["score"] = update_score(
        current_score=int(game_state.get("score", 0)),
        outcome=outcome,
        attempt_number=game_state["attempts"],
    )

    if outcome == "Win":
        game_state["status"] = "won"
        return {
            "kind": "won",
            "message": None,
            "hint_message": hint_message,
            "outcome": outcome,
        }

    if game_state["attempts"] >= attempt_limit:
        game_state["status"] = "lost"
        return {
            "kind": "lost",
            "message": None,
            "hint_message": hint_message,
            "outcome": outcome,
        }

    return {
        "kind": "continue",
        "message": None,
        "hint_message": hint_message,
        "outcome": outcome,
    }
