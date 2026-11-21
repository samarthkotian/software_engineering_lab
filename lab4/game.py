import random
from pathlib import Path

import pygame

WIDTH, HEIGHT = 900, 400
GROUND_Y = 340
FPS = 60
BG_COLOR = (245, 245, 245)
GROUND_COLOR = (80, 80, 80)
GRAVITY, JUMP_FORCE = 0.6, -14
# Keep the same saved best regardless of the folder used to launch the game.
HIGH_SCORE_FILE = Path(__file__).resolve().with_name("dino_highscore.txt")
CLEAR_NOTIFICATION_MS = 1200


def dino_tint(on_ground):
    """Keep the default green on the ground; use blue in the air."""
    return None if on_ground else (50, 120, 220)


def on_obstacle_passed(obstacle, score):
    """Build the clear message; Game owns the per-run combo and its display."""
    return f"CLEAR! Score: {score}"


def max_jumps():
    """Allow two jumps before the dino must land again."""
    return 2


def load_high_score():
    try:
        with open(HIGH_SCORE_FILE) as f:
            return int(f.read().strip())
    except (OSError, ValueError):
        return 0


def save_high_score(value):
    try:
        with open(HIGH_SCORE_FILE, "w") as f:
            f.write(str(value))
    except OSError:
        pass


class Dino:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 60)
        # y is the ground height, so start with the feet on the ground.
        self.rect.bottom = y
        self.vel_y = 0.0
        self.on_ground = True
        self.jump_count = 0
        self.color = (83, 141, 78)

    def jump(self):
        if self.jump_count < (max_jumps() or 1):
            self.vel_y = JUMP_FORCE
            self.on_ground = False
            self.jump_count += 1

    def update(self, ground_y):
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        if self.rect.bottom >= ground_y:
            self.rect.bottom = ground_y
            self.vel_y = 0
            self.on_ground = True
            self.jump_count = 0

    def draw(self, screen):
        color = dino_tint(self.on_ground) or self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=6)
        eye = pygame.Rect(self.rect.right - 12, self.rect.top + 10, 8, 8)
        pygame.draw.rect(screen, (255, 255, 255), eye, border_radius=4)
        pygame.draw.rect(screen, (0, 0, 0), (eye.x + 2, eye.y + 2, 4, 4))


class Obstacle:
    WIDTHS = [20, 30, 25]
    HEIGHTS = [40, 60, 50]

    def __init__(self, x, ground_y, speed):
        w = random.choice(self.WIDTHS)
        h = random.choice(self.HEIGHTS)
        self.rect = pygame.Rect(x, ground_y - h, w, h)
        self.speed = speed
        self.color = (180, 60, 40)
        self.passed = False

    def update(self):
        self.rect.x -= self.speed

    def is_off_screen(self):
        return self.rect.right < 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=4)


class Game:
    def __init__(self):
        self.font = pygame.font.Font(None, 28)
        self.big_font = pygame.font.Font(None, 48)
        self.high_score = load_high_score()
        self.reset()

    def reset(self):
        self.dino = Dino(80, GROUND_Y)
        self.obstacles = []
        self.score = 0
        self.combo = 0
        self.notifications = []
        self.speed = 6
        self.spawn_timer = 0
        self.spawn_interval = 90
        self.state = "wait"

    def start_or_jump(self):
        if self.state == "lose":
            self.reset()
            return
        if self.state == "wait":
            self.state = "play"
        self.dino.jump()

    def update(self):
        now = pygame.time.get_ticks()
        # Expire messages even while the game-over screen is showing.
        self.notifications = [
            (text, expires_at) for text, expires_at in self.notifications
            if now < expires_at
        ]
        if self.state != "play":
            return
        self.dino.update(GROUND_Y)
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            self.obstacles.append(Obstacle(WIDTH + 10, GROUND_Y, self.speed))
            self.spawn_timer = 0
            self.spawn_interval = random.randint(55, 110)

        hit = False
        for obs in self.obstacles:
            obs.update()
            if not obs.passed and obs.rect.right < self.dino.rect.left:
                obs.passed = True
                message = on_obstacle_passed(obs, self.score // 10)
                self.combo += 1
                self.notifications.append(
                    (f"{message}  Combo x{self.combo}", now + CLEAR_NOTIFICATION_MS)
                )
            if obs.rect.colliderect(self.dino.rect):
                hit = True
        self.obstacles = [o for o in self.obstacles if not o.is_off_screen()]

        if hit:
            self.state = "lose"
            current = self.score // 10
            if self.high_score < current:
                self.high_score = current
                save_high_score(self.high_score)
            return

        self.score += 1
        if self.score % 300 == 0:
            self.speed += 0.5

    def draw(self, screen):
        screen.fill(BG_COLOR)
        pygame.draw.line(screen, GROUND_COLOR, (0, GROUND_Y), (WIDTH, GROUND_Y), 3)
        self.dino.draw(screen)
        for obs in self.obstacles:
            obs.draw(screen)

        score_surf = self.font.render(f"Score: {self.score // 10}   Best: {self.high_score}", True, (50, 50, 50))
        screen.blit(score_surf, (WIDTH - 260, 20))

        combo_surf = self.font.render(f"Combo: {self.combo}", True, (50, 50, 50))
        screen.blit(combo_surf, (20, 20))
        for index, (text, _) in enumerate(self.notifications):
            notification_surf = self.font.render(text, True, (30, 100, 180))
            screen.blit(notification_surf, (20, 55 + index * 28))

        if self.state == "wait":
            msg = self.big_font.render("Press SPACE to Start", True, (80, 80, 80))
            screen.blit(msg, msg.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 10)))
        elif self.state == "lose":
            msg = self.big_font.render("GAME OVER", True, (200, 40, 40))
            sub = self.font.render("Press SPACE to Restart", True, (80, 80, 80))
            screen.blit(msg, msg.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20)))
            screen.blit(sub, sub.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30)))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Dino Run")
    clock = pygame.time.Clock()
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                game.start_or_jump()
        game.update()
        game.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == "__main__":
    main()
