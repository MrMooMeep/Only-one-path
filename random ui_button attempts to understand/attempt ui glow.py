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
        self.rects = []
        self.level = 0
        self.hover = False
        self.selected = False

        for i in range(box_count):
            rect = pygame.Rect(
                x, y + i * (box_height + box_gap),
                box_width, box_height
            )
            self.rects.append(rect)

    def draw(self, surface):
        for i, rect in enumerate(self.rects):
            if i < self.level:
                color = COLOR_ACTIVE
            elif self.hover or self.selected:
                color = COLOR_HOVER
            else:
                color = COLOR_INACTIVE
            pygame.draw.rect(surface, color, rect, border_radius=4)

    def handle_event(self, event, mouse_pos):
        self.hover = any(rect.collidepoint(mouse_pos) for rect in self.rects)

        if event.type == pygame.MOUSEBUTTONDOWN and self.hover:
            self.selected = True
            self.level = min(self.level + 1, len(self.rects))

    def reset(self):
        self.level = 0
        self.selected = False


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
