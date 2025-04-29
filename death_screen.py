import pygame as pg
from settings import *
from font_manager import load_custom_font
from menu import Button

class DeathScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.active = False

        # Load background image (using the same as loading screen)
        self.bg_image = pg.image.load('resources/teksture/loading_bg.png')
        self.bg_image = pg.transform.scale(self.bg_image, RES)

        # Load fonts
        self.title_font = load_custom_font(72)
        self.subtitle_font = load_custom_font(36)

        # Create title text
        self.title_text = self.title_font.render("YOU DIED", True, (220, 50, 50))
        self.title_rect = self.title_text.get_rect(center=(HALF_WIDTH, HALF_HEIGHT - 150))

        # Create buttons - larger size
        button_height = 70
        button_width = 400
        center_x = HALF_WIDTH - button_width // 2

        self.buttons = [
            Button(center_x, HALF_HEIGHT, button_width, button_height, "Reset Level", font_size=42),
            Button(center_x, HALF_HEIGHT + 100, button_width, button_height, "Exit", font_size=42)
        ]

    def start(self):
        """Activate the death screen"""
        self.active = True
        pg.mouse.set_visible(True)

    def handle_events(self):
        """Handle events for the death screen"""
        if not self.active:
            return False

        mouse_pos = pg.mouse.get_pos()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

            # Update and check buttons
            for i, button in enumerate(self.buttons):
                button.update(mouse_pos, self.game)
                if button.is_clicked(event, self.game):
                    if i == 0:  # Reset Level button
                        self.active = False
                        try:
                            # Reset the current level
                            self.game.reset_current_level()
                            return False  # Continue the game loop
                        except Exception as e:
                            print(f"Error in reset level button: {e}")
                            return False
                    elif i == 1:  # Exit button
                        pg.quit()
                        exit()

        return False

    def update(self):
        """Update the death screen"""
        if not self.active:
            return

    def draw(self):
        """Draw the death screen"""
        if not self.active:
            return

        # Draw background
        self.screen.blit(self.bg_image, (0, 0))

        # Draw title
        self.screen.blit(self.title_text, self.title_rect)

        # Draw buttons
        for button in self.buttons:
            button.draw(self.screen)

        pg.display.flip()
