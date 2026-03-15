from logic_utils import check_guess, is_duplicate_guess


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
