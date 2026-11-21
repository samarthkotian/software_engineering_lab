"""Record actual Pygame frames with reproducible, automated jump inputs.

No scores, collisions, physics, obstacles or game states are injected. The
temporary score file starts at zero, so recording never changes a player's best.
Run before recording against evidence/original_game.py, then after against game.py.
"""

import argparse
from contextlib import contextmanager
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import random
import tempfile

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import imageio.v2 as imageio
import pygame

ROOT = Path(__file__).resolve().parent


@contextmanager
def frame_writer(version, output, frames_only):
    if frames_only:
        directory = ROOT / "_frames" / version
        directory.mkdir(parents=True, exist_ok=True)

        class PNGWriter:
            count = 0

            def append_data(self, frame):
                imageio.imwrite(directory / f"{self.count:04d}.png", frame)
                self.count += 1

        yield PNGWriter()
    else:
        with imageio.get_writer(output, fps=60, codec="libx264", quality=8,
                                macro_block_size=2, pixelformat="yuv420p") as writer:
            yield writer


def encode_saved_frames(version):
    output = ROOT / "videos" / f"{version}.mp4"
    frames = sorted((ROOT / "_frames" / version).glob("*.png"))
    if len(frames) != 600:
        raise ValueError(f"Expected 600 captured frames; found {len(frames)}")
    with frame_writer(version, output, False) as writer:
        for path in frames:
            writer.append_data(imageio.imread(path))
    print(f"Encoded {len(frames)} captured frames: {output}")


def record(version, frames_only=False):
    source = ROOT / ("evidence/original_game.py" if version == "before" else "game.py")
    spec = importlib.util.spec_from_file_location("recorded_game", source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    random.seed(4)
    pygame.init()
    surface = pygame.display.set_mode((module.WIDTH, module.HEIGHT + 80))
    game_surface = pygame.Surface((module.WIDTH, module.HEIGHT))
    label_font = pygame.font.Font(None, 24)
    clock = pygame.time.Clock()
    (ROOT / "videos").mkdir(exist_ok=True)
    events = []
    snapshots = []
    with tempfile.TemporaryDirectory() as temp:
        module.HIGH_SCORE_FILE = Path(temp) / "dino_highscore.txt"
        module.HIGH_SCORE_FILE.write_text("0", encoding="utf-8")
        game = module.Game()
        output = ROOT / "videos" / f"{version}.mp4"
        with frame_writer(version, output, frames_only) as writer:
            for frame in range(600):
                pygame.event.pump()
                # Start normally. Demonstrate an extra midair key press.
                if frame in (0, 14):
                    game.start_or_jump()
                    events.append({"frame": frame, "event": "jump key", "jumps": game.dino.jump_count})
                # Clear early obstacles, then deliberately stop jumping to
                # demonstrate a real collision and persisted record in 10 sec.
                if game.state == "play" and frame < 420 and game.dino.on_ground:
                    approaching = [o for o in game.obstacles if not o.passed
                                   and o.rect.right >= game.dino.rect.left]
                    if approaching and min(o.rect.left for o in approaching) - game.dino.rect.right < 110:
                        game.start_or_jump()
                        events.append({"frame": frame, "event": "jump key", "jumps": game.dino.jump_count})
                old_state = game.state
                old_passed = sum(o.passed for o in game.obstacles)
                game.update()
                new_passed = sum(o.passed for o in game.obstacles)
                if new_passed > old_passed:
                    events.append({"frame": frame, "event": "obstacle cleared", "score": game.score // 10})
                    snapshots.append((frame + 5, "clear"))
                if game.state != old_state:
                    events.append({"frame": frame, "event": game.state, "score": game.score // 10,
                                   "best": game.high_score})
                game.draw(game_surface)
                surface.fill((23, 33, 49))
                surface.blit(game_surface, (0, 0))
                title = f"{version.upper()} | Actual Pygame frames | Automated jump inputs | {frame / 60:04.1f}s / 10.0s"
                note = ("Supplied code: single jump, no tint or clear feedback; best-score comparison already correct."
                        if version == "before" else
                        "Completed: blue airborne tint, double jump, timed clear messages + combo, persistent best.")
                surface.blit(label_font.render(title, True, (255, 255, 255)), (18, module.HEIGHT + 13))
                surface.blit(label_font.render(note, True, (210, 224, 240)), (18, module.HEIGHT + 44))
                writer.append_data(pygame.surfarray.array3d(surface).transpose(1, 0, 2))
                if frame in (20, 599) or any(frame == n for n, _ in snapshots):
                    pygame.image.save(surface, ROOT / "evidence" / f"{version}_{frame:03d}.png")
                # Use real time for the game's 1,200 ms notification expiry.
                clock.tick(module.FPS)
        persisted = module.load_high_score()
        reloaded = module.Game().high_score
        metadata = {"version": version, "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                    "frames": 600, "fps": 60, "seconds": 10, "size": [900, 480],
                    "input_method": "automated calls to Game.start_or_jump; no gameplay state injection",
                    "timing": "real-time pygame clock capped at 60 fps",
                    "initial_best": 0, "final_score": game.score // 10, "final_best": game.high_score,
                    "saved_best": persisted, "reloaded_best": reloaded, "events": events}
        (ROOT / "evidence" / f"{version}_recording.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
        print(json.dumps(metadata, indent=2))
    pygame.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("version", choices=("before", "after"))
    parser.add_argument("--frames-only", action="store_true", help="Capture PNGs before encoding")
    parser.add_argument("--encode-saved", action="store_true", help="Encode previously captured PNGs")
    args = parser.parse_args()
    if args.encode_saved:
        encode_saved_frames(args.version)
    else:
        record(args.version, args.frames_only)
