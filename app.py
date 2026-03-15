import streamlit as st
from logic_utils import (
    apply_guess,
    get_attempt_limit_for_difficulty,
    get_guess_input_key,
    get_range_for_difficulty,
    new_game_state,
)

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit = get_attempt_limit_for_difficulty(difficulty)

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "game_number" not in st.session_state:
    st.session_state.game_number = 0

if "difficulty" not in st.session_state or "secret" not in st.session_state:
    st.session_state.update(
        new_game_state(difficulty, previous_game_number=st.session_state.game_number)
    )
    st.session_state.difficulty = difficulty
elif st.session_state.difficulty != difficulty:
    st.session_state.update(
        new_game_state(difficulty, previous_game_number=st.session_state.game_number)
    )
    st.session_state.difficulty = difficulty

st.subheader("Make a guess")

st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=get_guess_input_key(difficulty, st.session_state.game_number)
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    st.session_state.update(
        new_game_state(difficulty, previous_game_number=st.session_state.game_number)
    )
    st.session_state.difficulty = difficulty
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    result = apply_guess(raw_guess, st.session_state, attempt_limit)

    if result["kind"] == "error":
        st.error(result["message"])
    elif result["kind"] == "duplicate":
        st.warning(result["message"])
    else:
        if show_hint and result["hint_message"]:
            st.warning(result["hint_message"])

        if result["kind"] == "won":
            st.balloons()
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        elif result["kind"] == "lost":
            st.error(
                f"Out of attempts! "
                f"The secret was {st.session_state.secret}. "
                f"Score: {st.session_state.score}"
            )

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
