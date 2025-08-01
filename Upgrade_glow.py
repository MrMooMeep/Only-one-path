import pygame
from ui import Button  # Uses your uploaded custom Button class

# pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
FPS = 60
WHITE = (255, 255, 255)
BG_COLOR = (25, 25, 40)
ACTIVE_COLOR = (80, 255, 80)
INACTIVE_COLOR = (60, 60, 60)
HOVER_COLOR = (140, 255, 140)

# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Upgrade Indicator with Button")
# clock = pygame.time.Clock()


class UpgradeIndicator:
    def __init__(self, x, y, box_width, box_height, gap, count):
        self.boxes = []
        self.active_count = 0  # Number of activated boxes

        for i in range(count):
            rect = pygame.Rect(x, y + i * (box_height + gap), box_width, box_height)
            self.boxes.append({"rect": rect, "hover": False})

    def draw(self, surface):
        for i, box in enumerate(self.boxes):
            color = INACTIVE_COLOR
            if box["hover"]:
                color = HOVER_COLOR
            if i < self.active_count:
                color = ACTIVE_COLOR
            pygame.draw.rect(surface, color, box["rect"], border_radius=4)

    def update_hover(self, mouse_pos):
        for box in self.boxes:
            box["hover"] = box["rect"].collidepoint(mouse_pos)

    def handle_click(self, mouse_pos):
        for i, box in enumerate(self.boxes):
            if box["rect"].collidepoint(mouse_pos):
                self.active_count = i + 1  # Set all above to active
                return

    def activate_next(self):
        if self.active_count < len(self.boxes):
            self.active_count += 1



# # Initialize components
# indicator = UpgradeIndicator(x=100, y=80, box_width=60, box_height=20, gap=10, count=5)

# # Create a button using your Button class
# def upgrade_action(): #function that lights up the next box
#     indicator.activate_next()

# upgrade_button = Button(250, 150, 150, 60, "Upgrade", action=upgrade_action) # upgrade_action passing a function that activates box lights

# # Game loop
# running = True
# while running:
#     dt = clock.tick(FPS) / 1000
#     screen.fill(BG_COLOR)
#     mouse_pos = pygame.mouse.get_pos()

#     for event in pygame.event.get(): #logic on how to handle mouse clicks
#         if event.type == pygame.QUIT:
#             running = False

#         upgrade_button.handle_event(event)

#         # if event.type == pygame.MOUSEBUTTONDOWN:
#         #     indicator.handle_click(mouse_pos)

#     # Update
#     upgrade_button.update(mouse_pos)
#     indicator.update_hover(mouse_pos)

#     # Draw
#     indicator.draw(screen)
#     upgrade_button.draw(screen)

#     pygame.display.flip()

# pygame.quit()
