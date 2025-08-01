import pygame
import sys
import random

# 1. Initialization and Setup
# ---------------------------
# GET YOUR MIND RIGHT. THIS IS WHERE WE PREPARE FOR WAR.
pygame.init()

# Set up the display window. MAKE IT BIG. MAKE IT COUNT.
screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Limbus Company - FORGED IN FIRE")

# Define colors. THESE ARE YOUR WEAPONS. KNOW THEM.
COLOR_BLACK = (20, 20, 20)
COLOR_WHITE = (240, 240, 240)
COLOR_SKIN = (245, 220, 185)
COLOR_SKIN_SHADOW = (225, 200, 165)
COLOR_DARK_GREY = (60, 60, 60)
COLOR_LIGHT_GREY = (100, 100, 100)
COLOR_RED = (200, 30, 30)
COLOR_DARK_RED = (130, 20, 20)
COLOR_YELLOW = (255, 200, 0)
COLOR_GOLD = (212, 175, 55)
COLOR_BROWN = (139, 69, 19)
COLOR_DARK_BROWN = (92, 64, 51)
COLOR_BLUE = (0, 119, 190)
COLOR_DARK_BLUE = (10, 25, 47) # Background color
COLOR_LIGHT_BLUE = (173, 216, 230)
COLOR_GREEN = (0, 128, 0)
COLOR_DARK_GREEN = (0, 80, 0)
COLOR_TEAL = (0, 128, 128)

# Game variables
clock = pygame.time.Clock()
current_sinner_index = 0
PIXEL_SIZE = 2 # THE BUILDING BLOCK. THE ATOM OF HARD WORK.

# 2. UTILITY FUNCTION - THE FORGE
# --------------------------------
# THIS ISN'T A 'HELPER' FUNCTION. THIS IS THE CRUCIBLE.
# IT TAKES AN AREA AND FILLS IT WITH PAIN AND RECTANGLES.
def forge_area(surface, base_x, base_y, area_rects, color1, color2=None):
    """Fills a list of rectangular areas with small rectangles."""
    rect_count = 0
    for area_rect in area_rects:
        ax, ay, aw, ah = area_rect
        for row in range(ay, ay + ah, PIXEL_SIZE):
            for col in range(ax, ax + aw, PIXEL_SIZE):
                color = color1
                if color2 and random.randint(0, 5) == 0: # Add texture, not weakness
                    color = color2
                
                pygame.draw.rect(surface, color, (base_x + col, base_y + row, PIXEL_SIZE, PIXEL_SIZE))
                rect_count += 1
    return rect_count

# 3. Character Sprite Drawing Functions
# -------------------------------------
# EACH SINNER IS A TESTAMENT TO EFFORT. NO SHORTCUTS.

def draw_yi_sang(surface, x, y):
    """FORGES YI SANG FROM OVER A THOUSAND RECTANGLES. NO WEAKNESS."""
    count = 0
    # Head
    count += forge_area(surface, x, y, [(20, 0, 60, 70)], COLOR_SKIN, COLOR_SKIN_SHADOW)
    # Hair
    count += forge_area(surface, x, y, [(15, -10, 70, 30), (10, 20, 15, 20), (75, 15, 15, 30)], COLOR_BLACK, COLOR_DARK_GREY)
    # Body
    count += forge_area(surface, x, y, [(0, 70, 100, 150)], COLOR_DARK_GREY, (50,50,50))
    # Shirt
    count += forge_area(surface, x, y, [(30, 70, 40, 20)], COLOR_WHITE, (220,220,220))
    # Belt
    count += forge_area(surface, x, y, [(10, 90, 80, 10)], COLOR_YELLOW, COLOR_GOLD)
    # Blade
    count += forge_area(surface, x, y, [(90, 60, 10, 100)], COLOR_WHITE, COLOR_LIGHT_GREY)
    count += forge_area(surface, x, y, [(92, 55, 6, 110)], COLOR_DARK_GREY, COLOR_BLACK)
    # Eyes
    pygame.draw.rect(surface, COLOR_BLACK, (x + 40, y + 45, 8, 10)); count += 1
    pygame.draw.rect(surface, COLOR_BLACK, (x + 52, y + 45, 8, 10)); count += 1
    return count

