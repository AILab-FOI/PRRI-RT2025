import pygame as pg
import sys
from settings import *
from font_manager import load_custom_font, resource_path
from menu import Button, MetallicUIRenderer

class DeathScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.active = False
        bg_image_path = resource_path('resources/teksture/theEnd.png')
        self.bg_image = pg.image.load(bg_image_path)
        self.bg_image = pg.transform.scale(self.bg_image, RES)
        self.title_font = load_custom_font(72)
        self.subtitle_font = load_custom_font(36)

        self.ui_renderer = MetallicUIRenderer(self.screen)

        button_height = 70
        button_width = 400
        center_x = HALF_WIDTH - button_width // 2

        self.buttons = [
            Button(center_x, HALF_HEIGHT + 150, button_width, button_height, "Reset Level", font_size=42),
            Button(center_x, HALF_HEIGHT + 250, button_width, button_height, "Exit", font_size=42)
        ]

    def start(self):
        self.active = True
        pg.mouse.set_visible(True)

        pg.mixer.music.stop()
        pg.mixer.stop()

        if self.game.sound.defeat:
            self.original_volume = self.game.sound.defeat.get_volume()
            self.game.sound.defeat.set_volume(0.4)
            self.game.sound.defeat.play()
            pg.time.set_timer(pg.USEREVENT + 2, 500)

    def handle_events(self):
        if not self.active:
            return False

        mouse_pos = pg.mouse.get_pos()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            elif event.type == pg.USEREVENT + 2:
                if hasattr(self, 'original_volume') and self.game.sound.defeat:
                    self.game.sound.defeat.set_volume(self.original_volume)
                pg.time.set_timer(pg.USEREVENT + 2, 0)

            for i, button in enumerate(self.buttons):
                button.update(mouse_pos, self.game)
                if button.is_clicked(event, self.game):
                    if i == 0:
                        self.active = False

                        if self.game.sound.defeat:
                            self.game.sound.defeat.stop()

                        self.game.reset_current_level()
                        return False

                    elif i == 1:
                        pg.quit()
                        sys.exit()

        return False

    def update(self):
        if not self.active:
            return

    def draw(self):
        if not self.active:
            return

        self.screen.blit(self.bg_image, (0, 0))

        for button in self.buttons:
            button.draw(self.screen)

        pg.display.flip()
