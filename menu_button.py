from pygame import Rect


class Button:
    def __init__(self, text, center, fontsize=24, width=200, height=32, on_click=None):
        self.text = text
        self.center = center
        self.width = width
        self.height = height
        self.on_click = on_click

        self.rect = Rect((0, 0), (width, height))
        self.rect.center = center
        self.fontsize = fontsize
        self.bg_color = (100, 100, 100)
        self.hover_color = (150, 150, 150)
        self.text_color = "white"

    def draw(self, screen, mouse_pos):
        is_hovered = self.rect.collidepoint(mouse_pos)

        screen.draw.filled_rect(
            self.rect, self.hover_color if is_hovered else self.bg_color
        )
        screen.draw.text(
            self.text,
            center=self.center,
            fontsize=self.fontsize,
            color=self.text_color,
        )

    def check_click(self, pos):
        if self.rect.collidepoint(pos) and self.on_click:
            self.on_click()
