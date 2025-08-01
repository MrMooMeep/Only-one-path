import pygame
import random
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
FPS = 60

# Colors
WHITE, BLACK, GREEN, ORANGE, RED, DARK_GRAY = (255,255,255), (0,0,0), (50,200,50), (255,165,0), (220,50,50), (64,64,64)

class GameState(Enum):
    MENU = 1
    COMBAT = 2

class SinType(Enum):
    WRATH = "Wrath"
    LUST = "Lust"
    PRIDE = "Pride"

@dataclass
class Skill:
    name: str
    sin_type: SinType
    base_power: int
    coin_count: int
    description: str

@dataclass
class Identity:
    name: str
    hp: int
    max_hp: int
    speed: int
    skills: List[Skill]

class Sinner:
    def __init__(self, identity, sprite):
        self.identity = identity
        self.sprite = sprite
        self.hp = identity.hp
        self.position = (0, 0)

    def is_alive(self): return self.hp > 0

class Enemy:
    def __init__(self, name, hp, sprite):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.sprite = sprite
        self.position = (0, 0)

    def is_alive(self): return self.hp > 0

class LimbusGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Limbus Company - Sprite Edition")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 30)
        self.state = GameState.MENU

        self.sprites = {
    "Yi Sang": pygame.transform.scale(pygame.image.load("sprites/yi_sang.png"), (100, 100)),
    "Faust": pygame.transform.scale(pygame.image.load("sprites/faust.png"), (100, 100)),
    "Don Quixote": pygame.transform.scale(pygame.image.load("sprites/don_quixote.png"), (100, 100)),
    "Abnormality": pygame.transform.scale(pygame.image.load("sprites/abnormality.png"), (100, 100))
}


        self.init_characters()

    def init_characters(self):
        self.sinners = [
            Sinner(Identity("Yi Sang", 100, 100, 5, []), self.sprites["Yi Sang"]),
            Sinner(Identity("Faust", 90, 90, 7, []), self.sprites["Faust"]),
            Sinner(Identity("Don Quixote", 110, 110, 4, []), self.sprites["Don Quixote"])
        ]
        for i, s in enumerate(self.sinners):
            s.position = (200, 200 + i * 150)

        self.enemies = [
            Enemy("Abnormality", 150, self.sprites["Abnormality"])
        ]
        for i, e in enumerate(self.enemies):
            e.position = (900, 300 + i * 150)

    def draw_menu(self):
        self.screen.fill(BLACK)
        title = self.font.render("Press SPACE to start", True, WHITE)
        self.screen.blit(title, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2))

    def draw_units(self):
        for s in self.sinners:
            if s.sprite: self.screen.blit(s.sprite, s.sprite.get_rect(center=s.position))
        for e in self.enemies:
            if e.sprite: self.screen.blit(e.sprite, e.sprite.get_rect(center=e.position))

    def run(self):
        running = True
        while running:
            self.screen.fill(BLACK)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if self.state == GameState.MENU and event.key == pygame.K_SPACE:
                        self.state = GameState.COMBAT

            if self.state == GameState.MENU:
                self.draw_menu()
            elif self.state == GameState.COMBAT:
                self.draw_units()

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    game = LimbusGame()
    game.run()
