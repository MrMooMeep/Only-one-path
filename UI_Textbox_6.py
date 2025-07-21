import pygame
import sys

class ScrollableTextbox:
    def __init__(self, rect, font, text_color, bg_color, border_color, padding=8, line_spacing=4):
        self.rect = pygame.Rect(rect)
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.border_color = border_color
        self.padding = padding
        self.line_spacing = line_spacing

        self.text = ""
        self.scroll_offset = 0
        self.max_scroll = 0

        self.rendered_lines = []

    def set_text(self, text):
        self.text = text
        self.rendered_lines = self.wrap_text(text, self.rect.width - 2 * self.padding)
        total_height = len(self.rendered_lines) * (self.font.get_height() + self.line_spacing)
        self.max_scroll = max(0, total_height - (self.rect.height - 2 * self.padding))
        self.scroll_offset = 0

    def scroll(self, dy):
        self.scroll_offset = max(0, min(self.scroll_offset + dy, self.max_scroll))

    def draw(self, surface):
        # Draw box with rounded corners
        pygame.draw.rect(surface, self.bg_color, self.rect, border_radius=12)
        pygame.draw.rect(surface, self.border_color, self.rect, width=3, border_radius=12)

        # Create a surface to render text and clip it
        text_area = pygame.Surface((self.rect.width - 2 * self.padding, len(self.rendered_lines) * (self.font.get_height() + self.line_spacing)), pygame.SRCALPHA)
        text_area.fill(self.bg_color)

        for i, line in enumerate(self.rendered_lines):
            y = i * (self.font.get_height() + self.line_spacing)
            line_surf = self.font.render(line, False, self.text_color)
            text_area.blit(line_surf, (0, y))

        # Clip and blit the scrolled part
        visible_area = pygame.Rect(0, self.scroll_offset, self.rect.width - 2 * self.padding, self.rect.height - 2 * self.padding)
        surface.blit(text_area.subsurface(visible_area), (self.rect.x + self.padding, self.rect.y + self.padding))

    def wrap_text(self, text, max_width):
        words = text.split(" ")
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            if self.font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.strip())
        return lines

# ---- Main ----
def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Scrollable Textbox (Novel Style)")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Courier New", 18)

    # Colors
    bg_color = (155, 188, 15)
    textbox_bg = (248, 248, 248)
    textbox_border = (0, 0, 0)
    text_color = (0, 0, 0)

    textbox = ScrollableTextbox(
        rect=(40, 270, 560, 180), #x,y position, x y size
        font=font,
        text_color=text_color,
        bg_color=textbox_bg,
        border_color=textbox_border
    )

    # Long dummy text
    dummy_text = (
        "In the beginning, there was only a vast silence. From that silence came the wind, "
        "then the stars, and the world was born. This world is full of stories, both ancient and new, "
        "waiting to be told.\n\n"
        "Chapter 1: The Awakening\n"
        "The sun rose slowly over the quiet village of Eldenmoor. Birds chirped, trees whispered, "
        "and the faint aroma of baking bread drifted through the air. Our hero, barely awake, "
        "had no idea what adventures would unfold before the day's end...\n\n"
        "Chapter 2: The Stranger\n"
        "At the market square, a cloaked figure appeared. He asked for no goods and offered no coin. "
        "Instead, he shared a warning, one that chilled the bones of even the bravest townsfolk.\n\n"
        "Chapter 3: The Journey Begins\n"
        "With a worn satchel and a stubborn heart, our hero stepped beyond the village gates. "
        "A journey of hardship, mystery, and courage awaited."
        
        "Chapter Blah, Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah Blah blah blah "
    )

    textbox.set_text(dummy_text)

    # Game loop
    running = True
    while running:
        screen.fill(bg_color)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    textbox.scroll(20)
                elif event.key == pygame.K_UP:
                    textbox.scroll(-20)

            elif event.type == pygame.MOUSEWHEEL:
                textbox.scroll(-event.y * 20)

        textbox.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
