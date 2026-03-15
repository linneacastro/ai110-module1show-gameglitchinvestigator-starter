# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
When I first ran the game, there were several noticeable bugs, but the game seemed to be in a pretty good place in terms of the user interface and basic design. I appreciated that the game had a "Developer Debug Info" Panel which gave me a glimpse of what the game was taking into account behind the scenes, before even looking at the code. One of the first things I noticed was that there were limited ways to customize the game - the main method being through choosing the Difficulty level of Easy, Normal, or Hard. This game reminded me of a small program I had written when I was just getting started - a "High/Low" game where you could set a range, and then have the computer guess the number you were thinking of using the binary search algorithm.

- List at least two concrete bugs you noticed at the start  
✅ 1. When I guessed 1, the game told me to "Go LOWER!" and when I guessed 100, the game told me "Go HIGHER!". This is when I was playing on Normal mode. 
✅ 2. It let me guess the number 99 several times, ie. it kept counting that number as one of my guesses instead of telling me that I had already guessed that number before.
  (for example: "the secret number kept changing" or "the hints were backwards").
✅ 3. When I click "New Game" after exhausting my turns in the first game, it doesn't reset anything unless I refresh the browser window.
✅ 4. The difficulty levels don't seem to match. Easy is 1-20 range with 6 attempts. Normal is 1-100 range with 8 attempts. Hard is 1-50 with 5 attempts. 
5. In Normal mode, it says I have 8 attempts, but at 7, it says Game over. Array only contains guesses 0-6 (7 total, not 8). It doesn't look like the first guess is being stored in the history array.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
I used Github Copilot. This was my first time using it. I used it first in Plan mode, and then in Agent mode. I also used Claude.ai (just the browser chatbot) when I ran into issues installing dependencies like pytest.
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
One example where the AI suggestion was correct was in the first bug I tackled - correcting the direction of a too high or too low guess. The logic here was reversed initially, so the fix was quite simple. The AI also correctly refactored the function to check the guess into the logic_utils.py file and then imported it where needed. The AI also was correct in creating a test case to verify these changes. The great thing was that not only could I verify with pytest, but I also ran the program and could see first hand how the behavior changed. 
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
I haven't yet encountered a suggestion yet where the AI was off base... but this just tells me that I haven't used it enough! 

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
Two things: I created a test for it, and made sure I understood the logic behind the test (so the AI couldn't just create a test that it passed in every case), and I also verified the behavior within the game.
- Describe at least one test you ran (manual or using pytest) and what it showed you about your code.
Using pytest, there were two situations that I tested. The first was whether a guess that was higher than the secret number would give the correct message. The test captured the output and checked that it was equal to the "Go LOWER!" message you would expect. The reverse situation was also tested. Another way I tested was to launch the new version of the game and give it a play. This helped me verify that the behavior matched the changes made in the code. 
- Did AI help you design or understand any tests? How?
Yes! The AI helped me design the test. At first, I didn't understand what it was doing since it had been over a year since I used pytest. My main concern was making sure that the AI didn't just create a test case it would pass 100% of the time. Once the test was created, I used the inline Chat with Github Copilot to explain the logic of the test. When it gave me this, I verified the behavior of the test to make sure that it was actually passing (and it was!). 

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
