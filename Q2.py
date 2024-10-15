import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FPS = 30  # Game speed
GRAVITY = 1
PLAYER_SPEED = 5

# Game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Animal Hero Side-Scroller")

# Fonts
font = pygame.font.SysFont(None, 30)

# Clock
clock = pygame.time.Clock()

# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 60))  # Placeholder for hero sprite
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = HEIGHT - 100
        self.speed_x = 0
        self.speed_y = 0
        self.health = 100
        self.lives = 3
        self.is_jumping = False

    def update(self):
        self.speed_y += GRAVITY
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Prevent falling off screen
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.is_jumping = False

        # Prevent player from going off the left or right edge
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def jump(self):
        if not self.is_jumping:
            self.speed_y = -15  # Jump strength
            self.is_jumping = True

    def shoot(self):
        return Projectile(self.rect.right, self.rect.centery - 10)
# Projectile Class
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed_x = 7  # Projectile speed

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.left > WIDTH:
            self.kill()

# Enemy Class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, health=50, speed=2):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = speed  # Dynamic speed based on level
        self.health = health

    def update(self):
        self.rect.x -= self.speed_x
        if self.rect.right < 0:
            self.kill()

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()

# Boss Class (inherits from Enemy)
class Boss(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, health=300, speed=1)
        self.image = pygame.Surface((100, 100))  # Larger size for the boss
        self.image.fill((150, 0, 0))  # Different color for the boss
        self.fire_rate = 30  # Boss can shoot back at player

    def shoot(self):
        # Boss shoots back at the player
        return Projectile(self.rect.left, self.rect.centery)

# Collectible Class
class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, collectible_type):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(GREEN)  # Can change color based on type
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = collectible_type  # 'health' or 'life'

    def apply_effect(self, player):
        if self.type == 'health':
            player.health += 20
            if player.health > 100:
                player.health = 100
        elif self.type == 'life':
            player.lives += 1

# Enemy Spawner
def spawn_enemy(level):
    speed = 2 + level  # Increase enemy speed with each level
    health = 50 + (level * 20)  # Increase enemy health with each level
    return Enemy(WIDTH + random.randint(0, 300), HEIGHT - 100, health, speed)

# Draw text on screen
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    surface.blit(text_obj, (x, y))
# Draw Health Bar
def draw_health_bar(surface, x, y, health):
    bar_length = 100
    bar_height = 10
    fill = (health / 100) * bar_length
    outline_rect = pygame.Rect(x, y, bar_length, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surface, GREEN, fill_rect)
    pygame.draw.rect(surface, WHITE, outline_rect)

# Game Over Screen
def game_over_screen():
    screen.fill(BLACK)
    draw_text("GAME OVER", font, WHITE, screen, WIDTH // 2 - 100, HEIGHT // 2)
    draw_text("Press R to Restart", font, WHITE, screen, WIDTH // 2 - 120, HEIGHT // 2 + 50)
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False

# Main Game Loop
def main_game():
    player = Player()
    projectiles = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    collectibles = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group(player)

    score = 0
    level = 1
    enemies_killed = 0
    level_goal = 10  # Enemies needed to complete a level
    boss_spawned = False

    running = True

    while running:
        clock.tick(FPS)

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    projectile = player.shoot()
                    projectiles.add(projectile)
                    all_sprites.add(projectile)
                if event.key == pygame.K_UP:
                    player.jump()
                if event.key == pygame.K_LEFT:
                    player.speed_x = -PLAYER_SPEED
                if event.key == pygame.K_RIGHT:
                    player.speed_x = PLAYER_SPEED
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.speed_x = 0

        # Spawning Enemies
        if not boss_spawned and random.randint(1, 100) < 7:
            enemy = spawn_enemy(level)
            enemies.add(enemy)
            all_sprites.add(enemy)

        # Spawn Boss at Level 3
        if level == 3 and enemies_killed >= level_goal and not boss_spawned:
            boss = Boss(WIDTH, HEIGHT - 150)
            enemies.add(boss)
            all_sprites.add(boss)
            boss_spawned = True

        # Update
        all_sprites.update()

        # Collisions - Player projectiles with enemies
        for projectile in projectiles:
            enemy_hit = pygame.sprite.spritecollide(projectile, enemies, False)
            if enemy_hit:
                for enemy in enemy_hit:
                    enemy.take_damage(25)
                    if enemy.health <= 0:
                        score += 10
                        enemies_killed += 1
                        if enemies_killed >= level_goal and level < 3:
                            level += 1  # Progress to next level
                            enemies_killed = 0  # Reset for the new level
                projectile.kill()

        # Player collision with enemies
        player_hit = pygame.sprite.spritecollide(player, enemies, False)
        if player_hit:
            player.health -= 10
            if player.health <= 0:
                player.lives -= 1
                player.health = 100
                if player.lives <= 0:
                    game_over_screen()
                    running = False

        # Drawing
        screen.fill(BLACK)
        all_sprites.draw(screen)
        draw_text(f"Score: {score}", font, WHITE, screen, 10, 10)
        draw_text(f"Level: {level}", font, WHITE, screen, 10, 40)
        draw_health_bar(screen, 10, 70, player.health)
        pygame.display.flip()

    pygame.quit()

# Start the game
main_game()