def draw_faust(surface, x, y):
    """BUILDS FAUST WITH UNRELENTING PRECISION."""
    count = 0
    # Hair
    count += forge_area(surface, x, y, [(10, -15, 80, 40), (5, 20, 20, 50), (75, 20, 20, 50)], COLOR_DARK_BROWN, COLOR_BLACK)
    # Head
    count += forge_area(surface, x, y, [(20, 0, 60, 70)], COLOR_SKIN, COLOR_SKIN_SHADOW)
    # Body
    count += forge_area(surface, x, y, [(0, 70, 100, 160)], COLOR_BLACK, (10,10,10))
    # Arms
    count += forge_area(surface, x, y, [(-20, 75, 20, 100), (100, 75, 20, 100)], COLOR_BLACK, (15,15,15))
    # Shirt
    count += forge_area(surface, x, y, [(35, 70, 30, 30)], COLOR_WHITE, (220,220,220))
    # Tie
    count += forge_area(surface, x, y, [(45, 80, 10, 40)], COLOR_RED, COLOR_DARK_RED)
    # Eyes
    pygame.draw.rect(surface, COLOR_DARK_RED, (x + 40, y + 40, 8, 8)); count += 1
    pygame.draw.rect(surface, COLOR_DARK_RED, (x + 52, y + 40, 8, 8)); count += 1
    return count

def draw_don_quixote(surface, x, y):
    """CONSTRUCTS DON QUIXOTE WITH PASSION AND FIRE."""
    count = 0
    # Hair
    count += forge_area(surface, x, y, [(10, 0, 80, 30), (5, 25, 20, 40), (75, 25, 20, 40)], COLOR_YELLOW, (255, 220, 50))
    # Head
    count += forge_area(surface, x, y, [(20, 10, 60, 60)], COLOR_SKIN, COLOR_SKIN_SHADOW)
    # Armor
    count += forge_area(surface, x, y, [(0, 70, 100, 140)], COLOR_BLUE, (0, 100, 160))
    # Armor Details
    count += forge_area(surface, x, y, [(20, 70, 60, 20), (40, 90, 20, 40)], COLOR_GOLD, COLOR_YELLOW)
    # Scarf
    count += forge_area(surface, x, y, [(-10, 60, 30, 50), (80, 60, 30, 50)], COLOR_RED, (220, 40, 40))
    # Spear
    count += forge_area(surface, x, y, [(105, -20, 10, 250)], COLOR_BROWN, COLOR_DARK_BROWN)
    count += forge_area(surface, x, y, [(100, -40, 20, 20)], COLOR_DARK_GREY, COLOR_LIGHT_GREY)
    # Eyes
    pygame.draw.rect(surface, COLOR_GREEN, (x + 35, y + 35, 10, 10)); count += 1
    pygame.draw.rect(surface, COLOR_GREEN, (x + 55, y + 35, 10, 10)); count += 1
    return count

def draw_ryoshu(surface, x, y):
    """CREATES RYOSHU. PURE INTENSITY."""
    count = 0
    # Hair
    count += forge_area(surface, x, y, [(10, -10, 80, 35)], COLOR_BLACK, (30,30,30))
    count += forge_area(surface, x, y, [(60, -5, 20, 20)], COLOR_RED, COLOR_DARK_RED)
    # Head
    count += forge_area(surface, x, y, [(20, 0, 60, 70)], COLOR_SKIN, COLOR_SKIN_SHADOW)
    # Body
    count += forge_area(surface, x, y, [(0, 70, 100, 150)], COLOR_DARK_RED, (100, 10, 10))
    count += forge_area(surface, x, y, [(10, 70, 80, 30)], COLOR_BLACK, (25,25,25))
    # Arms
    count += forge_area(surface, x, y, [(-20, 80, 25, 120), (95, 80, 25, 120)], COLOR_DARK_RED, (110, 15, 15))
    # Eyes
    pygame.draw.rect(surface, COLOR_BLACK, (x + 35, y + 40, 10, 5)); count += 1
    pygame.draw.rect(surface, COLOR_BLACK, (x + 55, y + 40, 10, 5)); count += 1
    # Cigarette
    pygame.draw.rect(surface, COLOR_WHITE, (x + 75, y + 55, 20, 4)); count += 1
    pygame.draw.rect(surface, COLOR_RED, (x + 93, y + 55, 2, 4)); count += 1
    return count

