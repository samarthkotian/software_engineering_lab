import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

os.environ.update(SDL_VIDEODRIVER='dummy', SDL_AUDIODRIVER='dummy',
                  PYGAME_HIDE_SUPPORT_PROMPT='1')
import pygame

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'game.py'
spec = importlib.util.spec_from_file_location('dino', SOURCE)
game = importlib.util.module_from_spec(spec)
spec.loader.exec_module(game)


class FinalGameTests(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.temp = tempfile.TemporaryDirectory()
        self.score_path = Path(self.temp.name) / 'dino_highscore.txt'
        self.score_patch = patch.object(game, 'HIGH_SCORE_FILE', self.score_path)
        self.score_patch.start()
        self.g = game.Game()

    def tearDown(self):
        self.score_patch.stop()
        self.temp.cleanup()
        pygame.quit()

    def obstacle(self, right, speed=0):
        obs = game.Obstacle(0, game.GROUND_Y, speed)
        obs.rect.right = right
        return obs

    def collide(self, score):
        self.g = game.Game()
        self.g.state = 'play'
        self.g.score = score * 10
        obs = self.obstacle(self.g.dino.rect.right)
        obs.rect = self.g.dino.rect.copy()
        self.g.obstacles = [obs]
        self.g.update()
        self.assertEqual(self.g.state, 'lose')

    def test_initial_ground_and_first_jump(self):
        d = self.g.dino
        self.assertEqual(d.rect.bottom, game.GROUND_Y)
        self.assertTrue(d.on_ground)
        self.assertEqual((d.jump_count, d.vel_y), (0, 0))
        self.g.start_or_jump()
        self.g.update()
        self.assertEqual(self.g.state, 'play')
        self.assertLess(d.rect.bottom, game.GROUND_Y)
        self.assertFalse(d.on_ground)
        self.assertEqual(d.jump_count, 1)

    def test_double_jump_third_blocked_and_landing_rearms(self):
        d = self.g.dino
        self.assertEqual(game.max_jumps(), 2)
        for cycle in range(2):
            d.jump()
            for _ in range(5):
                d.update(game.GROUND_Y)
            self.assertEqual(d.jump_count, 1)
            d.jump()
            self.assertEqual((d.jump_count, d.vel_y), (2, game.JUMP_FORCE))
            d.update(game.GROUND_Y)
            before = (d.jump_count, d.vel_y, d.rect.y)
            d.jump()
            self.assertEqual((d.jump_count, d.vel_y, d.rect.y), before)
            for _ in range(150):
                d.update(game.GROUND_Y)
            self.assertEqual((d.rect.bottom, d.jump_count, d.vel_y),
                             (game.GROUND_Y, 0, 0))
            self.assertTrue(d.on_ground)

    def test_rendered_ground_air_and_landing_colors(self):
        screen = pygame.Surface((game.WIDTH, game.HEIGHT))
        d = self.g.dino
        for expected in ((83, 141, 78), (50, 120, 220), (83, 141, 78)):
            d.draw(screen)
            self.assertEqual(screen.get_at(d.rect.center)[:3], expected)
            if d.on_ground:
                d.jump()
                d.update(game.GROUND_Y)
            else:
                for _ in range(150):
                    d.update(game.GROUND_Y)

    def test_pass_counts_once_and_not_on_spawn(self):
        self.g.state = 'play'
        self.g.spawn_interval = 100000
        obs = self.obstacle(self.g.dino.rect.right + 100, 0)
        self.g.obstacles = [obs]
        with patch.object(game, 'on_obstacle_passed', wraps=game.on_obstacle_passed) as hook:
            self.g.update()
            self.assertEqual(self.g.combo, 0)
            obs.rect.right = self.g.dino.rect.left + 1
            obs.speed = 2
            self.g.update()
            self.assertTrue(obs.passed)
            for _ in range(100):
                self.g.update()
            self.assertEqual(hook.call_count, 1)
            self.assertEqual(self.g.combo, 1)
            self.assertNotIn(obs, self.g.obstacles)
        other = self.obstacle(self.g.dino.rect.left - 1)
        self.g.obstacles = [other]
        self.g.update()
        self.assertEqual(self.g.combo, 2)

    def test_notifications_expire_independently_during_game_over(self):
        self.g.state = 'play'
        for now in (100, 200):
            self.g.obstacles = [self.obstacle(self.g.dino.rect.left - 1)]
            with patch.object(pygame.time, 'get_ticks', return_value=now):
                self.g.update()
        self.assertEqual(len(self.g.notifications), 2)
        self.assertIn('CLEAR!', self.g.notifications[0][0])
        self.assertIn('Combo x2', self.g.notifications[1][0])
        self.g.state = 'lose'
        for now, remaining in ((1299, 2), (1300, 1), (1400, 0)):
            with patch.object(pygame.time, 'get_ticks', return_value=now):
                self.g.update()
            self.assertEqual(len(self.g.notifications), remaining)

    def test_restart_resets_run_state_and_keeps_best(self):
        self.g.high_score = 99
        self.g.combo = 7
        self.g.notifications = [('CLEAR!', 999999)]
        self.g.score = 1000
        self.g.speed = 10
        self.g.spawn_timer = 45
        self.g.obstacles = [self.obstacle(500)]
        self.g.dino.jump()
        self.g.dino.jump()
        self.g.state = 'lose'
        self.g.start_or_jump()
        self.assertEqual(self.g.state, 'wait')
        self.assertEqual((self.g.combo, self.g.score, self.g.spawn_timer), (0, 0, 0))
        self.assertEqual(self.g.speed, 6)
        self.assertEqual(self.g.spawn_interval, 90)
        self.assertEqual((self.g.notifications, self.g.obstacles), ([], []))
        self.assertEqual(self.g.high_score, 99)
        self.assertEqual(self.g.dino.rect.bottom, game.GROUND_Y)
        self.assertEqual((self.g.dino.jump_count, self.g.dino.vel_y), (0, 0))
        self.assertTrue(self.g.dino.on_ground)
        self.g.start_or_jump()
        self.g.update()
        self.assertEqual(self.g.dino.jump_count, 1)
        self.assertLess(self.g.dino.rect.bottom, game.GROUND_Y)

    def test_high_score_higher_equal_lower_and_no_collision_clear(self):
        self.score_path.write_text('55')
        for score, expected_saves in ((80, 1), (80, 0), (40, 0)):
            before = self.score_path.stat().st_mtime_ns
            with patch.object(game, 'save_high_score', wraps=game.save_high_score) as save:
                self.collide(score)
                self.assertEqual(save.call_count, expected_saves)
            if not expected_saves:
                self.assertEqual(self.score_path.stat().st_mtime_ns, before)
            self.assertEqual(self.score_path.read_text(), '80')
            self.assertEqual(game.Game().high_score, 80)
            self.assertEqual(self.g.combo, 0)
            self.assertEqual(self.g.notifications, [])

    def test_missing_invalid_score_and_unwritable_save(self):
        self.assertEqual(game.load_high_score(), 0)
        for text in ('', 'invalid'):
            self.score_path.write_text(text)
            self.assertEqual(game.load_high_score(), 0)
        with patch('builtins.open', side_effect=PermissionError('test')):
            game.save_high_score(80)  # Existing behavior: no game crash.

    def test_new_process_saves_and_reloads_from_other_folder(self):
        script = Path(self.temp.name) / 'game.py'
        script.write_bytes(SOURCE.read_bytes())
        self.score_path.write_text('55')
        other = Path(self.temp.name) / 'elsewhere'
        other.mkdir()
        base = (
            'import importlib.util, pygame; '
            f's=importlib.util.spec_from_file_location("dino", {str(script)!r}); '
            'm=importlib.util.module_from_spec(s); s.loader.exec_module(m); '
            'pygame.init(); g=m.Game(); '
        )
        save = base + (
            'assert g.high_score == 55; g.state="play"; g.score=800; '
            'o=m.Obstacle(80,m.GROUND_Y,0); o.rect=g.dino.rect.copy(); '
            'g.obstacles=[o]; g.update(); assert g.high_score == 80; pygame.quit()'
        )
        reload = base + 'assert g.high_score == 80; pygame.quit()'
        for code in (save, reload):
            subprocess.run([sys.executable, '-c', code], cwd=other, check=True)
        self.assertFalse((other / 'dino_highscore.txt').exists())

    def test_spawn_score_speed_ramp_and_idle(self):
        self.g.update()
        self.assertEqual(self.g.score, 0)
        self.g.state = 'play'
        self.g.spawn_timer = self.g.spawn_interval - 1
        with patch.object(game.random, 'randint', return_value=73) as rng:
            self.g.update()
            rng.assert_called_once_with(55, 110)
        self.assertEqual(len(self.g.obstacles), 1)
        self.assertEqual(self.g.spawn_interval, 73)
        self.g.obstacles = []
        self.g.spawn_interval = 100000
        self.g.score = 299
        self.g.update()
        self.assertEqual((self.g.score, self.g.speed), (300, 6.5))
        self.g.state = 'lose'
        self.g.update()
        self.assertEqual(self.g.score, 300)

    def test_all_screens_render_and_notifications_are_visible(self):
        screen = pygame.display.set_mode((game.WIDTH, game.HEIGHT))
        for state in ('wait', 'play', 'lose'):
            self.g.state = state
            self.g.draw(screen)
        self.g.state = 'play'
        self.g.combo = 2
        self.g.notifications = [('CLEAR! Score: 3  Combo x2', 999999)]
        self.g.dino.jump()
        self.g.dino.update(game.GROUND_Y)
        self.g.draw(screen)
        background = screen.map_rgb(game.BG_COLOR)
        self.assertTrue(any(screen.get_at_mapped((x, y)) != background
                            for x in range(20, 300) for y in range(55, 80)))
        pygame.image.save(screen, ROOT / 'evidence/after_test_preview.png')

    def test_main_loop_handles_each_control_and_quit(self):
        for key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
            frames = [[pygame.event.Event(pygame.KEYDOWN, key=key)],
                      [pygame.event.Event(pygame.KEYDOWN, key=key)],
                      [pygame.event.Event(pygame.KEYDOWN, key=key)],
                      [pygame.event.Event(pygame.QUIT)]]
            with patch.object(pygame.event, 'get', side_effect=frames):
                game.main()


if __name__ == '__main__':
    print(f'Python {sys.version.split()[0]}; Pygame {pygame.version.ver}; SDL dummy display/audio', flush=True)
    unittest.main(verbosity=2)
