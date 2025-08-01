import pygame
import sys
import os
import textwrap
import math

pygame.init()

# Fonts - Using custom fonts will add personality
# Keep the default fonts as fallbacks
TEXT_FONT = pygame.font.Font(None, 36)
BUTTON_FONT = pygame.font.Font(None, 48)
# Try to load custom fonts if available
try:
    TEXT_FONT = pygame.font.Font(os.path.join('assets', 'fonts', 'rpgfont.ttf'), 32)
    BUTTON_FONT = pygame.font.Font(os.path.join('assets', 'fonts', 'rpgfont.ttf'), 40)
except:
    pass  # Fallback to default fonts if custom ones aren't available

# Enhanced Color Palette
WHITE = (255, 255, 255)
TBLACK = (0, 0, 0, 0)  # Transparent black
BLACK = (0, 0, 0)
GRAY = (120, 120, 120)
LIGHT_GRAY = (220, 220, 220)
GOLD = (255, 215, 0)
DARK_GOLD = (184, 134, 11)
HEALTH_COLOR = (220, 50, 50)
MANA_COLOR = (50, 50, 220)
UI_BG = (40, 40, 60, 180)  # Dark blue with transparency

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
            self.boxColor = (40, 40, 60, 5)
            self.hasBorder = True
            self.borderColor = GOLD
        if(not visible):
            self.boxColor = (0, 0, 0, 0)
            self.hasBorder = False
            # self.borderColor = (0, 0, 0, 0)
        

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
        # Update text animation
        if len(self.animated_text) < len(self.text):
            self.animation_timer += dt
            if self.animation_timer >= self.animation_speed:
                self.animated_text += self.text[self.current_char]
                self.current_char += 1
                self.animation_timer = 0
        else:
            self.isFinished = True
            
        # Update cursor blinking
        self.cursor_timer += dt
        if self.cursor_timer >= 0.5:  # Blink every half second
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
        # Create background surface with transparency
        tempSurface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        tempSurface.fill(self.boxColor)
        
        # Draw a slightly darker background for depth
        inner_rect = pygame.Rect(4, 4, self.rect.width-8, self.rect.height-8)
        darker_color = (max(self.boxColor[0]-20, 0), max(self.boxColor[1]-20, 0), 
                        max(self.boxColor[2]-20, 0), self.boxColor[3])
        pygame.draw.rect(tempSurface, darker_color, inner_rect)
        
        # Blit the background
        surface.blit(tempSurface, (self.rect.x, self.rect.y))

        # Draw fancy border if enabled
        if self.hasBorder:
            # Outer border
            pygame.draw.rect(surface, self.borderColor, self.rect, 2)
            
            # Corner accents
            corner_size = 8
            # Top-left
            pygame.draw.line(surface, self.borderColor, 
                            (self.rect.left, self.rect.top + corner_size),
                            (self.rect.left, self.rect.top), 3)
            pygame.draw.line(surface, self.borderColor, 
                            (self.rect.left, self.rect.top),
                            (self.rect.left + corner_size, self.rect.top), 3)
            # Top-right
            pygame.draw.line(surface, self.borderColor, 
                            (self.rect.right - corner_size, self.rect.top),
                            (self.rect.right, self.rect.top), 3)
            pygame.draw.line(surface, self.borderColor, 
                            (self.rect.right, self.rect.top),
                            (self.rect.right, self.rect.top + corner_size), 3)
            # Bottom-left
            pygame.draw.line(surface, self.borderColor, 
                            (self.rect.left, self.rect.bottom - corner_size),
                            (self.rect.left, self.rect.bottom), 3)
            pygame.draw.line(surface, self.borderColor, 
                            (self.rect.left, self.rect.bottom),
                            (self.rect.left + corner_size, self.rect.bottom), 3)
            # Bottom-right
            pygame.draw.line(surface, self.borderColor, 
                            (self.rect.right - corner_size, self.rect.bottom),
                            (self.rect.right, self.rect.bottom), 3)
            pygame.draw.line(surface, self.borderColor, 
                            (self.rect.right, self.rect.bottom),
                            (self.rect.right, self.rect.bottom - corner_size), 3)

        # Draw text with shadow effect
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
            
            # Draw text shadow
            shadow_surf = TEXT_FONT.render(self.text_to_render, True, (30, 30, 30))
            surface.blit(shadow_surf, (self.rect.x + 12, y + 2))
            
            # Draw actual text
            text_surf = TEXT_FONT.render(self.text_to_render, True, WHITE)
            surface.blit(text_surf, (self.rect.x + 12, y))
            y += self.line_height
            
            if y + self.line_height > self.rect.bottom - 15:
                break
                
        # Draw cursor at end of text if still typing
        if not self.isFinished and self.cursor_visible:
            last_line_width = TEXT_FONT.size(self.text_to_render)[0]
            cursor_x = self.rect.x + 12 + last_line_width
            cursor_y = y - self.line_height
            pygame.draw.line(surface, WHITE, 
                            (cursor_x, cursor_y), 
                            (cursor_x, cursor_y + self.line_height - 5), 2)
            
import pygame