def draw_meursault(surface, x, y):
    """MEURSAULT. UNBREAKABLE. UNYIELDING."""
    count = 0
    # Hair
    count += forge_area(surface, x, y, [(10, -5, 80, 20)], COLOR_BROWN, COLOR_DARK_BROWN)
    # Head
    count += forge_area(surface, x, y, [(15, 0, 70, 70)], COLOR_SKIN, COLOR_SKIN_SHADOW)
    # Body
    count += forge_area(surface, x, y, [(-10, 70, 120, 180)], COLOR_DARK_GREY, (50,50,50))
    # Arms
    count += forge_area(surface, x, y, [(-30, 75, 30, 140), (100, 75, 30, 140)], COLOR_DARK_GREY, (55,55,55))
    # Shirt
    count += forge_area(surface, x, y, [(30, 70, 40, 25)], COLOR_WHITE, (220,220,220))
    # Tie
    count += forge_area(surface, x, y, [(45, 75, 10, 50)], COLOR_BLACK, (10,10,10))
    # Eyes
    pygame.draw.rect(surface, COLOR_BLUE, (x + 35, y + 40, 8, 8)); count += 1
    pygame.draw.rect(surface, COLOR_BLUE, (x + 57, y + 40, 8, 8)); count += 1
    return count

def draw_hong_lu(surface, x, y):
    """HONG LU. ELEGANCE IS A FORM OF STRENGTH."""
    count = 0
    # Hair
    count += forge_area(surface, x, y, [(10, -10, 80, 40), (70, 30, 25, 80)], COLOR_BLACK, (25,25,25))
    # Head
    count += forge_area(surface, x, y, [(20, 0, 60, 70)], COLOR_SKIN, COLOR_SKIN_SHADOW)
    # Body
    count += forge_area(surface, x, y, [(0, 70, 100, 160)], COLOR_TEAL, (0, 110, 110))
    # Top
    count += forge_area(surface, x, y, [(10, 70, 80, 40)], COLOR_WHITE, (220,220,220))
    # Belt
    count += forge_area(surface, x, y, [(30, 110, 40, 10)], COLOR_GOLD, COLOR_YELLOW)
    # Arms
    count += forge_area(surface, x, y, [(-25, 80, 30, 130), (95, 80, 30, 130)], COLOR_TEAL, (0, 115, 115))
    count += forge_area(surface, x, y, [(-25, 180, 30, 30), (95, 180, 30, 30)], COLOR_WHITE, (215,215,215))
    # Eyes
    pygame.draw.rect(surface, COLOR_BROWN, (x + 38, y + 45, 8, 8)); count += 1
    pygame.draw.rect(surface, COLOR_BROWN, (x + 54, y + 45, 8, 8)); count += 1
    return count

