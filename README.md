# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [ ] Describe the game's purpose.
The game's purpose is to play a game with the user. The user's job isi to guess the secret number that the computer has selected. The user can select between Easy, Normal, and Hard modes, with range and number of guesses varying according to level. 
- [ ] Detail which bugs you found.
1. Hints are backwards — On Normal mode, guessing 1 shows "Go LOWER!" and guessing 100 shows "Go HIGHER!" — the hint logic is inverted.
2. Duplicate guesses are not rejected — The game allows the same number (e.g., 99) to be guessed multiple times, counting each as a separate attempt instead of warning the player they already tried that number.
3. "New Game" button doesn't reset state — After running out of turns, clicking "New Game" fails to reset the game. A full browser refresh is required for the game to restart properly.
4. Difficulty level ranges and attempts are mismatched — The levels are inconsistent with expected difficulty scaling:

Easy: 1–20 range, 6 attempts
Normal: 1–100 range, 8 attempts
Hard: 1–50 range, 5 attempts

Hard should have a wider range than Normal (not narrower), and the attempt counts don't scale meaningfully with difficulty.
- [ ] Explain what fixes you applied.
I fixed four core logic/state issues in the game. First, I corrected the comparison logic for hints so low guesses now correctly show “Go HIGHER!” and high guesses show “Go LOWER!” on Normal mode (and all modes). Second, I added a duplicate-guess check against guess history so repeated numbers are flagged as already guessed and do not consume a new attempt. Third, I updated the New Game flow to fully reset session state, including the secret number, attempts, guess history, and game-over status, so the game restarts without needing a browser refresh. Finally, I fixed the difficulty settings so each mode uses the intended range and number of attempts consistently. I verified each fix by replaying the app behavior and confirming it matched the expected rules.

## 📸 Demo

- [ ] [Insert a screenshot of your fixed, winning game here]
![my fixed game!](<Screenshot 2026-03-15 at 16.01.44.png>)

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]
