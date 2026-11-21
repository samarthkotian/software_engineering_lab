# Lab 4 - Vibe Coding: Dino Run

This folder contains the completed Pygame Dino Run lab, its before/after gameplay
recordings, an exported chat PDF, regression checks, and the original supplied code.

## Chat history

[Complete chat history](https://chatgpt.com/s/cx_6b01e93fce00819188c6779c1bed1f5b)
is the canonical conversation for this submission. The same URL is saved in
[chat_link.txt](chat_link.txt) and included in the [PDF export](chat_history.pdf).
The final `game.py` and `requirements.txt` match the files produced in that chat.

## Run

Use Python 3.10 or newer:

```powershell
python -m pip install -r requirements.txt
python game.py
```

Space, Up, or W starts the game and jumps. Press again in midair for a double
jump. A third jump is blocked until landing. After a collision, press a jump key
to return to the start screen, then press it again to begin a new run.

## Tasks

| Task | Implementation |
| --- | --- |
| 1. Persistent high score | Preserve the correct `self.high_score < current` comparison; save beside `game.py`, independent of the launch directory. Missing or noninteger saves start at zero. |
| 2. `dino_tint(on_ground)` | Keep the original green on the ground; use blue while airborne. |
| 3. `on_obstacle_passed(obstacle, score)` | Return clear-message text for `Game` to display with the combo. Each message expires after 1,200 ms, including during Game Over. Count each obstacle once; reset messages and combo on restart. |
| 4. `max_jumps()` | Allow two jumps, reject the third, and replenish jumps on landing. Position the dino's feet at the constructor's ground-height argument. |

The supplied README describes a reversed high-score comparison, but the actual
supplied `game.py` already contains the correct `if self.high_score < current:`
condition. The baseline was preserved exactly in `evidence/original_game.py`.
The first task therefore verifies and preserves the existing comparison, and
anchors the save path to the script directory.
The before video honestly shows the supplied code; the described reversed
comparison was not introduced to manufacture a bug demonstration.

## Deliverables

- `game.py`: completed single-file game.
- [Before gameplay](videos/before.mp4): 10 seconds of the exact supplied game.
- [After gameplay](videos/after.mp4): 10 seconds of the completed game.
- [Complete chat history](https://chatgpt.com/s/cx_6b01e93fce00819188c6779c1bed1f5b): the supplied shared conversation.
- [Chat history PDF](chat_history.pdf): export of the same conversation, with the shared URL on its first page.
- `evidence/`: untouched baseline, recording metadata and representative frames.
- `tests/test_game.py`: checks for persistence, jumps, landing, clear events and restart behavior.

Both videos contain 600 real Pygame-rendered frames at 60 fps (900 x 480).
The bottom caption identifies the version and the automated input method.
Recordings use normal `Game.start_or_jump()` inputs, a fixed random seed, and a
temporary high-score file initially containing zero. Scores, obstacles,
collisions, physics, and game states are not injected. A deliberate missed jump
shows an actual collision and record saving. Metadata records the source hash,
input events, final score, saved best, and best loaded by a fresh `Game`.
There is no audio because this game has no sound effects.

The `CLEAR! Score: ... Combo x...` notification reports the score at the moment
an obstacle is cleared; it does not add points to the time-based score. Combo
means consecutive obstacles cleared in the current run. The README's original
stub ignored the callback's return; the final integration consumes it as the
notification text, as shown in the shared conversation.

## Verify and reproduce videos

```powershell
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python record_gameplay.py before
python record_gameplay.py after
```

The tests and recordings isolate their score files and do not overwrite a
player's saved record. `dino_highscore.txt` is created by gameplay and is ignored
by Git.

Validation on 22 November 2026: all 12 regression tests passed. Both MP4 files
were decoded and verified to contain 600 frames at 60 fps with a duration of
10.0 seconds. Both recordings reached score 51, saved best 51, and loaded best
51 in a fresh `Game`. The completed game cleared four obstacles. The input at
frame 14 reached jump count 2 in the completed game. See the JSON files in
`evidence/` for the detailed events and video properties.

The original before-video is preserved. The after-video was regenerated from
the shared conversation's final code, paced in real time so the 1,200 ms
notification lifetime is represented correctly. The tests include a fresh
process reloading the saved record; the video metadata additionally verifies
that a new `Game` loads the same best. The video is an automated gameplay
capture, not a manual keyboard recording or a close-and-relaunch recording.

Separate commits preserve the baseline and each of the four tasks. This lab
belongs in the personal lab repository under `lab4/`; no pull request to the
instructor's repository is needed.
