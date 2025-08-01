import pygame
import sys
from ui import TextBox, Button, WHITE, UI_BG, GOLD

# Initialize
pygame.init()
WIDTH, HEIGHT = 1000, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Adventure UI Demo")
clock = pygame.time.Clock()
FPS = 60

# Dialogue Box
dialogue_box = TextBox(300, 420, 660, 180, "Welcome to the adventure. Choose a scene to begin.")

# Scene Buttons (S1–S8)
scene_buttons = []
for i in range(8):
    scene_index = i + 1

    def make_callback(index=scene_index):
        return lambda: dialogue_box.setText(f"You selected Scene {index}.")

    btn = Button(30, 30 + i * 65, 100, 50, f"S{scene_index}", action=make_callback())
    scene_buttons.append(btn)

# Bottom Buttons (Map, Talk, Log, Next)
bottom_buttons = []
bottom_labels = ["Map", "Talk", "Log", "Next"]
for i, label in enumerate(bottom_labels):
    def make_action(name=label):
        return lambda: dialogue_box.setText(f"'{name}' button pressed.")

    btn = Button(300 + i * 120, 610, 100, 40, label, action=make_action())
    bottom_buttons.append(btn)

# Main loop
running = True
while running:
    dt = clock.tick(FPS) / 1000
    screen.fill((15, 15, 35))  # Background color

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for btn in scene_buttons + bottom_buttons:
            btn.handle_event(event)

    # Update and draw all buttons
    for btn in scene_buttons + bottom_buttons:
        btn.update(dt)
        btn.draw(screen)

    # Character placeholder
    pygame.draw.circle(screen, WHITE, (660, 200), 80, 4)  # Head
    pygame.draw.line(screen, WHITE, (660, 280), (660, 380), 4)  # Body
    pygame.draw.line(screen, WHITE, (660, 300), (600, 250), 4)  # Left arm
    pygame.draw.line(screen, WHITE, (660, 300), (720, 250), 4)  # Right arm

    # Dialogue box update & draw
    dialogue_box.update(dt)
    dialogue_box.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()
