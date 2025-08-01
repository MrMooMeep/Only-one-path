
import pygame
import random
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (50, 200, 50)
ORANGE = (255, 165, 0)
RED = (220, 50, 50)
DARK_GRAY = (64, 64, 64)
YELLOW = (255, 255, 0)

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
        self.current_hp = identity.hp
        self.position = (0, 0)
        self.base_position = (0, 0)
        self.target_position = (0, 0)
        self.is_attacking = False
        self.attack_progress = 0.0
        self.return_progress = 0.0
        self.is_returning = False

    def is_alive(self):
        return self.current_hp > 0

    def start_attack(self, target_pos):
        self.base_position = self.position
        self.target_position = (target_pos[0] - 100, target_pos[1])
        self.is_attacking = True
        self.attack_progress = 0.0
        self.return_progress = 0.0
        self.is_returning = False

    def update_animation(self):
        if self.is_attacking and not self.is_returning:
            self.attack_progress += 0.1
            if self.attack_progress >= 1.0:
                self.attack_progress = 1.0
                self.is_returning = True

            t = self.attack_progress * self.attack_progress * (3 - 2 * self.attack_progress)
            self.position = (
                int(self.base_position[0] + (self.target_position[0] - self.base_position[0]) * t),
                int(self.base_position[1] + (self.target_position[1] - self.base_position[1]) * t)
            )

        elif self.is_returning:
            self.return_progress += 0.08
            if self.return_progress >= 1.0:
                self.return_progress = 1.0
                self.is_attacking = False
                self.is_returning = False
                self.position = self.base_position

            t = 1.0 - self.return_progress
            t = t * t * (3 - 2 * t)
            self.position = (
                int(self.base_position[0] + (self.target_position[0] - self.base_position[0]) * t),
                int(self.base_position[1] + (self.target_position[1] - self.base_position[1]) * t)
            )

    def take_damage(self, dmg):
        self.current_hp = max(0, self.current_hp - dmg)

class Enemy:
    def __init__(self, name, hp, sprite):
        self.name = name
        self.max_hp = hp
        self.current_hp = hp
        self.sprite = sprite
        self.position = (0, 0)

    def is_alive(self):
        return self.current_hp > 0

    def take_damage(self, dmg):
        self.current_hp = max(0, self.current_hp - dmg)

class LimbusGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Limbus Company - Sprite Combat")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 28)
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
            Sinner(Identity("Yi Sang", 100, 100, 5, [Skill("Dim Rift", SinType.PRIDE, 12, 2, "")]), self.sprites["Yi Sang"]),
            Sinner(Identity("Faust", 90, 90, 7, [Skill("Mind Pierce", SinType.LUST, 10, 1, "")]), self.sprites["Faust"]),
            Sinner(Identity("Don Quixote", 110, 110, 4, [Skill("Charge!", SinType.WRATH, 15, 3, "")]), self.sprites["Don Quixote"])
        ]
        for i, s in enumerate(self.sinners):
            pos = (200, 200 + i * 150)
            s.position = s.base_position = pos

        self.enemies = [Enemy("Abnormality", 150, self.sprites["Abnormality"])]
        self.enemies[0].position = (900, 350)

        self.selected_sinner = self.sinners[0]
        self.turn_queue = []
        self.current_turn = 0
        self.setup_turn_queue()

    def setup_turn_queue(self):
        units = [(s, s.identity.speed) for s in self.sinners if s.is_alive()]
        units += [(e, 5) for e in self.enemies if e.is_alive()]
        units.sort(key=lambda x: x[1], reverse=True)
        self.turn_queue = [u[0] for u in units]
        self.current_turn = 0

    def draw_health_bar(self, x, y, cur, maxhp, w=100):
        pygame.draw.rect(self.screen, DARK_GRAY, (x, y, w, 20))
        if maxhp > 0:
            filled = int((cur / maxhp) * w)
            col = GREEN if cur > maxhp * 0.5 else ORANGE if cur > maxhp * 0.25 else RED
            pygame.draw.rect(self.screen, col, (x, y, filled, 20))
        pygame.draw.rect(self.screen, WHITE, (x, y, w, 20), 2)
        hp_text = self.font.render(f"{cur}/{maxhp}", True, WHITE)
        self.screen.blit(hp_text, (x + w + 10, y))

    def draw_units(self):
        for s in self.sinners:
            self.screen.blit(s.sprite, s.sprite.get_rect(center=s.position))
            self.draw_health_bar(s.position[0] - 50, s.position[1] + 60, s.current_hp, s.identity.max_hp)
            if s == self.selected_sinner:
                pygame.draw.circle(self.screen, YELLOW, s.position, 55, 3)

        for e in self.enemies:
            self.screen.blit(e.sprite, e.sprite.get_rect(center=e.position))
            self.draw_health_bar(e.position[0] - 50, e.position[1] + 60, e.current_hp, e.max_hp)

    def execute_skill(self, attacker, skill, target):
        if isinstance(attacker, Sinner):
            attacker.start_attack(target.position)
        total = skill.base_power
        for _ in range(skill.coin_count):
            if random.random() > 0.5:
                total += random.randint(3, 8)
        pygame.time.wait(500)
        target.take_damage(total)
        print(f"{attacker.identity.name if isinstance(attacker, Sinner) else attacker.name} used {skill.name}! -> {total} dmg")

    def next_turn(self):
        self.current_turn = (self.current_turn + 1) % len(self.turn_queue)
        if self.current_turn == 0:
            self.setup_turn_queue()

    def run(self):
        running = True
        while running:
            self.screen.fill(BLACK)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                elif e.type == pygame.KEYDOWN:
                    if self.state == GameState.MENU and e.key == pygame.K_SPACE:
                        self.state = GameState.COMBAT
                    elif self.state == GameState.COMBAT:
                        if e.key == pygame.K_1: self.selected_sinner = self.sinners[0]
                        elif e.key == pygame.K_2: self.selected_sinner = self.sinners[1]
                        elif e.key == pygame.K_3: self.selected_sinner = self.sinners[2]
                        elif e.key == pygame.K_q:
                            if isinstance(self.turn_queue[self.current_turn], Sinner):
                                s = self.turn_queue[self.current_turn]
                                if s == self.selected_sinner and s.is_alive():
                                    self.execute_skill(s, s.identity.skills[0], self.enemies[0])
                                    self.next_turn()

            if self.state == GameState.MENU:
                text = self.font.render("Press SPACE to start", True, WHITE)
                self.screen.blit(text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2))
            elif self.state == GameState.COMBAT:
                for s in self.sinners:
                    s.update_animation()
                self.draw_units()

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    LimbusGame().run()
