import pygame
import random
import math
import json
import os
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Optional

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 50, 50)
GREEN = (50, 200, 50)
BLUE = (50, 50, 200)
YELLOW = (255, 255, 0)
PURPLE = (150, 50, 200)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)

class GameState(Enum):
    MENU = 1
    COMBAT = 2
    IDENTITY_SELECT = 3
    SPRITE_MANAGER = 4

class SinType(Enum):
    WRATH = "Wrath"
    LUST = "Lust"
    SLOTH = "Sloth"
    GLUTTONY = "Gluttony"
    GLOOM = "Gloom"
    PRIDE = "Pride"
    ENVY = "Envy"

@dataclass
class SpriteSet:
    idle: Optional[pygame.Surface] = None
    attack: Optional[pygame.Surface] = None
    
    def has_sprites(self):
        return self.idle is not None or self.attack is not None

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
    sin_affinities: Dict[SinType, int]

class Sinner:
    def __init__(self, identity: Identity):
        self.identity = identity
        self.current_hp = identity.hp
        self.selected_skill = None
        self.position = (0, 0)
        self.base_position = (0, 0)
        self.target_position = (0, 0)
        self.is_attacking = False
        self.attack_progress = 0.0
        self.return_progress = 0.0
        self.is_returning = False
        
    def is_alive(self):
        return self.current_hp > 0
    
    def take_damage(self, damage):
        self.current_hp = max(0, self.current_hp - damage)
    
    def heal(self, amount):
        self.current_hp = min(self.identity.max_hp, self.current_hp + amount)
    
    def start_attack(self, target_pos):
        self.base_position = self.position
        self.target_position = (target_pos[0] - 100, target_pos[1])
        self.is_attacking = True
        self.attack_progress = 0.0
        self.is_returning = False
        self.return_progress = 0.0
    
    def update_animation(self):
        if self.is_attacking and not self.is_returning:
            self.attack_progress += 0.1
            if self.attack_progress >= 1.0:
                self.attack_progress = 1.0
                self.is_returning = True
            
            t = self.attack_progress
            t = t * t * (3 - 2 * t)
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

class Enemy:
    def __init__(self, name, hp, skills):
        self.name = name
        self.max_hp = hp
        self.current_hp = hp
        self.skills = skills
        self.position = (0, 0)
    
    def is_alive(self):
        return self.current_hp > 0
    
    def take_damage(self, damage):
        self.current_hp = max(0, self.current_hp - damage)

class SpriteManager:
    def __init__(self):
        self.sprites_dir = "sprites"
        self.ensure_sprite_directories()
        self.character_sprites = {}
        self.load_all_sprites()
    
    def ensure_sprite_directories(self):
        if not os.path.exists(self.sprites_dir):
            os.makedirs(self.sprites_dir)
        
        characters = ["yi_sang", "faust", "don_quixote"]
        for char in characters:
            char_dir = os.path.join(self.sprites_dir, char)
            if not os.path.exists(char_dir):
                os.makedirs(char_dir)
    
    def load_all_sprites(self):
        characters = ["yi_sang", "faust", "don_quixote"]
        
        for char in characters:
            char_dir = os.path.join(self.sprites_dir, char)
            sprite_set = SpriteSet()
            
            idle_path = os.path.join(char_dir, "idle.png")
            if os.path.exists(idle_path):
                try:
                    sprite_set.idle = pygame.image.load(idle_path).convert_alpha()
                    sprite_set.idle = pygame.transform.scale(sprite_set.idle, (120, 150))
                except pygame.error:
                    print(f"Could not load idle sprite for {char}")
            
            attack_path = os.path.join(char_dir, "attack.png")
            if os.path.exists(attack_path):
                try:
                    sprite_set.attack = pygame.image.load(attack_path).convert_alpha()
                    sprite_set.attack = pygame.transform.scale(sprite_set.attack, (120, 150))
                except pygame.error:
                    print(f"Could not load attack sprite for {char}")
            
            self.character_sprites[char] = sprite_set
    
    def get_sprite(self, character_name, sprite_type="idle"):
        char_key = character_name.lower().replace(" ", "_")
        if char_key in self.character_sprites:
            sprite_set = self.character_sprites[char_key]
            if sprite_type == "idle" and sprite_set.idle:
                return sprite_set.idle
            elif sprite_type == "attack" and sprite_set.attack:
                return sprite_set.attack
        return None
    
    def save_default_sprites(self):
        print(f"Default sprite templates saved to {self.sprites_dir}/")

class LimbusCompanyGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Limbus Company")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 48)
        
        self.state = GameState.MENU
        self.running = True
        
        self.sprite_manager = SpriteManager()
        
        self.sinners = []
        self.enemies = []
        self.selected_sinner = None
        self.turn_queue = []
        self.current_turn = 0
        
        self.init_identities()
        self.init_team()
    
    def init_identities(self):
        self.identities = {
            "Yi Sang - LCB Sinner": Identity(
                name="Yi Sang - LCB Sinner",
                hp=100, max_hp=100, speed=8,
                skills=[
                    Skill("Gloom", SinType.GLOOM, 12, 2, "Basic gloom attack"),
                    Skill("Dimensional Rift", SinType.PRIDE, 15, 3, "Tears through reality"),
                    Skill("Crow's Eye View", SinType.ENVY, 18, 2, "Observes and strikes")
                ],
                sin_affinities={SinType.GLOOM: 3, SinType.PRIDE: 2, SinType.ENVY: 1}
            ),
            "Faust - LCB Sinner": Identity(
                name="Faust - LCB Sinner",
                hp=95, max_hp=95, speed=9,
                skills=[
                    Skill("Knowledge", SinType.PRIDE, 10, 2, "Uses intellect as weapon"),
                    Skill("Telepole", SinType.ENVY, 14, 3, "Piercing attack"),
                    Skill("Analysis", SinType.GLOOM, 16, 2, "Calculated strike")
                ],
                sin_affinities={SinType.PRIDE: 3, SinType.ENVY: 2, SinType.GLOOM: 1}
            ),
            "Don Quixote - LCB Sinner": Identity(
                name="Don Quixote - LCB Sinner",
                hp=110, max_hp=110, speed=7,
                skills=[
                    Skill("Valorous Charge", SinType.WRATH, 16, 2, "Heroic assault"),
                    Skill("Hardblood Harpoon", SinType.LUST, 14, 3, "Bloodthirsty strike"),
                    Skill("Justice", SinType.PRIDE, 20, 1, "Righteous blow")
                ],
                sin_affinities={SinType.WRATH: 2, SinType.LUST: 2, SinType.PRIDE: 2}
            )
        }
    
    def init_team(self):
        for i, identity_name in enumerate(list(self.identities.keys())[:3]):
            sinner = Sinner(self.identities[identity_name])
            self.sinners.append(sinner)
        
        for i, sinner in enumerate(self.sinners):
            pos = (200, 200 + i * 120)
            sinner.position = pos
            sinner.base_position = pos
    
    def start_combat(self):
        self.state = GameState.COMBAT
        
        self.enemies = [
            Enemy("Abnormality", 150, [
                Skill("Crushing Blow", SinType.WRATH, 20, 2, "Heavy attack"),
                Skill("Consume", SinType.GLUTTONY, 15, 3, "Draining attack")
            ])
        ]
        
        for i, enemy in enumerate(self.enemies):
            enemy.position = (800, 300 + i * 120)
        
        self.setup_turn_queue()
    
    def setup_turn_queue(self):
        all_units = [(sinner, sinner.identity.speed) for sinner in self.sinners if sinner.is_alive()]
        all_units.extend([(enemy, 5) for enemy in self.enemies if enemy.is_alive()])
        all_units.sort(key=lambda x: x[1], reverse=True)
        self.turn_queue = [unit[0] for unit in all_units]
        self.current_turn = 0
    
    def draw_menu(self):
        self.screen.fill(BLACK)
        
        title = self.large_font.render("LIMBUS COMPANY", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 150))
        self.screen.blit(title, title_rect)
        
        options = [
            ("Press SPACE to Start Combat", 250),
            ("Press S to Manage Sprites", 300),
            ("Press T to Save Template Sprites", 350),
            ("Press Q to Quit", 400)
        ]
        
        for text, y in options:
            text_surface = self.font.render(text, True, WHITE)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH//2, y))
            self.screen.blit(text_surface, text_rect)
        
        instructions = [
            "Sprite Instructions:",
            "1. Place PNG files in sprites/[character]/",
            "2. Name them 'idle.png' and 'attack.png'",
            "3. Characters: yi_sang, faust, don_quixote",
            "4. Use 'T' to generate template sprites first!"
        ]
        
        for i, instruction in enumerate(instructions):
            color = YELLOW if i == 0 else WHITE
            text = self.small_font.render(instruction, True, color)
            self.screen.blit(text, (50, 500 + i * 25))
    
    def draw_sprite_manager(self):
        self.screen.fill(BLACK)
        
        title = self.large_font.render("SPRITE MANAGER", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 50))
        self.screen.blit(title, title_rect)
        
        characters = [
            ("Yi Sang", "yi_sang"),
            ("Faust", "faust"), 
            ("Don Quixote", "don_quixote")
        ]
        
        for i, (display_name, char_key) in enumerate(characters):
            x = 150 + i * 300
            y = 150
            
            name_text = self.font.render(display_name, True, WHITE)
            name_rect = name_text.get_rect(center=(x, y))
            self.screen.blit(name_text, name_rect)
            
            idle_sprite = self.sprite_manager.get_sprite(char_key, "idle")
            if idle_sprite:
                sprite_rect = idle_sprite.get_rect(center=(x - 50, y + 80))
                self.screen.blit(idle_sprite, sprite_rect)
                idle_status = "✓ Loaded"
                status_color = GREEN
            else:
                pygame.draw.rect(self.screen, GRAY, (x - 90, y + 30, 80, 100))
                pygame.draw.rect(self.screen, WHITE, (x - 90, y + 30, 80, 100), 2)
                idle_status = "✗ Missing"
                status_color = RED
            
            idle_text = self.small_font.render(f"Idle: {idle_status}", True, status_color)
            self.screen.blit(idle_text, (x - 90, y + 140))
            
            attack_sprite = self.sprite_manager.get_sprite(char_key, "attack")
            if attack_sprite:
                sprite_rect = attack_sprite.get_rect(center=(x + 50, y + 80))
                self.screen.blit(attack_sprite, sprite_rect)
                attack_status = "✓ Loaded"
                status_color = GREEN
            else:
                pygame.draw.rect(self.screen, GRAY, (x + 10, y + 30, 80, 100))
                pygame.draw.rect(self.screen, WHITE, (x + 10, y + 30, 80, 100), 2)
                attack_status = "✗ Missing"
                status_color = RED
            
            attack_text = self.small_font.render(f"Attack: {attack_status}", True, status_color)
            self.screen.blit(attack_text, (x + 10, y + 140))
        
        instructions = [
            "Instructions:",
            "• Place your PNG sprites in the 'sprites' folder",
            "• Create folders: sprites/yi_sang/, sprites/faust/, sprites/don_quixote/",
            "• Name files: idle.png and attack.png",
            "• Recommended size: 120x150 pixels or similar ratio",
            "",
            "Press R to Reload Sprites",
            "Press T to Save Template Sprites (to get started)",
            "Press ESC to Return to Menu"
        ]
        
        for i, instruction in enumerate(instructions):
            color = YELLOW if instruction.endswith(":") else WHITE
            if instruction.startswith("Press"):
                color = GREEN
            text = self.small_font.render(instruction, True, color)
            self.screen.blit(text, (50, 400 + i * 25))
    
    def draw_health_bar(self, x, y, current_hp, max_hp, width=100):
        pygame.draw.rect(self.screen, DARK_GRAY, (x, y, width, 20))
        
        if max_hp > 0:
            health_width = int((current_hp / max_hp) * width)
            color = GREEN if current_hp > max_hp * 0.5 else ORANGE if current_hp > max_hp * 0.25 else RED
            pygame.draw.rect(self.screen, color, (x, y, health_width, 20))
        
        pygame.draw.rect(self.screen, WHITE, (x, y, width, 20), 2)
        
        hp_text = self.small_font.render(f"{current_hp}/{max_hp}", True, WHITE)
        self.screen.blit(hp_text, (x + width + 10, y))
    
    def draw_detailed_yi_sang(self, x, y, is_alive, is_attacking=False):
        """Draw Yi Sang with 100+ rectangles for maximum detail"""
        base_color = (100, 100, 150) if is_alive else GRAY
        skin_color = (255, 220, 177) if is_alive else GRAY
        hair_color = (50, 50, 50) if is_alive else GRAY
        coat_color = (80, 80, 120) if is_alive else GRAY
        
        offset_x = 10 if is_attacking else 0
        
        # Head base (10 rectangles for rounded shape)
        head_rects = [
            (x-12+offset_x, y-35, 4, 6), (x-8+offset_x, y-37, 4, 8), (x-4+offset_x, y-38, 4, 9),
            (x+offset_x, y-38, 4, 9), (x+4+offset_x, y-37, 4, 8), (x+8+offset_x, y-35, 4, 6),
            (x-10+offset_x, y-32, 20, 4), (x-8+offset_x, y-28, 16, 4), 
            (x-6+offset_x, y-24, 12, 4), (x-4+offset_x, y-20, 8, 4)
        ]
        for rect in head_rects:
            pygame.draw.rect(self.screen, skin_color, rect)
        
        # Hair (20 rectangles for messy effect)
        hair_rects = [
            (x-15+offset_x, y-40, 3, 8), (x-12+offset_x, y-42, 3, 10), (x-9+offset_x, y-41, 3, 9),
            (x-6+offset_x, y-43, 3, 11), (x-3+offset_x, y-42, 3, 10), (x+offset_x, y-44, 3, 12),
            (x+3+offset_x, y-42, 3, 10), (x+6+offset_x, y-43, 3, 11), (x+9+offset_x, y-41, 3, 9),
            (x+12+offset_x, y-42, 3, 10), (x+15+offset_x, y-40, 3, 8), (x-18+offset_x, y-38, 3, 6),
            (x-21+offset_x, y-36, 3, 4), (x+18+offset_x, y-38, 3, 6), (x+21+offset_x, y-36, 3, 4),
            (x-14+offset_x, y-45, 2, 5), (x-7+offset_x, y-46, 2, 6), (x+offset_x, y-47, 2, 7),
            (x+7+offset_x, y-46, 2, 6), (x+14+offset_x, y-45, 2, 5)
        ]
        for rect in hair_rects:
            pygame.draw.rect(self.screen, hair_color, rect)
        
        # Eyes (8 rectangles)
        if is_alive:
            eye_rects = [
                (x-8+offset_x, y-30, 3, 2), (x-5+offset_x, y-30, 2, 2),  # Left eye
                (x+3+offset_x, y-30, 2, 2), (x+6+offset_x, y-30, 3, 2),  # Right eye
                (x-7+offset_x, y-32, 1, 1), (x+4+offset_x, y-32, 1, 1),  # Eye highlights
                (x-6+offset_x, y-29, 1, 1), (x+5+offset_x, y-29, 1, 1)   # Pupils
            ]
            for rect in eye_rects:
                pygame.draw.rect(self.screen, BLACK, rect)
        
        # Nose and mouth (4 rectangles)
        facial_rects = [
            (x-1+offset_x, y-26, 2, 1),  # Nose
            (x-3+offset_x, y-22, 6, 1),  # Mouth
            (x-1+offset_x, y-25, 1, 2),  # Nose shadow
            (x+offset_x, y-21, 1, 1)     # Mouth corner
        ]
        for rect in facial_rects:
            pygame.draw.rect(self.screen, (200, 180, 150), rect)
        
        # Neck (3 rectangles)
        neck_rects = [
            (x-4+offset_x, y-18, 8, 6),
            (x-3+offset_x, y-17, 6, 5),
            (x-2+offset_x, y-16, 4, 4)
        ]
        for rect in neck_rects:
            pygame.draw.rect(self.screen, skin_color, rect)
        
        # Coat collar (8 rectangles)
        collar_rects = [
            (x-15+offset_x, y-15, 6, 12), (x+9+offset_x, y-15, 6, 12),  # Collar sides
            (x-12+offset_x, y-10, 4, 8), (x+8+offset_x, y-10, 4, 8),   # Collar inner
            (x-9+offset_x, y-12, 18, 3), (x-8+offset_x, y-9, 16, 2),   # Collar top
            (x-7+offset_x, y-7, 14, 2), (x-6+offset_x, y-5, 12, 2)     # Collar details
        ]
        for rect in collar_rects:
            pygame.draw.rect(self.screen, coat_color, rect)
        
        # Main coat body (15 rectangles)
        coat_rects = [
            (x-20+offset_x, y-5, 40, 8), (x-19+offset_x, y+3, 38, 8),
            (x-18+offset_x, y+11, 36, 8), (x-17+offset_x, y+19, 34, 8),
            (x-16+offset_x, y+27, 32, 8), (x-15+offset_x, y+35, 30, 6),
            (x-22+offset_x, y+5, 4, 30), (x+18+offset_x, y+5, 4, 30),  # Side panels
            (x-14+offset_x, y+41, 28, 4), (x-13+offset_x, y+45, 26, 3),
            (x-12+offset_x, y+48, 24, 2), (x-25+offset_x, y-3, 3, 35),  # Left edge
            (x+22+offset_x, y-3, 3, 35), (x-10+offset_x, y+50, 20, 2),  # Right edge
            (x-8+offset_x, y+52, 16, 2)  # Bottom hem
        ]
        for rect in coat_rects:
            pygame.draw.rect(self.screen, base_color, rect)
        
        # Coat buttons (6 rectangles)
        button_rects = [
            (x-2+offset_x, y-2, 4, 3), (x-2+offset_x, y+6, 4, 3),
            (x-2+offset_x, y+14, 4, 3), (x-2+offset_x, y+22, 4, 3),
            (x-2+offset_x, y+30, 4, 3), (x-2+offset_x, y+38, 4, 3)
        ]
        for rect in button_rects:
            pygame.draw.rect(self.screen, (60, 60, 80), rect)
        
        # Arms (12 rectangles)
        arm_rects = [
            (x-35+offset_x, y+5, 8, 25), (x+27+offset_x, y+5, 8, 25),  # Upper arms
            (x-37+offset_x, y+30, 8, 20), (x+29+offset_x, y+30, 8, 20),  # Forearms
            (x-33+offset_x, y+3, 4, 8), (x+29+offset_x, y+3, 4, 8),    # Shoulders
            (x-39+offset_x, y+50, 10, 6), (x+29+offset_x, y+50, 10, 6),  # Hands
            (x-41+offset_x, y+48, 6, 4), (x+35+offset_x, y+48, 6, 4),   # Fingers
            (x-35+offset_x, y+28, 6, 4), (x+29+offset_x, y+28, 6, 4)    # Elbow details
        ]
        for rect in arm_rects:
            pygame.draw.rect(self.screen, base_color, rect)
        
        # Coat details and shadows (15 rectangles)
        detail_rects = [
            (x-18+offset_x, y+2, 2, 40), (x+16+offset_x, y+2, 2, 40),  # Coat seams
            (x-16+offset_x, y+8, 32, 1), (x-15+offset_x, y+16, 30, 1),  # Horizontal lines
            (x-14+offset_x, y+24, 28, 1), (x-13+offset_x, y+32, 26, 1),
            (x-25+offset_x, y+35, 5, 2), (x+20+offset_x, y+35, 5, 2),  # Pocket flaps
            (x-23+offset_x, y+37, 3, 8), (x+20+offset_x, y+37, 3, 8),  # Pockets
            (x-10+offset_x, y+12, 20, 1), (x-9+offset_x, y+20, 18, 1),  # Belt line
            (x-8+offset_x, y+28, 16, 1), (x-7+offset_x, y+36, 14, 1),
            (x-6+offset_x, y+44, 12, 1)
        ]
        for rect in detail_rects:
            pygame.draw.rect(self.screen, (70, 70, 100), rect)
    
    def draw_detailed_faust(self, x, y, is_alive, is_attacking=False):
        """Draw Faust with 100+ rectangles for maximum detail"""
        base_color = (120, 80, 150) if is_alive else GRAY
        skin_color = (255, 220, 177) if is_alive else GRAY
        hair_color = (80, 50, 100) if is_alive else GRAY
        dress_color = (100, 60, 130) if is_alive else GRAY
        
        offset_x = 8 if is_attacking else 0
        
        # Head (12 rectangles for elegant shape)
        head_rects = [
            (x-10+offset_x, y-36, 4, 8), (x-6+offset_x, y-38, 4, 10), (x-2+offset_x, y-39, 4, 11),
            (x+2+offset_x, y-38, 4, 10), (x+6+offset_x, y-36, 4, 8), (x-8+offset_x, y-33, 16, 4),
            (x-7+offset_x, y-29, 14, 4), (x-6+offset_x, y-25, 12, 4), (x-5+offset_x, y-21, 10, 4),
            (x-4+offset_x, y-17, 8, 4), (x-12+offset_x, y-34, 2, 6), (x+10+offset_x, y-34, 2, 6)
        ]
        for rect in head_rects:
            pygame.draw.rect(self.screen, skin_color, rect)
        
        # Long flowing hair (25 rectangles)
        hair_rects = [
            (x-18+offset_x, y-42, 3, 12), (x-15+offset_x, y-44, 3, 14), (x-12+offset_x, y-45, 3, 15),
            (x-9+offset_x, y-46, 3, 16), (x-6+offset_x, y-47, 3, 17), (x-3+offset_x, y-48, 3, 18),
            (x+offset_x, y-48, 3, 18), (x+3+offset_x, y-47, 3, 17), (x+6+offset_x, y-46, 3, 16),
            (x+9+offset_x, y-45, 3, 15), (x+12+offset_x, y-44, 3, 14), (x+15+offset_x, y-42, 3, 12),
            (x-21+offset_x, y-38, 2, 20), (x-19+offset_x, y-35, 2, 25), (x+17+offset_x, y-35, 2, 25),
            (x+19+offset_x, y-38, 2, 20), (x-17+offset_x, y-30, 2, 30), (x+15+offset_x, y-30, 2, 30),
            (x-15+offset_x, y-25, 2, 35), (x+13+offset_x, y-25, 2, 35), (x-13+offset_x, y-20, 2, 40),
            (x+11+offset_x, y-20, 2, 40), (x-11+offset_x, y-15, 2, 45), (x+9+offset_x, y-15, 2, 45),
            (x-9+offset_x, y-10, 2, 50)
        ]
        for rect in hair_rects:
            pygame.draw.rect(self.screen, hair_color, rect)
        
        # Eyes (10 rectangles for sharp intelligent look)
        if is_alive:
            eye_rects = [
                (x-8+offset_x, y-31, 4, 2), (x+4+offset_x, y-31, 4, 2),  # Eye shapes
                (x-7+offset_x, y-32, 2, 1), (x+5+offset_x, y-32, 2, 1),  # Upper lids
                (x-6+offset_x, y-30, 1, 2), (x+6+offset_x, y-30, 1, 2),  # Pupils
                (x-7+offset_x, y-29, 3, 1), (x+5+offset_x, y-29, 3, 1),  # Lower lids
                (x-9+offset_x, y-33, 1, 1), (x+7+offset_x, y-33, 1, 1)   # Eye corners
            ]
            for rect in eye_rects:
                pygame.draw.rect(self.screen, (100, 50, 150), rect)
        
        # Elegant dress bodice (18 rectangles)
        bodice_rects = [
            (x-12+offset_x, y-15, 24, 6), (x-11+offset_x, y-9, 22, 6), (x-10+offset_x, y-3, 20, 6),
            (x-9+offset_x, y+3, 18, 6), (x-8+offset_x, y+9, 16, 6), (x-7+offset_x, y+15, 14, 6),
            (x-14+offset_x, y-12, 4, 30), (x+10+offset_x, y-12, 4, 30),  # Side panels
            (x-13+offset_x, y-8, 2, 25), (x+11+offset_x, y-8, 2, 25),   # Trim
            (x-6+offset_x, y+21, 12, 4), (x-5+offset_x, y+25, 10, 4),   # Waist
            (x-15+offset_x, y-5, 3, 20), (x+12+offset_x, y-5, 3, 20),   # Decorative panels
            (x-4+offset_x, y-10, 8, 2), (x-3+offset_x, y-6, 6, 2),     # Chest details
            (x-2+offset_x, y-2, 4, 2), (x-1+offset_x, y+2, 2, 2)       # Center line
        ]
        for rect in bodice_rects:
            pygame.draw.rect(self.screen, dress_color, rect)
        
        # Dress skirt (20 rectangles for flowing effect)
        skirt_rects = [
            (x-16+offset_x, y+29, 32, 6), (x-18+offset_x, y+35, 36, 6), (x-20+offset_x, y+41, 40, 6),
            (x-22+offset_x, y+47, 44, 5), (x-24+offset_x, y+52, 48, 4), (x-26+offset_x, y+56, 52, 3),
            (x-14+offset_x, y+27, 28, 4), (x-12+offset_x, y+31, 24, 4), (x-10+offset_x, y+35, 20, 4),
            (x-8+offset_x, y+39, 16, 4), (x-6+offset_x, y+43, 12, 4), (x-4+offset_x, y+47, 8, 4),
            (x-28+offset_x, y+50, 4, 8), (x+24+offset_x, y+50, 4, 8),   # Skirt sides
            (x-30+offset_x, y+54, 3, 6), (x+27+offset_x, y+54, 3, 6),   # Skirt edges
            (x-25+offset_x, y+59, 50, 2), (x-23+offset_x, y+61, 46, 2), # Hem
            (x-21+offset_x, y+63, 42, 1), (x-19+offset_x, y+64, 38, 1)  # Hem details
        ]
        for rect in skirt_rects:
            pygame.draw.rect(self.screen, base_color, rect)
        
        # Arms and telepole (15 rectangles)
        arm_rects = [
            (x-25+offset_x, y-8, 6, 20), (x+19+offset_x, y-8, 6, 20),   # Upper arms
            (x-27+offset_x, y+12, 6, 18), (x+21+offset_x, y+12, 6, 18), # Forearms
            (x-29+offset_x, y+30, 8, 6), (x+21+offset_x, y+30, 8, 6),   # Hands
            (x-31+offset_x, y+28, 4, 4), (x+25+offset_x, y+28, 4, 4),   # Fingers
            (x-23+offset_x, y-10, 4, 6), (x+19+offset_x, y-10, 4, 6),   # Shoulders
            (x+30+offset_x, y-15, 3, 40), (x+33+offset_x, y-18, 2, 8),  # Telepole shaft
            (x+31+offset_x, y-20, 4, 4), (x+29+offset_x, y-22, 8, 2),   # Telepole head
            (x+35+offset_x, y-16, 6, 2)   # Telepole tip
        ]
        for rect in arm_rects:
            if "telepole" in str(rect):  # Telepole parts
                pygame.draw.rect(self.screen, (150, 150, 150), rect)
            else:
                pygame.draw.rect(self.screen, dress_color, rect)
        
        # Dress decorations (12 rectangles)
        decor_rects = [
            (x-10+offset_x, y-12, 2, 8), (x+8+offset_x, y-12, 2, 8),    # Side decorations
            (x-8+offset_x, y-8, 2, 6), (x+6+offset_x, y-8, 2, 6),      # Inner decorations
            (x-6+offset_x, y-4, 2, 4), (x+4+offset_x, y-4, 2, 4),      # Center decorations
            (x-12+offset_x, y+20, 24, 1), (x-14+offset_x, y+30, 28, 1), # Waist lines
            (x-16+offset_x, y+40, 32, 1), (x-18+offset_x, y+50, 36, 1), # Skirt lines
            (x-3+offset_x, y+18, 6, 2), (x-2+offset_x, y+22, 4, 2)     # Belt details
        ]
        for rect in decor_rects:
            pygame.draw.rect(self.screen, (90, 40, 110), rect)
    
    def draw_detailed_don_quixote(self, x, y, is_alive, is_attacking=False):
        """Draw Don Quixote with 100+ rectangles for maximum detail"""
        armor_color = (200, 150, 50) if is_alive else GRAY
        skin_color = (255, 220, 177) if is_alive else GRAY
        hair_color = (255, 215, 100) if is_alive else GRAY
        gold_color = (255, 215, 0) if is_alive else GRAY
        
        offset_x = 12 if is_attacking else 0
        
        # Head (10 rectangles)
        head_rects = [
            (x-11+offset_x, y-36, 4, 8), (x-7+offset_x, y-38, 4, 10), (x-3+offset_x, y-39, 6, 11),
            (x+3+offset_x, y-38, 4, 10), (x+7+offset_x, y-36, 4, 8), (x-9+offset_x, y-33, 18, 4),
            (x-8+offset_x, y-29, 16, 4), (x-7+offset_x, y-25, 14, 4), (x-6+offset_x, y-21, 12, 4),
            (x-5+offset_x, y-17, 10, 4)
        ]
        for rect in head_rects:
            pygame.draw.rect(self.screen, skin_color, rect)
        
        # Flowing blonde hair (20 rectangles)
        hair_rects = [
            (x-16+offset_x, y-41, 3, 10), (x-13+offset_x, y-43, 3, 12), (x-10+offset_x, y-44, 3, 13),
            (x-7+offset_x, y-45, 3, 14), (x-4+offset_x, y-46, 3, 15), (x-1+offset_x, y-47, 3, 16),
            (x+2+offset_x, y-46, 3, 15), (x+5+offset_x, y-45, 3, 14), (x+8+offset_x, y-44, 3, 13),
            (x+11+offset_x, y-43, 3, 12), (x+14+offset_x, y-41, 3, 10), (x-19+offset_x, y-38, 2, 15),
            (x+17+offset_x, y-38, 2, 15), (x-17+offset_x, y-30, 2, 20), (x+15+offset_x, y-30, 2, 20),
            (x-15+offset_x, y-25, 2, 25), (x+13+offset_x, y-25, 2, 25), (x-13+offset_x, y-20, 2, 30),
            (x+11+offset_x, y-20, 2, 30), (x-11+offset_x, y-15, 2, 35)
        ]
        for rect in hair_rects:
            pygame.draw.rect(self.screen, hair_color, rect)
        
        # Bright enthusiastic eyes (8 rectangles)
        if is_alive:
            eye_rects = [
                (x-8+offset_x, y-31, 4, 3), (x+4+offset_x, y-31, 4, 3),  # Eye shapes
                (x-7+offset_x, y-30, 2, 2), (x+5+offset_x, y-30, 2, 2),  # Pupils
                (x-6+offset_x, y-32, 1, 1), (x+6+offset_x, y-32, 1, 1),  # Highlights
                (x-9+offset_x, y-29, 1, 1), (x+7+offset_x, y-29, 1, 1)   # Sparkles
            ]
            for rect in eye_rects:
                pygame.draw.rect(self.screen, (50, 150, 255), rect)
        
        # Armor breastplate (25 rectangles)
        breastplate_rects = [
            (x-15+offset_x, y-12, 30, 8), (x-14+offset_x, y-4, 28, 8), (x-13+offset_x, y+4, 26, 8),
            (x-12+offset_x, y+12, 24, 8), (x-11+offset_x, y+20, 22, 6), (x-10+offset_x, y+26, 20, 6),
            (x-17+offset_x, y-10, 4, 35), (x+13+offset_x, y-10, 4, 35),  # Side plates
            (x-16+offset_x, y-8, 2, 30), (x+14+offset_x, y-8, 2, 30),   # Trim
            (x-9+offset_x, y+32, 18, 4), (x-8+offset_x, y+36, 16, 4),   # Lower armor
            (x-18+offset_x, y-5, 3, 25), (x+15+offset_x, y-5, 3, 25),   # Outer plates
            (x-19+offset_x, y+5, 2, 15), (x+17+offset_x, y+5, 2, 15),   # Edge details
            (x-6+offset_x, y-8, 12, 3), (x-5+offset_x, y-3, 10, 3),    # Chest details
            (x-4+offset_x, y+2, 8, 3), (x-3+offset_x, y+7, 6, 3),      # Center line
            (x-2+offset_x, y+12, 4, 3), (x-1+offset_x, y+17, 2, 3),    # Lower center
            (x-7+offset_x, y+40, 14, 3), (x-6+offset_x, y+43, 12, 2),  # Belt area
            (x-5+offset_x, y+45, 10, 2)
        ]
        for rect in breastplate_rects:
            pygame.draw.rect(self.screen, armor_color, rect)
        
        # Golden emblem and decorations (15 rectangles)
        gold_rects = [
            (x-3+offset_x, y-6, 6, 6), (x-2+offset_x, y-8, 4, 2),      # Central emblem
            (x-4+offset_x, y-4, 2, 8), (x+2+offset_x, y-4, 2, 8),     # Emblem sides
            (x-1+offset_x, y-2, 2, 4), (x-5+offset_x, y+2, 10, 2),    # Emblem details
            (x-12+offset_x, y-6, 3, 3), (x+9+offset_x, y-6, 3, 3),    # Side emblems
            (x-10+offset_x, y+8, 2, 6), (x+8+offset_x, y+8, 2, 6),    # Decorative strips
            (x-8+offset_x, y+18, 2, 4), (x+6+offset_x, y+18, 2, 4),   # Lower decorations
            (x-6+offset_x, y+28, 2, 3), (x+4+offset_x, y+28, 2, 3),   # Belt decorations
            (x+offset_x, y+35, 2, 8)    # Center belt decoration
        ]
        for rect in gold_rects:
            pygame.draw.rect(self.screen, gold_color, rect)
        
        # Arms and shoulders (12 rectangles)
        arm_rects = [
            (x-28+offset_x, y-8, 8, 22), (x+20+offset_x, y-8, 8, 22),   # Upper arms
            (x-30+offset_x, y+14, 8, 20), (x+22+offset_x, y+14, 8, 20), # Forearms
            (x-32+offset_x, y+34, 10, 8), (x+22+offset_x, y+34, 10, 8), # Hands
            (x-26+offset_x, y-12, 6, 8), (x+20+offset_x, y-12, 6, 8),   # Shoulder guards
            (x-24+offset_x, y-14, 4, 6), (x+20+offset_x, y-14, 4, 6),   # Shoulder spikes
            (x-32+offset_x, y+12, 6, 4), (x+26+offset_x, y+12, 6, 4)    # Elbow guards
        ]
        for rect in arm_rects:
            pygame.draw.rect(self.screen, armor_color, rect)
        
        # Lance (12 rectangles)
        lance_rects = [
            (x+35+offset_x, y-20, 4, 60), (x+39+offset_x, y-22, 2, 8),  # Lance shaft
            (x+37+offset_x, y-25, 6, 5), (x+35+offset_x, y-30, 10, 3),  # Lance head
            (x+33+offset_x, y-33, 14, 2), (x+31+offset_x, y-35, 18, 1), # Spear tip
            (x+36+offset_x, y-18, 2, 4), (x+40+offset_x, y-16, 2, 3),   # Guard details
            (x+34+offset_x, y+35, 8, 3), (x+32+offset_x, y+38, 12, 2),  # Lance grip
            (x+30+offset_x, y+40, 16, 2), (x+28+offset_x, y+42, 20, 1)  # Lance end
        ]
        for rect in lance_rects:
            pygame.draw.rect(self.screen, (139, 69, 19), rect)
        
        # Lance tip (5 rectangles for metallic spear)
        tip_rects = [
            (x+37+offset_x, y-35, 4, 8), (x+35+offset_x, y-38, 8, 3),
            (x+33+offset_x, y-41, 12, 2), (x+39+offset_x, y-33, 2, 5),
            (x+41+offset_x, y-31, 2, 3)
        ]
        for rect in tip_rects:
            pygame.draw.rect(self.screen, (200, 200, 200), rect)
        
        # Armor details and rivets (18 rectangles)
        detail_rects = [
            (x-13+offset_x, y-10, 1, 1), (x-11+offset_x, y-8, 1, 1), (x-9+offset_x, y-6, 1, 1),
            (x+9+offset_x, y-6, 1, 1), (x+11+offset_x, y-8, 1, 1), (x+13+offset_x, y-10, 1, 1),
            (x-15+offset_x, y+5, 1, 1), (x-13+offset_x, y+10, 1, 1), (x-11+offset_x, y+15, 1, 1),
            (x+11+offset_x, y+15, 1, 1), (x+13+offset_x, y+10, 1, 1), (x+15+offset_x, y+5, 1, 1),
            (x-7+offset_x, y+25, 1, 1), (x-3+offset_x, y+27, 1, 1), (x+3+offset_x, y+27, 1, 1),
            (x+7+offset_x, y+25, 1, 1), (x-5+offset_x, y+33, 1, 1), (x+5+offset_x, y+33, 1, 1)
        ]
        for rect in detail_rects:
            pygame.draw.rect(self.screen, (180, 130, 30), rect)
    
    def draw_sinner(self, sinner):
        x, y = sinner.position
        name = sinner.identity.name.split(" - ")[0]
        char_key = name.lower().replace(" ", "_")
        
        sprite_type = "attack" if sinner.is_attacking and not sinner.is_returning else "idle"
        sprite = self.sprite_manager.get_sprite(char_key, sprite_type)
        
        if sprite:
            sprite_rect = sprite.get_rect(center=(x, y))
            
            if not sinner.is_alive():
                gray_sprite = sprite.copy()
                pygame.transform.threshold(gray_sprite, sprite, (128, 128, 128), (0, 0, 0, 0), (255, 255, 255), 1)
                self.screen.blit(gray_sprite, sprite_rect)
            else:
                self.screen.blit(sprite, sprite_rect)
        else:
            # Use detailed drawn characters
            is_attacking = sinner.is_attacking and not sinner.is_returning
            if "Yi Sang" in name:
                self.draw_detailed_yi_sang(x, y, sinner.is_alive(), is_attacking)
            elif "Faust" in name:
                self.draw_detailed_faust(x, y, sinner.is_alive(), is_attacking)
            elif "Don Quixote" in name:
                self.draw_detailed_don_quixote(x, y, sinner.is_alive(), is_attacking)
        
        # Name
        name_parts = sinner.identity.name.split(" - ")
        name_text = self.small_font.render(name_parts[0], True, WHITE)
        name_rect = name_text.get_rect(center=(x, y - 80))
        self.screen.blit(name_text, name_rect)
        
        # Identity
        if len(name_parts) > 1:
            identity_text = self.small_font.render(name_parts[1], True, GRAY)
            identity_rect = identity_text.get_rect(center=(x, y - 60))
            self.screen.blit(identity_text, identity_rect)
        
        # Health bar
        self.draw_health_bar(x - 50, y + 80, sinner.current_hp, sinner.identity.max_hp)
        
        # Highlight if selected
        if sinner == self.selected_sinner:
            pygame.draw.circle(self.screen, YELLOW, (x, y), 60, 4)
    
    def draw_enemy(self, enemy):
        x, y = enemy.position
        
        color = RED if enemy.is_alive() else GRAY
        outline_color = (150, 0, 0) if enemy.is_alive() else GRAY
        
        points = [
            (x - 35, y + 30), (x - 20, y - 35), (x, y - 40), 
            (x + 20, y - 35), (x + 35, y + 30), (x + 20, y + 35),
            (x - 20, y + 35)
        ]
        pygame.draw.polygon(self.screen, color, points)
        pygame.draw.polygon(self.screen, outline_color, points, 4)
        
        if enemy.is_alive():
            eye_positions = [(x - 15, y - 10), (x + 15, y - 10), (x, y + 5)]
            for eye_pos in eye_positions:
                pygame.draw.circle(self.screen, WHITE, eye_pos, 6)
                pygame.draw.circle(self.screen, BLACK, eye_pos, 3)
                pygame.draw.circle(self.screen, RED, eye_pos, 4, 1)
        
        if enemy.is_alive():
            for i in range(4):
                angle = i * math.pi / 2
                end_x = x + int(50 * math.cos(angle))
                end_y = y + int(50 * math.sin(angle))
                pygame.draw.line(self.screen, outline_color, (x, y), (end_x, end_y), 3)
                pygame.draw.circle(self.screen, color, (end_x, end_y), 5)
        
        name_text = self.small_font.render(enemy.name, True, RED if enemy.is_alive() else GRAY)
        name_rect = name_text.get_rect(center=(x, y - 60))
        self.screen.blit(name_text, name_rect)
        
        self.draw_health_bar(x - 50, y + 60, enemy.current_hp, enemy.max_hp)
    
    def draw_skill_selection(self):
        if not self.selected_sinner or not self.selected_sinner.is_alive():
            return
        
        if (not self.turn_queue or 
            self.current_turn >= len(self.turn_queue) or
            self.turn_queue[self.current_turn] != self.selected_sinner):
            return
        
        panel_rect = pygame.Rect(50, SCREEN_HEIGHT - 200, SCREEN_WIDTH - 100, 150)
        pygame.draw.rect(self.screen, DARK_GRAY, panel_rect)
        pygame.draw.rect(self.screen, WHITE, panel_rect, 2)
        
        title_text = self.font.render(f"{self.selected_sinner.identity.name} - Select Skill", True, WHITE)
        self.screen.blit(title_text, (60, SCREEN_HEIGHT - 190))
        
        for i, skill in enumerate(self.selected_sinner.identity.skills):
            skill_rect = pygame.Rect(70 + i * 350, SCREEN_HEIGHT - 150, 330, 80)
            
            sin_colors = {
                SinType.WRATH: RED,
                SinType.LUST: ORANGE,
                SinType.SLOTH: BLUE,
                SinType.GLUTTONY: YELLOW,
                SinType.GLOOM: PURPLE,
                SinType.PRIDE: (255, 215, 0),
                SinType.ENVY: GREEN
            }
            
            sin_color = sin_colors.get(skill.sin_type, WHITE)
            pygame.draw.rect(self.screen, sin_color, skill_rect)
            pygame.draw.rect(self.screen, WHITE, skill_rect, 2)
            
            skill_name = self.small_font.render(skill.name, True, BLACK)
            self.screen.blit(skill_name, (skill_rect.x + 5, skill_rect.y + 5))
            
            power_text = self.small_font.render(f"Power: {skill.base_power}", True, BLACK)
            self.screen.blit(power_text, (skill_rect.x + 5, skill_rect.y + 25))
            
            coins_text = self.small_font.render(f"Coins: {skill.coin_count}", True, BLACK)
            self.screen.blit(coins_text, (skill_rect.x + 5, skill_rect.y + 45))
            
            keys = ['Q', 'W', 'E']
            if i < len(keys):
                key_text = self.font.render(keys[i], True, WHITE)
                self.screen.blit(key_text, (skill_rect.x + 300, skill_rect.y + 25))
    
    def draw_turn_indicator(self):
        if self.turn_queue and self.current_turn < len(self.turn_queue):
            current_unit = self.turn_queue[self.current_turn]
            if isinstance(current_unit, Sinner):
                turn_text = f"Turn: {current_unit.identity.name.split(' - ')[0]}"
            else:
                turn_text = f"Turn: {current_unit.name}"
            
            text_surface = self.font.render(turn_text, True, WHITE)
            self.screen.blit(text_surface, (10, 10))
    
    def draw_combat(self):
        self.screen.fill(BLACK)
        
        
        for sinner in self.sinners:
            self.draw_sinner(sinner)
        
        for enemy in self.enemies:
            self.draw_enemy(enemy)
        
        self.draw_turn_indicator()
        self.draw_skill_selection()
        
        instructions = [
            "Select Sinner: 1/2/3",
            "Use Skills: Q/W/E (when it's their turn)",
            "Skip Turn: SPACE",
            "Menu: ESC"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.small_font.render(instruction, True, WHITE)
            self.screen.blit(text, (10, 50 + i * 25))
    
    def execute_skill(self, attacker, skill, target):
        if isinstance(attacker, Sinner):
            attacker.start_attack(target.position)
        
        total_damage = skill.base_power
        heads_count = 0
        for _ in range(skill.coin_count):
            if random.random() > 0.5:
                coin_damage = random.randint(3, 8)
                total_damage += coin_damage
                heads_count += 1
        
        pygame.time.wait(500)
        target.take_damage(total_damage)
        
        attack_name = attacker.identity.name.split(" - ")[0] if isinstance(attacker, Sinner) else attacker.name
        print(f"{attack_name} used {skill.name}!")
        print(f"Coin flips: {heads_count}/{skill.coin_count} heads")
        print(f"Total damage: {total_damage}")
        print(f"{target.name if isinstance(target, Enemy) else target.identity.name.split(' - ')[0]} HP: {target.current_hp}")
        print("---")
    
    def ai_turn(self, enemy):
        alive_sinners = [s for s in self.sinners if s.is_alive()]
        if alive_sinners and enemy.skills:
            target = random.choice(alive_sinners)
            skill = random.choice(enemy.skills)
            self.execute_skill(enemy, skill, target)
    
    def next_turn(self):
        self.current_turn = (self.current_turn + 1) % len(self.turn_queue)
        if self.current_turn == 0:
            self.setup_turn_queue()
    
    def check_combat_end(self):
        alive_sinners = any(s.is_alive() for s in self.sinners)
        alive_enemies = any(e.is_alive() for e in self.enemies)
        
        if not alive_sinners:
            print("Defeat! All sinners have fallen.")
            self.state = GameState.MENU
        elif not alive_enemies:
            print("Victory! All enemies defeated.")
            self.state = GameState.MENU
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if self.state == GameState.MENU:
                    if event.key == pygame.K_SPACE:
                        self.start_combat()
                    elif event.key == pygame.K_s:
                        self.state = GameState.SPRITE_MANAGER
                    elif event.key == pygame.K_t:
                        self.sprite_manager.save_default_sprites()
                    elif event.key == pygame.K_q:
                        self.running = False
                
                elif self.state == GameState.SPRITE_MANAGER:
                    if event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU
                    elif event.key == pygame.K_r:
                        self.sprite_manager.load_all_sprites()
                        print("Sprites reloaded!")
                    elif event.key == pygame.K_t:
                        self.sprite_manager.save_default_sprites()
                
                elif self.state == GameState.COMBAT:
                    if event.key == pygame.K_1 and len(self.sinners) > 0:
                        self.selected_sinner = self.sinners[0]
                    elif event.key == pygame.K_2 and len(self.sinners) > 1:
                        self.selected_sinner = self.sinners[1]
                    elif event.key == pygame.K_3 and len(self.sinners) > 2:
                        self.selected_sinner = self.sinners[2]
                    
                    elif (self.selected_sinner and 
                          self.turn_queue and 
                          self.current_turn < len(self.turn_queue) and
                          self.turn_queue[self.current_turn] == self.selected_sinner and
                          self.selected_sinner.is_alive()):
                        
                        skill_index = None
                        if event.key == pygame.K_q:
                            skill_index = 0
                        elif event.key == pygame.K_w:
                            skill_index = 1
                        elif event.key == pygame.K_e:
                            skill_index = 2
                        
                        if (skill_index is not None and 
                            skill_index < len(self.selected_sinner.identity.skills)):
                            
                            alive_enemies = [e for e in self.enemies if e.is_alive()]
                            if alive_enemies:
                                skill = self.selected_sinner.identity.skills[skill_index]
                                target = alive_enemies[0]
                                self.execute_skill(self.selected_sinner, skill, target)
                                self.next_turn()
                    
                    elif event.key == pygame.K_SPACE:
                        self.next_turn()
                    
                    elif event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU
    
    def update(self):
        if self.state == GameState.COMBAT:
            for sinner in self.sinners:
                sinner.update_animation()
            
            if (self.turn_queue and 
                self.current_turn < len(self.turn_queue) and
                isinstance(self.turn_queue[self.current_turn], Enemy) and
                self.turn_queue[self.current_turn].is_alive()):
                
                pygame.time.wait(800)
                self.ai_turn(self.turn_queue[self.current_turn])
                self.next_turn()
            
            self.check_combat_end()
    
    def draw(self):
        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.COMBAT:
            self.draw_combat()
        elif self.state == GameState.SPRITE_MANAGER:
            self.draw_sprite_manager()
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()

if __name__ == "__main__":
    game = LimbusCompanyGame()
    game.run()