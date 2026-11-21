"""Gameplay regression checks using real Pygame rectangles and temporary saves."""

import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import pygame
import game

DEFAULT_SCORE_PATH = game.HIGH_SCORE_FILE


class HighScoreTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.score_file = Path(self.temp.name) / "best.txt"
        self.patcher = patch.object(game, "HIGH_SCORE_FILE", self.score_file)
        self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def collide(self, score, previous):
        self.score_file.write_text(str(previous), encoding="utf-8")
        run = game.Game()
        run.state = "play"
        run.score = score * 10
        run.dino.rect.bottom = game.GROUND_Y
        obstacle = game.Obstacle(run.dino.rect.x + 6, game.GROUND_Y, 6)
        run.obstacles = [obstacle]
        run.update()
        self.assertEqual(run.state, "lose")
        return run

    def test_new_record_is_saved_and_loaded_by_new_game(self):
        run = self.collide(12, 5)
        self.assertEqual(run.high_score, 12)
        self.assertEqual(self.score_file.read_text(), "12")
        self.assertEqual(game.Game().high_score, 12)

    def test_lower_or_equal_score_does_not_overwrite_record(self):
        for score in (4, 10):
            with self.subTest(score=score):
                run = self.collide(score, 10)
                self.assertEqual(run.high_score, 10)
                self.assertEqual(self.score_file.read_text(), "10")

    def test_missing_invalid_and_negative_scores_load_as_zero(self):
        self.assertEqual(game.load_high_score(), 0)
        for value in ("", "bad", "-8", "2.5"):
            with self.subTest(value=value):
                self.score_file.write_text(value, encoding="utf-8")
                self.assertEqual(game.load_high_score(), 0)

    def test_score_file_is_anchored_to_game_directory(self):
        self.assertEqual(Path(DEFAULT_SCORE_PATH), Path(game.__file__).resolve().with_name("dino_highscore.txt"))

    def test_unwritable_score_location_does_not_crash(self):
        with patch.object(game, "HIGH_SCORE_FILE", Path(self.temp.name) / "absent" / "best.txt"):
            game.save_high_score(5)
            self.assertEqual(game.load_high_score(), 0)


if __name__ == "__main__":
    unittest.main()
