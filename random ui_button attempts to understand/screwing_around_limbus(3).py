import pygame
import random
import math
import json
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

class SinType(Enum):
    WRATH = "Wrath"
    LUST = "Lust"
    SLOTH = "Sloth"
    GLUTTONY = "Gluttony"
    GLOOM = "Gloom"
    PRIDE = "Pride"
    ENVY = "Envy"

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
        self.target_position = (target_pos[0] - 100, target_pos[1])  # Stop short of target
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
            
            # Interpolate position
            t = self.attack_progress
            # Use easing for smoother animation
            t = t * t * (3 - 2 * t)  # Smoothstep
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
            
            # Interpolate back to base position
            t = 1.0 - self.return_progress
            t = t * t * (3 - 2 * t)  # Smoothstep
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

class LimbusCompany:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Limbus Company")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 48)
        
        self.state = GameState.MENU
        self.running = True
        
        # Game data
        self.sinners = []
        self.enemies = []
        self.selected_sinner = None
        self.turn_queue = []
        self.current_turn = 0
        
        self.init_identities()
        self.init_team()
    
    def init_identities(self):
        # Sample identities based on Limbus Company
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
        # Create a team of sinners
        for i, identity_name in enumerate(list(self.identities.keys())[:3]):
            sinner = Sinner(self.identities[identity_name])
            self.sinners.append(sinner)
        
        # Position sinners
        for i, sinner in enumerate(self.sinners):
            pos = (200, 200 + i * 120)
            sinner.position = pos
            sinner.base_position = pos
    
    def start_combat(self):
        self.state = GameState.COMBAT
        
        # Create enemies
        self.enemies = [
            Enemy("Abnormality", 150, [
                Skill("Crushing Blow", SinType.WRATH, 20, 2, "Heavy attack"),
                Skill("Consume", SinType.GLUTTONY, 15, 3, "Draining attack")
            ])
        ]
        
        # Position enemies
        for i, enemy in enumerate(self.enemies):
            enemy.position = (800, 300 + i * 120)
        
        self.setup_turn_queue()
    
    def setup_turn_queue(self):
        # Simple turn order based on speed
        all_units = [(sinner, sinner.identity.speed) for sinner in self.sinners if sinner.is_alive()]
        all_units.extend([(enemy, 5) for enemy in self.enemies if enemy.is_alive()])
        all_units.sort(key=lambda x: x[1], reverse=True)
        self.turn_queue = [unit[0] for unit in all_units]
        self.current_turn = 0
    
    def draw_menu(self):
        self.screen.fill(BLACK)
        
        title = self.large_font.render("LIMBUS COMPANY", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 200))
        self.screen.blit(title, title_rect)
        
        start_text = self.font.render("Press SPACE to Start Combat", True, WHITE)
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH//2, 400))
        self.screen.blit(start_text, start_rect)
        
        quit_text = self.font.render("Press Q to Quit", True, WHITE)
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH//2, 450))
        self.screen.blit(quit_text, quit_rect)
    
    def draw_health_bar(self, x, y, current_hp, max_hp, width=100):
        # Background
        pygame.draw.rect(self.screen, DARK_GRAY, (x, y, width, 20))
        
        # Health bar
        if max_hp > 0:
            health_width = int((current_hp / max_hp) * width)
            color = GREEN if current_hp > max_hp * 0.5 else ORANGE if current_hp > max_hp * 0.25 else RED
            pygame.draw.rect(self.screen, color, (x, y, health_width, 20))
        
        # Border
        pygame.draw.rect(self.screen, WHITE, (x, y, width, 20), 2)
        
        # HP text
        hp_text = self.small_font.render(f"{current_hp}/{max_hp}", True, WHITE)
        self.screen.blit(hp_text, (x + width + 10, y))
    
    def draw_sinner(self, sinner):
        x, y = sinner.position
        name = sinner.identity.name.split(" - ")[0]
        
        # Character-specific appearances
        if "Yi Sang" in name:
            self.draw_yi_sang(x, y, sinner.is_alive())
        elif "Faust" in name:
            self.draw_faust(x, y, sinner.is_alive())
        elif "Don Quixote" in name:
            self.draw_don_quixote(x, y, sinner.is_alive())
        else:
            # Default appearance
            color = GREEN if sinner.is_alive() else GRAY
            pygame.draw.circle(self.screen, color, (x, y), 30)
            pygame.draw.circle(self.screen, WHITE, (x, y), 30, 3)
        
        # Name
        name_parts = sinner.identity.name.split(" - ")
        name_text = self.small_font.render(name_parts[0], True, WHITE)
        name_rect = name_text.get_rect(center=(x, y - 70))
        self.screen.blit(name_text, name_rect)
        
        # Identity
        if len(name_parts) > 1:
            identity_text = self.small_font.render(name_parts[1], True, GRAY)
            identity_rect = identity_text.get_rect(center=(x, y - 50))
            self.screen.blit(identity_text, identity_rect)
        
        # Health bar
        self.draw_health_bar(x - 50, y + 50, sinner.current_hp, sinner.identity.max_hp)
        
        # Highlight if selected
        if sinner == self.selected_sinner:
            pygame.draw.circle(self.screen, YELLOW, (x, y), 45, 4)
        
        # Add attack effect
        if sinner.is_attacking and not sinner.is_returning:
            # Draw motion lines or attack effect
            for i in range(3):
                offset = i * 10
                pygame.draw.line(self.screen, WHITE, 
                               (x - 20 - offset, y), (x - 30 - offset, y), 2)
    
    def draw_yi_sang(self, x, y, is_alive):
        color = (100, 100, 150) if is_alive else GRAY
        
        # Body (coat-like shape)
        pygame.draw.ellipse(self.screen, color, (x - 25, y - 10, 50, 40))
        
        # Head
        head_color = (255, 220, 177) if is_alive else GRAY
        pygame.draw.circle(self.screen, head_color, (x, y - 20), 15)
        
        # Hair (dark, messy)
        hair_color = (50, 50, 50) if is_alive else GRAY
        pygame.draw.arc(self.screen, hair_color, (x - 18, y - 35, 36, 25), 0, math.pi, 5)
        
        # Eyes (tired looking)
        if is_alive:
            pygame.draw.circle(self.screen, BLACK, (x - 5, y - 22), 2)
            pygame.draw.circle(self.screen, BLACK, (x + 5, y - 22), 2)
        
        # Coat details
        pygame.draw.line(self.screen, BLACK, (x - 15, y - 5), (x - 15, y + 20), 2)
        pygame.draw.line(self.screen, BLACK, (x + 15, y - 5), (x + 15, y + 20), 2)
    
    def draw_faust(self, x, y, is_alive):
        color = (120, 80, 150) if is_alive else GRAY
        
        # Body (elegant dress-like)
        pygame.draw.polygon(self.screen, color, [
            (x - 20, y + 25), (x + 20, y + 25), 
            (x + 15, y - 5), (x - 15, y - 5)
        ])
        
        # Head
        head_color = (255, 220, 177) if is_alive else GRAY
        pygame.draw.circle(self.screen, head_color, (x, y - 20), 15)
        
        # Hair (long, dark purple)
        hair_color = (80, 50, 100) if is_alive else GRAY
        pygame.draw.ellipse(self.screen, hair_color, (x - 20, y - 35, 40, 30))
        
        # Eyes (sharp, intelligent)
        if is_alive:
            pygame.draw.circle(self.screen, (100, 50, 150), (x - 5, y - 22), 2)
            pygame.draw.circle(self.screen, (100, 50, 150), (x + 5, y - 22), 2)
        
        # Telepole (her weapon)
        if is_alive:
            pygame.draw.line(self.screen, (150, 150, 150), (x + 25, y - 10), (x + 45, y - 30), 3)
            pygame.draw.circle(self.screen, (200, 200, 200), (x + 45, y - 30), 4)
    
    def draw_don_quixote(self, x, y, is_alive):
        color = (200, 150, 50) if is_alive else GRAY
        
        # Body (armor-like)
        pygame.draw.rect(self.screen, color, (x - 20, y - 5, 40, 30))
        
        # Head
        head_color = (255, 220, 177) if is_alive else GRAY
        pygame.draw.circle(self.screen, head_color, (x, y - 20), 15)
        
        # Hair (blonde, flowing)
        hair_color = (255, 215, 100) if is_alive else GRAY
        pygame.draw.ellipse(self.screen, hair_color, (x - 18, y - 35, 36, 25))
        
        # Eyes (bright, enthusiastic)
        if is_alive:
            pygame.draw.circle(self.screen, (50, 150, 255), (x - 5, y - 22), 2)
            pygame.draw.circle(self.screen, (50, 150, 255), (x + 5, y - 22), 2)
        
        # Lance
        if is_alive:
            pygame.draw.line(self.screen, (139, 69, 19), (x + 20, y), (x + 50, y - 20), 4)
            pygame.draw.polygon(self.screen, (150, 150, 150), [
                (x + 50, y - 20), (x + 55, y - 25), (x + 55, y - 15)
            ])
        
        # Armor details
        pygame.draw.circle(self.screen, (255, 215, 0), (x, y), 3)  # Golden emblem
    
    def draw_enemy(self, enemy):
        x, y = enemy.position
        
        # Draw enemy representation (more detailed abnormality)
        color = RED if enemy.is_alive() else GRAY
        outline_color = (150, 0, 0) if enemy.is_alive() else GRAY
        
        # Main body (irregular shape for abnormality feel)
        points = [
            (x - 35, y + 30), (x - 20, y - 35), (x, y - 40), 
            (x + 20, y - 35), (x + 35, y + 30), (x + 20, y + 35),
            (x - 20, y + 35)
        ]
        pygame.draw.polygon(self.screen, color, points)
        pygame.draw.polygon(self.screen, outline_color, points, 4)
        
        # Eyes (multiple, unsettling)
        if enemy.is_alive():
            eye_positions = [(x - 15, y - 10), (x + 15, y - 10), (x, y + 5)]
            for eye_pos in eye_positions:
                pygame.draw.circle(self.screen, WHITE, eye_pos, 6)
                pygame.draw.circle(self.screen, BLACK, eye_pos, 3)
                # Glowing effect
                pygame.draw.circle(self.screen, RED, eye_pos, 4, 1)
        
        # Tentacles or appendages
        if enemy.is_alive():
            for i in range(4):
                angle = i * math.pi / 2
                end_x = x + int(50 * math.cos(angle))
                end_y = y + int(50 * math.sin(angle))
                pygame.draw.line(self.screen, outline_color, (x, y), (end_x, end_y), 3)
                pygame.draw.circle(self.screen, color, (end_x, end_y), 5)
        
        # Name with ominous styling
        name_text = self.small_font.render(enemy.name, True, RED if enemy.is_alive() else GRAY)
        name_rect = name_text.get_rect(center=(x, y - 60))
        self.screen.blit(name_text, name_rect)
        
        # Health bar
        self.draw_health_bar(x - 50, y + 60, enemy.current_hp, enemy.max_hp)
    
    def draw_skill_selection(self):
        if not self.selected_sinner or not self.selected_sinner.is_alive():
            return
        
        # Only show skill selection if it's the selected sinner's turn
        if (not self.turn_queue or 
            self.current_turn >= len(self.turn_queue) or
            self.turn_queue[self.current_turn] != self.selected_sinner):
            return
        
        # Skill selection panel
        panel_rect = pygame.Rect(50, SCREEN_HEIGHT - 200, SCREEN_WIDTH - 100, 150)
        pygame.draw.rect(self.screen, DARK_GRAY, panel_rect)
        pygame.draw.rect(self.screen, WHITE, panel_rect, 2)
        
        # Title
        title_text = self.font.render(f"{self.selected_sinner.identity.name} - Select Skill", True, WHITE)
        self.screen.blit(title_text, (60, SCREEN_HEIGHT - 190))
        
        # Skills
        for i, skill in enumerate(self.selected_sinner.identity.skills):
            skill_rect = pygame.Rect(70 + i * 350, SCREEN_HEIGHT - 150, 330, 80)
            
            # Sin type color
            sin_colors = {
                SinType.WRATH: RED,
                SinType.LUST: ORANGE,
                SinType.SLOTH: BLUE,
                SinType.GLUTTONY: YELLOW,
                SinType.GLOOM: PURPLE,
                SinType.PRIDE: (255, 215, 0),  # Gold
                SinType.ENVY: GREEN
            }
            
            sin_color = sin_colors.get(skill.sin_type, WHITE)
            pygame.draw.rect(self.screen, sin_color, skill_rect)
            pygame.draw.rect(self.screen, WHITE, skill_rect, 2)
            
            # Skill info
            skill_name = self.small_font.render(skill.name, True, BLACK)
            self.screen.blit(skill_name, (skill_rect.x + 5, skill_rect.y + 5))
            
            power_text = self.small_font.render(f"Power: {skill.base_power}", True, BLACK)
            self.screen.blit(power_text, (skill_rect.x + 5, skill_rect.y + 25))
            
            coins_text = self.small_font.render(f"Coins: {skill.coin_count}", True, BLACK)
            self.screen.blit(coins_text, (skill_rect.x + 5, skill_rect.y + 45))
            
            # Key to press (Q, W, E)
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
        
        # Draw battlefield background
        pygame.draw.line(self.screen, WHITE, (SCREEN_WIDTH//2, 0), (SCREEN_WIDTH//2, SCREEN_HEIGHT), 2)
        
        # Draw units
        for sinner in self.sinners:
            self.draw_sinner(sinner)
        
        for enemy in self.enemies:
            self.draw_enemy(enemy)
        
        # Draw UI
        self.draw_turn_indicator()
        
        # Show skill selection if it's a sinner's turn
        self.draw_skill_selection()
        
        # Draw instructions
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
        # Start attack animation for sinners
        if isinstance(attacker, Sinner):
            attacker.start_attack(target.position)
        
        # Simple damage calculation with coin flips
        total_damage = skill.base_power
        
        # Coin flips
        heads_count = 0
        for _ in range(skill.coin_count):
            if random.random() > 0.5:  # Heads
                coin_damage = random.randint(3, 8)
                total_damage += coin_damage
                heads_count += 1
        
        # Apply damage after a short delay for animation
        pygame.time.wait(500)  # Wait for attack animation
        target.take_damage(total_damage)
        
        # Visual feedback
        attack_name = attacker.identity.name.split(" - ")[0] if isinstance(attacker, Sinner) else attacker.name
        print(f"{attack_name} used {skill.name}!")
        print(f"Coin flips: {heads_count}/{skill.coin_count} heads")
        print(f"Total damage: {total_damage}")
        print(f"{target.name if isinstance(target, Enemy) else target.identity.name.split(' - ')[0]} HP: {target.current_hp}")
        print("---")
    
    def ai_turn(self, enemy):
        # Simple AI: attack random alive sinner
        alive_sinners = [s for s in self.sinners if s.is_alive()]
        if alive_sinners and enemy.skills:
            target = random.choice(alive_sinners)
            skill = random.choice(enemy.skills)
            self.execute_skill(enemy, skill, target)
    
    def next_turn(self):
        self.current_turn = (self.current_turn + 1) % len(self.turn_queue)
        if self.current_turn == 0:
            # New round, remove dead units and rebuild queue
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
                    elif event.key == pygame.K_q:
                        self.running = False
                
                elif self.state == GameState.COMBAT:
                    # Select sinner with number keys (1-3)
                    if event.key == pygame.K_1 and len(self.sinners) > 0:
                        self.selected_sinner = self.sinners[0]
                    elif event.key == pygame.K_2 and len(self.sinners) > 1:
                        self.selected_sinner = self.sinners[1]
                    elif event.key == pygame.K_3 and len(self.sinners) > 2:
                        self.selected_sinner = self.sinners[2]
                    
                    # Use skill with Q/W/E keys (if it's the selected sinner's turn)
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
                            
                            # Find target (first alive enemy for now)
                            alive_enemies = [e for e in self.enemies if e.is_alive()]
                            if alive_enemies:
                                skill = self.selected_sinner.identity.skills[skill_index]
                                target = alive_enemies[0]
                                self.execute_skill(self.selected_sinner, skill, target)
                                self.next_turn()
                    
                    # Skip turn
                    elif event.key == pygame.K_SPACE:
                        self.next_turn()
                    
                    # Return to menu
                    elif event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU
    
    def update(self):
        if self.state == GameState.COMBAT:
            # Update sinner animations
            for sinner in self.sinners:
                sinner.update_animation()
            
            # Handle AI turns (only execute immediately, don't auto-advance)
            if (self.turn_queue and 
                self.current_turn < len(self.turn_queue) and
                isinstance(self.turn_queue[self.current_turn], Enemy) and
                self.turn_queue[self.current_turn].is_alive()):
                
                # Add a small delay for AI turns to make them visible
                pygame.time.wait(800)  # Reduced delay
                self.ai_turn(self.turn_queue[self.current_turn])
                self.next_turn()
            
            # Check for combat end
            self.check_combat_end()
    
    def draw(self):
        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.COMBAT:
            self.draw_combat()
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()

if __name__ == "__main__":
    game = LimbusCompany()
    game.run()