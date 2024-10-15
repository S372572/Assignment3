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

