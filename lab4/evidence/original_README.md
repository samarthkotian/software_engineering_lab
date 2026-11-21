# Dino Run Repair Lab

This project is a single-file side-scrolling endless-runner clone using **Pygame**. It introduces students to obstacle spawning, jump-state tracking, and simple file-based persistence using a small, readable object-oriented codebase.

---

## What's Provided

A working Dino Run game with:

- A dino that jumps over obstacles, with gravity and ground collision
- Obstacles that spawn at random intervals and sizes and scroll past at an increasing speed
- A score that climbs over time and a game-speed ramp that kicks in every 300 points
- A high score that's meant to persist between runs, saved to a local `dino_highscore.txt` file

It has **one deliberate bug** and **three optional features** left as empty functions. You are expected to **analyze**, **interact with an AI assistant**, and **complete/fix** the game to make it fully functional and more interesting.

### **Use an LLM (e.g. ChatGPT or Claude) as your debugging and pair-programming partner for this lab.**

---

## Getting Started

### Setup

1. Make sure you have Python 3.10+ installed.
2. Install dependencies:

```bash
pip install pygame
```

3. Run the game:

```bash
python game.py
```

**Controls:** Space/Up/W to start and jump, same keys to restart after Game Over.

---

## Tasks to Complete

Each task must be completed using an iterative process involving LLM suggestions and your critical code review.

### Task 1: Fix the high-score bug

> The high score is supposed to update — and be saved to `dino_highscore.txt` — whenever the current run's score beats the previous best. In the current build, the high score never updates no matter how well you play, because the comparison that decides whether to update it is backwards. Look at the `if` condition right after a collision is detected in `Game.update`, and check which side of the comparison should be "the run that just ended" and which should be "the best score seen so far."

### Task 2: Implement `dino_tint(on_ground)`

> Called once per frame in `Dino.draw`, as `color = dino_tint(self.on_ground) or self.color`. It receives a boolean: `True` while the dino is standing on the ground, `False` while it's airborne. Return an `(r, g, b)` color, or `None` to keep the default green. Idea: give the dino a different color while it's mid-jump.

### Task 3: Implement `on_obstacle_passed(obstacle, score)`

> Called from `Game.update` exactly once per obstacle, the first frame that obstacle's right edge scrolls past the dino's left edge (i.e. it's been successfully jumped, not just spawned or removed off-screen). It receives the `Obstacle` that was passed and the score at that moment. Its return value is ignored. Idea: a small "+1" popup, or a running combo counter for consecutive obstacles cleared without a hit.

### Task 4: Implement `max_jumps()`

> Called every time the player tries to jump, as part of `if self.jump_count < (max_jumps() or 1):` in `Dino.jump`. It takes no arguments and should return an integer — the number of jumps the dino gets before it must touch the ground again — or `None` for the default of 1 (no double jump). The `jump_count` bookkeeping (incrementing on jump, resetting to 0 on landing) is already implemented; you only need to raise the limit. Idea: return `2` for a double jump.

---

## Expected Behavior

- The dino jumps only while grounded, unless `max_jumps()` allows more jumps in the air
- Obstacles spawn at randomized intervals and sizes, and the game gets gradually faster as the score climbs
- Colliding with an obstacle ends the run and shows a Game Over screen
- The high score updates and is saved to disk whenever the current run beats it, and is loaded back the next time the game starts
- Score never goes negative and the game restarts cleanly on `Space`

---

## Folder Structure

```
dino-run/
├── game.py
└── README.md
```

---

## Submission Checklist

Submission is only the following three things:

- [] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior
- [] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working
- [] The Chat/LLM used page link, with the complete chat history
