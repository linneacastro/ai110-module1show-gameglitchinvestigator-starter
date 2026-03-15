from logic_utils import check_guess


def test_winning_guess():
    outcome, message = check_guess(50, 50)

    assert outcome == "Win"
    assert "Correct" in message


#FIX: Had Copilot Agent Mode Fix this Test
def test_check_guess_reports_high_and_low_in_correct_direction():
    too_high_outcome, too_high_message = check_guess(60, 50)
    too_low_outcome, too_low_message = check_guess(40, 50)

    assert too_high_outcome == "Too High"
    assert "LOWER" in too_high_message
    assert too_low_outcome == "Too Low"
    assert "HIGHER" in too_low_message
