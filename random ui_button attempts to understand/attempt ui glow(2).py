import pygame

# Constants
WIDTH, HEIGHT = 400, 600
FPS = 60
BOX_WIDTH = 60
BOX_HEIGHT = 20
BOX_GAP = 10
BOX_COUNT = 5
INDICATOR_X = WIDTH // 2 - BOX_WIDTH // 2
INDICATOR_Y = 100

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Upgrade Indicator")
clock = pygame.time.Clock()

# Colors
COLOR_INACTIVE = (60, 60, 60)
COLOR_ACTIVE = (100, 200, 100)
COLOR_HOVER = (150, 255, 150)
BG_COLOR = (30, 30, 30)

# Class for the upgrade indicator
class UpgradeIndicator:
    def __init__(self, x, y, box_width, box_height, box_gap, box_count):
        self.boxes = []
        for i in range(box_count):
            rect = pygame.Rect(
                x, y + i * (box_height + box_gap),
                box_width, box_height
            )
            self.boxes.append({
                "rect": rect,
                "active": False,
                "hover": False
            })

    def draw(self, surface):
        for box in self.boxes:
            if box["active"]:
                color = COLOR_ACTIVE
            elif box["hover"]:
                color = COLOR_HOVER
            else:
                color = COLOR_INACTIVE
            pygame.draw.rect(surface, color, box["rect"], border_radius=4)

    def handle_event(self, event, mouse_pos):
        # Reset hover state
        for box in self.boxes:
            box["hover"] = box["rect"].collidepoint(mouse_pos)

        if event.type == pygame.MOUSEBUTTONDOWN:
            for box in self.boxes:
                if box["rect"].collidepoint(mouse_pos):
                    # Activate only this box, deactivate others
                    for b in self.boxes:
                        b["active"] = False
                    box["active"] = True

    def reset(self):
        for box in self.boxes:
            box["active"] = False
            box["hover"] = False


# Create upgrade indicator
indicator = UpgradeIndicator(INDICATOR_X, INDICATOR_Y, BOX_WIDTH, BOX_HEIGHT, BOX_GAP, BOX_COUNT)

# Main game loop
running = True
while running:
    clock.tick(FPS)
    screen.fill(BG_COLOR)
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        indicator.handle_event(event, mouse_pos)

    indicator.draw(screen)
    pygame.display.flip()

pygame.quit()
