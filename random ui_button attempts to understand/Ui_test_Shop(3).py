import pygame
import sys
import os
import textwrap
import math

pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Limbus Company - Dante Interface")

# Fonts
TEXT_FONT = pygame.font.Font(None, 36)
BUTTON_FONT = pygame.font.Font(None, 48)
TITLE_FONT = pygame.font.Font(None, 64)

# Enhanced Color Palette
WHITE = (255, 255, 255)
TBLACK = (0, 0, 0, 0)
BLACK = (0, 0, 0)
GRAY = (120, 120, 120)
LIGHT_GRAY = (220, 220, 220)
GOLD = (255, 215, 0)
DARK_GOLD = (184, 134, 11)
HEALTH_COLOR = (220, 50, 50)
MANA_COLOR = (50, 50, 220)
UI_BG = (40, 40, 60, 180)
LIMBUS_RED = (180, 20, 20)
LIMBUS_GOLD = (255, 200, 50)
DANTE_CLOCK_COLOR = (139, 69, 19)

class TextBox:
    def __init__(self, x, y, width, height, text='', bgColor=UI_BG, borderColor=GOLD):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.animated_text = ''
        self.animation_speed = 0.2
        self.animation_timer = 0
        self.current_char = 0
        self.line_height = TEXT_FONT.get_linesize()
        self.max_chars_per_line = (width - 30) // TEXT_FONT.size('A')[0]
        self.lines = self.wrap_text()
        self.boxColor = bgColor
        self.borderColor = borderColor
        self.hasBorder = borderColor is not None
        self.isFinished = False
        self.cursor_visible = True
        self.cursor_timer = 0
        self.shadow_offset = 2
        self.text_to_render = ''

    def isVisible(self, visible):
        if(visible):
            self.boxColor = (40, 40, 60, 200)
            self.hasBorder = True
            self.borderColor = GOLD
        if(not visible):
            self.boxColor = (0, 0, 0, 0)
            self.hasBorder = False

    def setText(self, newText):
        self.text = newText
        self.animated_text = ''
        self.current_char = 0
        self.isFinished = False
        self.lines = self.wrap_text()

    def wrap_text(self):
        words = self.text.split()
        lines = []
        current_line = []
        current_width = 0

        for word in words:
            word_width = TEXT_FONT.size(word + ' ')[0]
            if current_width + word_width <= self.rect.width - 30:
                current_line.append(word)
                current_width += word_width
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_width = word_width

        if current_line:
            lines.append(' '.join(current_line))
        return lines

    def update(self, dt):
        if len(self.animated_text) < len(self.text):
            self.animation_timer += dt
            if self.animation_timer >= self.animation_speed:
                self.animated_text += self.text[self.current_char]
                self.current_char += 1
                self.animation_timer = 0
        else:
            self.isFinished = True
            
        self.cursor_timer += dt
        if self.cursor_timer >= 0.5:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0

    def isTyping(self):
        return not self.isFinished
    
    def skipTyping(self):
        self.animated_text = self.text
        self.current_char = len(self.text)
        self.animation_timer = 0
        self.isFinished = True

    def draw(self, surface):
        tempSurface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        tempSurface.fill(self.boxColor)
        
        inner_rect = pygame.Rect(4, 4, self.rect.width-8, self.rect.height-8)
        darker_color = (max(self.boxColor[0]-20, 0), max(self.boxColor[1]-20, 0), 
                        max(self.boxColor[2]-20, 0), self.boxColor[3])
        pygame.draw.rect(tempSurface, darker_color, inner_rect)
        
        surface.blit(tempSurface, (self.rect.x, self.rect.y))

        if self.hasBorder:
            pygame.draw.rect(surface, self.borderColor, self.rect, 2)
            
            corner_size = 8
            pygame.draw.line(surface, self.borderColor, 
                            (self.rect.left, self.rect.top + corner_size),
                            (self.rect.left, self.rect.top), 3)
            pygame.draw.line(surface, self.borderColor, 
                            (self.rect.left, self.rect.top),
                            (self.rect.left + corner_size, self.rect.top), 3)

        y = self.rect.y + 15
        visible_text = self.animated_text
        
        for line in self.lines:
            if not visible_text:
                break
            if len(visible_text) > len(line):
                self.text_to_render = line
                visible_text = visible_text[len(line):]
            else:
                self.text_to_render = visible_text
                visible_text = ''
            
            shadow_surf = TEXT_FONT.render(self.text_to_render, True, (30, 30, 30))
            surface.blit(shadow_surf, (self.rect.x + 12, y + 2))
            
            text_surf = TEXT_FONT.render(self.text_to_render, True, WHITE)
            surface.blit(text_surf, (self.rect.x + 12, y))
            y += self.line_height
            
            if y + self.line_height > self.rect.bottom - 15:
                break
                
        if not self.isFinished and self.cursor_visible:
            last_line_width = TEXT_FONT.size(self.text_to_render)[0]
            cursor_x = self.rect.x + 12 + last_line_width
            cursor_y = y - self.line_height
            pygame.draw.line(surface, WHITE, 
                            (cursor_x, cursor_y), 
                            (cursor_x, cursor_y + self.line_height - 5), 2)