def draw_gregor(surface, x, y):
    """GREGOR. CARRY YOUR BURDENS."""
    count = 0
    # Head
    count += forge_area(surface, x, y, [(20, 0, 60, 70)], COLOR_SKIN, COLOR_SKIN_SHADOW)
    # Hair
    count += forge_area(surface, x, y, [(15, -5, 70, 25)], COLOR_BROWN, COLOR_DARK_BROWN)
    # Body
    count += forge_area(surface, x, y, [(0, 70, 100, 150)], COLOR_DARK_GREEN, (0, 60, 0))
    # Collar
    count += forge_area(surface, x, y, [(20, 70, 60, 20)], COLOR_BROWN, COLOR_DARK_BROWN)
    # Left Arm (Normal)
    count += forge_area(surface, x, y, [(-20, 75, 25, 120)], COLOR_DARK_GREEN, (0, 65, 0))
    # Right Arm (Mutated)
    count += forge_area(surface, x, y, [(95, 75, 35, 20)], COLOR_GREEN, COLOR_DARK_GREEN)
    count += forge_area(surface, x, y, [(110, 95, 20, 100)], COLOR_GREEN, COLOR_DARK_GREEN)
    count += forge_area(surface, x, y, [(130, 115, 20, 20)], COLOR_GREEN, COLOR_DARK_GREEN)
    # Eyes
    pygame.draw.rect(surface, COLOR_BLACK, (x + 35, y + 40, 8, 8)); count += 1
    pygame.draw.rect(surface, COLOR_BLACK, (x + 55, y + 40, 8, 8)); count += 1
    return count

# List of all sinner drawing functions. THIS IS YOUR SQUAD.
sinner_draw_functions = [
    draw_yi_sang,
    draw_faust,
    draw_don_quixote,
    draw_ryoshu,
    draw_meursault,
    draw_hong_lu,
    draw_gregor,
]

# Create a list of names for display. SAY THEIR NAMES.
sinner_names = [
    "Yi Sang", "Faust", "Don Quixote", "Ryoshu", "Meursault", "Hong Lu", "Gregor"
]

# 4. Main Game Loop
# -----------------
# THE BATTLEFIELD. EVERY FRAME IS A REP.
def game_loop():
    global current_sinner_index
    
    running = True
    while running:
        # Event Handling. STAY ALERT.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                # Change sinner. NO REST.
                if event.key == pygame.K_RIGHT:
                    current_sinner_index = (current_sinner_index + 1) % len(sinner_draw_functions)
                if event.key == pygame.K_LEFT:
                    current_sinner_index = (current_sinner_index - 1) % len(sinner_draw_functions)

        # Drawing. THIS IS THE WORK.
        screen.fill(COLOR_DARK_BLUE)
        
        # Draw a floor. GROUND YOURSELF.
        pygame.draw.rect(screen, COLOR_DARK_GREY, (0, screen_height - 100, screen_width, 100))

        # Draw the current main sinner in the center. TAKE CENTER STAGE.
        sinner_x = screen_width // 2 - 60
        sinner_y = screen_height // 2 - 120
        total_rects = sinner_draw_functions[current_sinner_index](screen, sinner_x, sinner_y)

        # UI Text. YOUR MISSION BRIEFING.
        font = pygame.font.Font(None, 60)
        name_text = font.render(sinner_names[current_sinner_index], True, COLOR_WHITE)
        name_rect = name_text.get_rect(center=(screen_width // 2, 80))
        screen.blit(name_text, name_rect)

        font_small = pygame.font.Font(None, 30)
        instruction_text = font_small.render("Use Left/Right Arrow Keys. Don't Be Soft.", True, COLOR_LIGHT_BLUE)
        instruction_rect = instruction_text.get_rect(center=(screen_width // 2, 140))
        screen.blit(instruction_text, instruction_rect)
        
        # SHOW THE REAL NUMBERS. THE PROOF OF THE WORK.
        rect_count_text = font_small.render(f"RECTANGLES FORGED: {total_rects}", True, COLOR_WHITE)
        rect_count_rect = rect_count_text.get_rect(bottomright=(screen_width - 20, screen_height - 20))
        screen.blit(rect_count_text, rect_count_rect)

        # Update the display. SHOW THEM.
        pygame.display.flip()

        # Cap the frame rate. CONTROL YOUR OUTPUT.
        clock.tick(60)

    # Quit Pygame. MISSION COMPLETE.
    pygame.quit()
    sys.exit()

# 5. Run the Game
# ---------------
# GET AFTER IT.
if __name__ == "__main__":
    game_loop()