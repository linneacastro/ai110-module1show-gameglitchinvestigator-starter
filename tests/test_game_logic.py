from logic_utils import (
    apply_guess,
    check_guess,
    get_attempt_limit_for_difficulty,
    get_guess_input_key,
    get_range_for_difficulty,
    is_duplicate_guess,
    new_game_state,
)


def test_winning_guess():
    outcome, message = check_guess(50, 50)

    assert outcome == "Win"
    assert "Correct" in message


def test_check_guess_reports_high_and_low_in_correct_direction():
    too_high_outcome, too_high_message = check_guess(60, 50)
    too_low_outcome, too_low_message = check_guess(40, 50)

    assert too_high_outcome == "Too High"
    assert "LOWER" in too_high_message
    assert too_low_outcome == "Too Low"
    assert "HIGHER" in too_low_message


def test_is_duplicate_guess_rejects_repeated_number():
    history = [10, 99, 42]

    assert is_duplicate_guess(99, history) is True


def test_is_duplicate_guess_accepts_new_number():
    history = [10, 99, 42]

    assert is_duplicate_guess(7, history) is False


def test_attempt_limit_matches_selected_difficulty():
    assert get_attempt_limit_for_difficulty("Easy") == 8
    assert get_attempt_limit_for_difficulty("Normal") == 6
    assert get_attempt_limit_for_difficulty("Hard") == 5


def test_difficulty_ranges_scale_with_difficulty():
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 50)
    assert get_range_for_difficulty("Hard") == (1, 100)


def test_new_game_state_resets_fields_and_picks_secret_in_range():
    calls = []

    def fake_randint(low, high):
        calls.append((low, high))
        return 17

    state = new_game_state(
        "Easy",
        previous_game_number=2,
        randint_func=fake_randint,
    )

    assert calls == [(1, 20)]
    assert state == {
        "secret": 17,
        "attempts": 0,
        "score": 0,
        "status": "playing",
        "history": [],
        "game_number": 3,
    }


def test_guess_input_key_changes_for_each_new_game():
    first_key = get_guess_input_key("Normal", 1)
    second_key = get_guess_input_key("Normal", 2)

    assert first_key == "guess_input_Normal_1"
    assert second_key == "guess_input_Normal_2"
    assert first_key != second_key


def test_apply_guess_stores_first_guess_in_history_and_increments_attempts():
    state = {
        "secret": 42,
        "attempts": 0,
        "score": 0,
        "status": "playing",
        "history": [],
    }

    result = apply_guess("30", state, attempt_limit=6)

    assert result["kind"] == "continue"
    assert state["history"] == [30]
    assert state["attempts"] == 1


def test_apply_guess_duplicate_does_not_change_history_or_attempts():
    state = {
        "secret": 42,
        "attempts": 1,
        "score": -5,
        "status": "playing",
        "history": [30],
    }

    result = apply_guess("30", state, attempt_limit=6)

    assert result["kind"] == "duplicate"
    assert state["history"] == [30]
    assert state["attempts"] == 1


def test_apply_guess_reaching_limit_marks_game_lost():
    state = {
        "secret": 50,
        "attempts": 5,
        "score": 0,
        "status": "playing",
        "history": [10, 20, 30, 40, 45],
    }

    result = apply_guess("49", state, attempt_limit=6)

    assert result["kind"] == "lost"
    assert state["status"] == "lost"
    assert state["attempts"] == 6


def test_apply_guess_correct_on_final_attempt_marks_game_won():
    state = {
        "secret": 23,
        "attempts": 5,
        "score": 0,
        "status": "playing",
        "history": [1, 5, 8, 13, 21],
    }

    result = apply_guess("23", state, attempt_limit=6)

    assert result["kind"] == "won"
    assert state["status"] == "won"
    assert state["attempts"] == 6
    assert state["history"][-1] == 23


def test_apply_guess_rejects_decimal_input_without_using_attempt():
    state = {
        "secret": 42,
        "attempts": 0,
        "score": 0,
        "status": "playing",
        "history": [],
    }

    result = apply_guess("12.5", state, attempt_limit=6, guess_range=(1, 50))

    assert result["kind"] == "error"
    assert "whole number" in result["message"]
    assert state["attempts"] == 0
    assert state["history"] == []


def test_apply_guess_rejects_negative_number_out_of_range():
    state = {
        "secret": 42,
        "attempts": 0,
        "score": 0,
        "status": "playing",
        "history": [],
    }

    result = apply_guess("-7", state, attempt_limit=6, guess_range=(1, 50))

    assert result["kind"] == "error"
    assert "between 1 and 50" in result["message"]
    assert state["attempts"] == 0
    assert state["history"] == []


def test_apply_guess_rejects_extremely_large_number_without_crashing():
    state = {
        "secret": 42,
        "attempts": 0,
        "score": 0,
        "status": "playing",
        "history": [],
    }

    result = apply_guess("999999999999999999999999", state, attempt_limit=6, guess_range=(1, 50))

    assert result["kind"] == "error"
    assert "too large" in result["message"]
    assert state["attempts"] == 0
    assert state["history"] == []