class Button:
    def __init__(self, x, y, width, height, text, action=None, borderColor=GOLD):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.color = (20, 20, 40, 200)
        self.hoverColor = (40, 40, 80, 230)
        self.clickColor = (60, 60, 100, 255)
        self.isHovered = False
        self.isClicked = False
        self.borderColor = borderColor
        self.icon = None
        self.icon_padding = 10
        self.animation_value = 0
        self.pulse_speed = 2
        self.border_radius = int(min(width, height) // 3)
        
    def set_icon(self, icon_surface):
        self.icon = icon_surface
        
    def update(self, dt):
        if self.isHovered:
            self.animation_value = min(1.0, self.animation_value + dt * self.pulse_speed)
        else:
            self.animation_value = max(0.0, self.animation_value - dt * self.pulse_speed)
        
    def draw(self, surface):
        if self.isClicked:
            color = self.clickColor
            border_color = WHITE
            text_color = WHITE
            offset = 1
        elif self.isHovered:
            glow = int(20 * math.sin(pygame.time.get_ticks() * 0.005) * self.animation_value)
            color = self.hoverColor
            border_color = (min(255, self.borderColor[0] + glow),
                           min(255, self.borderColor[1] + glow),
                           min(255, self.borderColor[2] + glow))
            text_color = WHITE
            offset = 0
        else:
            color = self.color
            border_color = self.borderColor
            text_color = LIGHT_GRAY
            offset = 0
            
        button_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        button_surface.fill((0, 0, 0, 0))
        
        button_rect = pygame.Rect(0, 0, self.rect.width, self.rect.height)
        for i in range(self.rect.height):
            alpha = color[3]
            shade = 1.0 - (i / self.rect.height * 0.4)
            gradient_color = (int(color[0] * shade), int(color[1] * shade), 
                             int(color[2] * shade), alpha)
            
            y_pos = i
            if y_pos < self.border_radius:
                x_offset = self.border_radius - int(math.sqrt(self.border_radius**2 - (self.border_radius - y_pos)**2))
                pygame.draw.line(button_surface, gradient_color, 
                                (x_offset, y_pos), (self.rect.width - x_offset, y_pos))
            elif y_pos >= self.rect.height - self.border_radius:
                y_from_bottom = self.rect.height - y_pos - 1
                x_offset = self.border_radius - int(math.sqrt(self.border_radius**2 - (self.border_radius - y_from_bottom)**2))
                pygame.draw.line(button_surface, gradient_color, 
                                (x_offset, y_pos), (self.rect.width - x_offset, y_pos))
            else:
                pygame.draw.line(button_surface, gradient_color, 
                                (0, y_pos), (self.rect.width, y_pos))
                            
        surface.blit(button_surface, (self.rect.x, self.rect.y + offset))
        
        pygame.draw.rect(surface, border_color, 
                        pygame.Rect(self.rect.x, self.rect.y + offset, 
                                   self.rect.width, self.rect.height), 
                        2, border_radius=self.border_radius)
        
        text_surf = BUTTON_FONT.render(self.text, True, text_color)
        shadow_surf = BUTTON_FONT.render(self.text, True, (30, 30, 30))
        
        text_rect = text_surf.get_rect(center=self.rect.center)
        shadow_rect = shadow_surf.get_rect(center=(self.rect.centerx + 2, self.rect.centery + 2 + offset))
        
        surface.blit(shadow_surf, shadow_rect)
        surface.blit(text_surf, (text_rect.x, text_rect.y + offset))

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.isHovered = self.rect.collidepoint(event.pos)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.isClicked = True
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.isClicked and self.rect.collidepoint(event.pos):
                    if self.action:
                        self.action()
                self.isClicked = False

def draw_dante(surface, x, y, size=100):
    """Draw Dante from Limbus Company with his distinctive clock head"""
    # Clock head (main circle)
    clock_center = (x, y - size//2)
    pygame.draw.circle(surface, DANTE_CLOCK_COLOR, clock_center, size//2, 0)
    pygame.draw.circle(surface, LIMBUS_GOLD, clock_center, size//2, 3)
    
    # Clock face details
    inner_radius = size//3
    pygame.draw.circle(surface, (100, 50, 20), clock_center, inner_radius, 0)
    
    # Clock hands
    hand_length = inner_radius - 5
    # Hour hand (shorter, thicker)
    pygame.draw.line(surface, LIMBUS_GOLD, clock_center, 
                    (clock_center[0] + hand_length//2, clock_center[1] - hand_length//3), 4)
    # Minute hand (longer, thinner)
    pygame.draw.line(surface, LIMBUS_GOLD, clock_center, 
                    (clock_center[0] - hand_length//3, clock_center[1] - hand_length), 3)
    
    # Clock numbers (just a few dots)
    for i in range(12):
        angle = i * (360 / 12) * (math.pi / 180) - math.pi/2
        dot_x = clock_center[0] + int((inner_radius - 8) * math.cos(angle))
        dot_y = clock_center[1] + int((inner_radius - 8) * math.sin(angle))
        pygame.draw.circle(surface, LIMBUS_GOLD, (dot_x, dot_y), 2)
    
    # Body (suit)
    body_width = size//2
    body_height = size
    body_rect = pygame.Rect(x - body_width//2, y, body_width, body_height)
    pygame.draw.rect(surface, (40, 40, 60), body_rect)
    pygame.draw.rect(surface, LIMBUS_GOLD, body_rect, 2)
    
    # Suit details (buttons)
    for i in range(3):
        button_y = y + 20 + i * 25
        pygame.draw.circle(surface, LIMBUS_GOLD, (x, button_y), 3)
    
    # Arms
    arm_length = size//2
    # Left arm
    pygame.draw.line(surface, (40, 40, 60), (x - body_width//2, y + 20), 
                    (x - body_width//2 - arm_length//2, y + 40), 8)
    # Right arm
    pygame.draw.line(surface, (40, 40, 60), (x + body_width//2, y + 20), 
                    (x + body_width//2 + arm_length//2, y + 40), 8)
    
    # Legs
    leg_length = size//2
    # Left leg
    pygame.draw.line(surface, (40, 40, 60), (x - body_width//4, y + body_height), 
                    (x - body_width//4 - 10, y + body_height + leg_length), 8)
    # Right leg
    pygame.draw.line(surface, (40, 40, 60), (x + body_width//4, y + body_height), 
                    (x + body_width//4 + 10, y + body_height + leg_length), 8)

def main():
    clock = pygame.time.Clock()
    
    # Create UI elements based on the sketch
    # Left panel with numbered items
    panel_items = []
    for i in range(8):
        item_text = f"Item {51 + i * 11}"  # 51, 62, 73, etc.
        panel_items.append(TextBox(50, 50 + i * 80, 200, 60, item_text, borderColor=LIMBUS_GOLD))
    
    # Main dialogue box
    dialogue_box = TextBox(450, 550, 700, 200, 
                          "Manager, we've encountered another anomaly in the district. The Sinners are requesting immediate orders.", 
                          borderColor=LIMBUS_GOLD)
    dialogue_box.isVisible(True)
    
    # Bottom action buttons
    action_buttons = [
        Button(450, 700, 150, 50, "Attack", borderColor=LIMBUS_RED),
        Button(620, 700, 150, 50, "Defend", borderColor=LIMBUS_GOLD),
        Button(790, 700, 150, 50, "Skills", borderColor=MANA_COLOR),
        Button(960, 700, 150, 50, "Items", borderColor=GOLD)
    ]
    
    running = True
    dt = 0
    
    while running:
        dt = clock.tick(60) / 1000.0  # Convert to seconds
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Handle button events
            for button in action_buttons:
                button.handle_event(event)
            
            # Skip typing on click
            if event.type == pygame.MOUSEBUTTONDOWN:
                if dialogue_box.isTyping():
                    dialogue_box.skipTyping()
        
        # Update UI elements
        dialogue_box.update(dt)
        for button in action_buttons:
            button.update(dt)
        
        # Draw everything
        # Background gradient
        for y in range(SCREEN_HEIGHT):
            color_value = int(20 + (y / SCREEN_HEIGHT) * 40)
            pygame.draw.line(screen, (color_value, color_value//2, color_value//3), 
                           (0, y), (SCREEN_WIDTH, y))
        
        # Draw left panel background
        panel_bg = pygame.Surface((280, SCREEN_HEIGHT), pygame.SRCALPHA)
        panel_bg.fill((20, 20, 40, 150))
        screen.blit(panel_bg, (20, 0))
        pygame.draw.rect(screen, LIMBUS_GOLD, (20, 0, 280, SCREEN_HEIGHT), 2)
        
        # Draw panel items
        for item in panel_items:
            item.draw(screen)
        
        # Draw Dante in the center area
        draw_dante(screen, SCREEN_WIDTH//2 + 100, 300, 120)
        
        # Draw title
        title_surf = TITLE_FONT.render("LIMBUS COMPANY", True, LIMBUS_GOLD)
        title_shadow = TITLE_FONT.render("LIMBUS COMPANY", True, (30, 30, 30))
        screen.blit(title_shadow, (SCREEN_WIDTH//2 - title_surf.get_width()//2 + 3, 53))
        screen.blit(title_surf, (SCREEN_WIDTH//2 - title_surf.get_width()//2, 50))
        
        # Draw subtitle
        subtitle_surf = TEXT_FONT.render("Manager Interface", True, WHITE)
        screen.blit(subtitle_surf, (SCREEN_WIDTH//2 - subtitle_surf.get_width()//2, 100))
        
        # Draw dialogue box
        dialogue_box.draw(screen)
        
        # Draw action buttons
        for button in action_buttons:
            button.draw(screen)
        
        # Draw frame border
        pygame.draw.rect(screen, LIMBUS_GOLD, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 3)
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()