class Button:
    def __init__(self, x, y, width, height, text, action=None,
                 color=(20, 20, 40), hover_color=(40, 40, 80),
                 click_color=(60, 60, 100), text_color=(255, 255, 255),
                 border_color=(255, 215, 0), font=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.color = color
        self.hover_color = hover_color
        self.click_color = click_color
        self.text_color = text_color
        self.border_color = border_color
        self.font = font or pygame.font.Font(None, 36)
        self.is_hovered = False
        self.is_clicked = False
        self.border_radius = int(min(width, height) // 3)

    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint((mouse_pos[0],mouse_pos[1])) # 0 accesses the 1st pt and 1 accesses the 2nd pt

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                self.is_clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.is_clicked and self.is_hovered:
                if self.action:
                    self.action()
            self.is_clicked = False

    def draw(self, surface):
        # Choose color
        if self.is_clicked:
            bg_color = self.click_color
        elif self.is_hovered:
            bg_color = self.hover_color
        else:
            bg_color = self.color

        # Draw background
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=self.border_radius)

        # Draw border
        pygame.draw.rect(surface, self.border_color, self.rect, 2, border_radius=self.border_radius)

        # Render text
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

class Text:
    def __init__(self, x, y, width, height, text, font=TEXT_FONT, color=WHITE, shadow=True):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.shadow = shadow
        self.shadow_offset = 2
    
    def draw(self, surface):
        if self.shadow:
            shadow_surf = self.font.render(self.text, True, (30, 30, 30))
            shadow_rect = shadow_surf.get_rect(center=(self.rect.centerx + self.shadow_offset, 
                                                     self.rect.centery + self.shadow_offset))
            surface.blit(shadow_surf, shadow_rect)
        
        text_surf = self.font.render(self.text, True, self.color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

class ProgressBar:
    def __init__(self, x, y, width, height, value, max_value, color, text="", icon=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.value = value
        self.max_value = max_value
        self.color = color
        self.text = text
        self.icon = icon
        self.border_color = WHITE
        self.outline_thickness = 2
        self.background_color = (20, 20, 30, 180)  # Semi-transparent dark background
        self.animate_value = value
        self.animation_speed = 2.0  # Speed to animate value changes
        
    def update(self, dt, new_value=None):
        if new_value is not None:
            self.value = new_value
            
        # Animate the bar smoothly
        if self.animate_value < self.value:
            self.animate_value = min(self.value, self.animate_value + dt * self.animation_speed * self.max_value)
        elif self.animate_value > self.value:
            self.animate_value = max(self.value, self.animate_value - dt * self.animation_speed * self.max_value)
            
    def draw(self, surface):
        # Draw background
        bg_rect = pygame.Rect(self.rect)
        bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        bg_surface.fill(self.background_color)
        surface.blit(bg_surface, bg_rect)
        
        # Draw the progress bar with gradient
        if self.max_value > 0:  # Avoid division by zero
            fill_width = int((self.animate_value / self.max_value) * self.rect.width)
            if fill_width > 0:
                # Create gradient effect
                gradient_surface = pygame.Surface((fill_width, self.rect.height), pygame.SRCALPHA)
                for i in range(self.rect.height):
                    # Lighten color toward top
                    y_ratio = 1.0 - (i / self.rect.height * 0.6)
                    r = min(255, int(self.color[0] * y_ratio + 40))
                    g = min(255, int(self.color[1] * y_ratio + 40))
                    b = min(255, int(self.color[2] * y_ratio + 40))
                    pygame.draw.line(gradient_surface, (r, g, b), 
                                  (0, i), (fill_width, i))
                
                # Add shine effect at top
                shine_height = max(2, int(self.rect.height * 0.3))
                for i in range(shine_height):
                    alpha = 120 - int(120 * (i / shine_height))
                    pygame.draw.line(gradient_surface, (255, 255, 255, alpha), 
                                  (0, i), (fill_width, i))
                
                # Apply gradient
                surface.blit(gradient_surface, self.rect)
        
        # Draw border
        pygame.draw.rect(surface, self.border_color, self.rect, self.outline_thickness)
        
        # Draw text
        if self.text:
            text_surf = TEXT_FONT.render(f"{self.text}: {self.value}/{self.max_value}", True, WHITE)
            text_rect = text_surf.get_rect(center=self.rect.center)
            
            # Draw text shadow
            shadow_surf = TEXT_FONT.render(f"{self.text}: {self.value}/{self.max_value}", True, (30, 30, 30))
            shadow_rect = shadow_surf.get_rect(center=(text_rect.centerx + 2, text_rect.centery + 2))
            surface.blit(shadow_surf, shadow_rect)
            surface.blit(text_surf, text_rect)
            
        # Draw icon if provided
        if self.icon:
            icon_rect = self.icon.get_rect()
            icon_rect.centery = self.rect.centery
            icon_rect.right = self.rect.left - 5  # Position icon to the left of the bar
            surface.blit(self.icon, icon_rect)

# Helper function to create icons
def create_simple_icon(width, height, color, shape="circle"):
    """Create a simple icon surface"""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    if shape == "circle":
        pygame.draw.circle(surface, color, (width//2, height//2), min(width, height)//2)
    elif shape == "sword":
        # Draw a simple sword icon
        pygame.draw.polygon(surface, color, [
            (width//2, 0),  # Tip
            (width//3, height//3),  # Side of blade
            (width//3, height*2//3),  # Handle transition
            (width//5, height),  # Handle end
            (width*4//5, height),  # Handle end
            (width*2//3, height*2//3),  # Handle transition
            (width*2//3, height//3),  # Side of blade
        ])
    elif shape == "shield":
        # Draw a simple shield icon
        pygame.draw.polygon(surface, color, [
            (width//2, 0),  # Top
            (width, height//3),  # Right top
            (width*4//5, height),  # Right bottom
            (width//2, height*4//5),  # Bottom
            (width//5, height),  # Left bottom
            (0, height//3),  # Left top
        ])
    return surface