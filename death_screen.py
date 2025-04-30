import pygame as pg
from settings import *
from font_manager import load_custom_font
from menu import Button, MetallicUIRenderer

class DeathScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.active = False
        self.bg_image = pg.image.load('resources/teksture/loading_bg.png')
        self.bg_image = pg.transform.scale(self.bg_image, RES)
        self.title_font = load_custom_font(72)
        self.subtitle_font = load_custom_font(36)

        self.ui_renderer = MetallicUIRenderer(self.screen)

        button_height = 70
        button_width = 400
        center_x = HALF_WIDTH - button_width // 2

        self.buttons = [
            Button(center_x, HALF_HEIGHT, button_width, button_height, "Reset Level", font_size=42),
            Button(center_x, HALF_HEIGHT + 100, button_width, button_height, "Exit", font_size=42)
        ]

    def start(self):
        self.active = True
        pg.mouse.set_visible(True)

    def handle_events(self):
        if not self.active:
            return False

        mouse_pos = pg.mouse.get_pos()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

            for i, button in enumerate(self.buttons):
                button.update(mouse_pos, self.game)
                if button.is_clicked(event, self.game):
                    if i == 0:
                        self.active = False
                        self.game.reset_current_level()
                        return False

                    elif i == 1:
                        pg.quit()
                        exit()

        return False

    def update(self):
        if not self.active:
            return

    def draw(self):
        if not self.active:
            return

        self.screen.blit(self.bg_image, (0, 0))


        self.ui_renderer.draw_metallic_text(
            "YOU DIED",
            self.title_font,
            (HALF_WIDTH, HALF_HEIGHT - 150),
            bg_alpha=180,
            border_color=(180, 40, 40)
        )

        for button in self.buttons:
            button.draw(self.screen)

        pg.display.flip()
