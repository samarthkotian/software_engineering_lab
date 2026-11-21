# Lab 4 - Vibe Coding: Dino Run

This folder contains the completed Pygame Dino Run lab, its before/after gameplay
recordings, an exported chat PDF, regression checks, and the original supplied code.

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
| 1. Persistent high score | Save only when `current > self.high_score`; load the best from a file beside `game.py`, independent of the launch directory. Missing, invalid or negative saves start at zero. |
| 2. `dino_tint(on_ground)` | Keep the original green on the ground; use blue while airborne. |
| 3. `on_obstacle_passed(obstacle, score)` | Create a floating clear notification. Count each cleared obstacle once in a per-run combo counter, which resets on restart. |
| 4. `max_jumps()` | Allow two jumps, reject the third, and replenish jumps on landing. Start the dino on the ground. |

The supplied README describes a reversed high-score comparison, but the actual
supplied `game.py` already contains the correct `if self.high_score < current:`
condition. The baseline was preserved exactly in `evidence/original_game.py`.
The first task therefore verifies the existing comparison, rewrites it in the
more direct `current > self.high_score` form, and strengthens file handling.
The before video honestly shows the supplied code; the described reversed
comparison was not introduced to manufacture a bug demonstration.

## Deliverables

- `game.py`: completed single-file game.
- [Before gameplay](videos/before.mp4): 10 seconds of the exact supplied game.
- [After gameplay](videos/after.mp4): 10 seconds of the completed game.
- [Chat history PDF](chat_history.pdf): exported user/assistant conversation through the stated cutoff.
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

The `+1 CLEAR` popup counts obstacles cleared; it does not add points to the
time-based score. Combo means consecutive obstacles cleared in the current run.

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

Validation on 21 November 2026: all 13 regression tests passed. Both MP4 files
were decoded and verified to contain 600 frames at 60 fps with a duration of
10.0 seconds. Both recordings reached score 51, saved best 51, and loaded best
51 in a fresh `Game`. The completed game cleared four obstacles. The input at
frame 14 reached jump count 2 in the completed game. See the JSON files in
`evidence/` for the detailed events and video properties.

Separate commits preserve the baseline and each of the four tasks. This lab
belongs in the personal lab repository under `lab4/`; no pull request to the
instructor's repository is needed.
