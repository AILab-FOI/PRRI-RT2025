import pygame as pg
from settings import *
from font_manager import load_custom_font

# Helper functions removed

class UIElement:
    """Base class for UI elements with common functionality"""
    def __init__(self):
        pass

class Button(UIElement):
    def __init__(self, x, y, width, height, text, font_size=36, text_color=(220, 220, 255),
                 bg_color=(40, 45, 80), hover_color=(60, 70, 120)):
        super().__init__()
        self.rect = pg.Rect(x, y, width, height)
        self.text = text
        self.font_size = font_size
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.hovered = False
        self.was_hovered = False
        self.glow_size = 0

        # Load font and render text
        self.font = load_custom_font(self.font_size)
        self.update_text(text)

    def update_text(self, new_text):
        """Update button text and recalculate text surface"""
        self.text = new_text
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def update(self, mouse_pos, game=None):
        # Check previous hover state
        self.was_hovered = self.hovered

        # Update current hover state
        self.hovered = self.rect.collidepoint(mouse_pos)

        # Play hover sound if just started hovering
        if game and self.hovered and not self.was_hovered:
            game.sound.menu_hover.play()

        # Update glow effect when hovered
        if self.hovered:
            self.glow_size = min(self.glow_size + 0.5, 8)
        else:
            self.glow_size = max(self.glow_size - 0.5, 0)

    def draw(self, screen):
        color = self.hover_color if self.hovered else self.bg_color

        pg.draw.rect(screen, color, self.rect, border_radius=12)

        pg.draw.rect(screen, (120, 160, 255), self.rect, 2, border_radius=12)

        screen.blit(self.text_surface, self.text_rect)

    def is_clicked(self, event, game=None):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and self.hovered:
            if game:
                game.sound.menu_click.play()
            return True
        return False

class Slider(UIElement):
    def __init__(self, x, y, width, height, min_val, max_val, initial_val, text, font_size=24):
        super().__init__()
        self.rect = pg.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.text = text
        self.font_size = font_size
        self.dragging = False

        # Load font
        self.font = load_custom_font(self.font_size)

        # Update text and position
        self.update_text()

        # Create handle
        self.handle_rect = pg.Rect(0, 0, 16, height + 14)
        self.update_handle_position()

    def update_text(self):
        """Update the slider text with current value"""
        self.text_surface = self.font.render(f"{self.text}: {int(self.value * 100)}%", True, (220, 220, 255))
        # Center the text above the slider
        self.text_rect = self.text_surface.get_rect(center=(self.rect.centerx, self.rect.y - 15))

    def update_handle_position(self):
        """Update the slider handle position based on current value"""
        normalized_value = (self.value - self.min_val) / (self.max_val - self.min_val)
        handle_x = self.rect.x + (self.rect.width - self.handle_rect.width) * normalized_value
        self.handle_rect.x = handle_x
        self.handle_rect.y = self.rect.y - 7

    def update(self, mouse_pos, mouse_pressed):
        if mouse_pressed[0]:
            if self.handle_rect.collidepoint(mouse_pos):
                self.dragging = True
            elif self.dragging:
                normalized_pos = (mouse_pos[0] - self.rect.x) / self.rect.width
                normalized_pos = max(0, min(1, normalized_pos))
                self.value = self.min_val + normalized_pos * (self.max_val - self.min_val)
                self.update_handle_position()
                self.update_text()
        else:
            self.dragging = False

    def draw(self, screen):
        track_color = (30, 35, 60)
        pg.draw.rect(screen, track_color, self.rect, border_radius=5)

        fill_width = int((self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.width)
        if fill_width > 0:
            fill_rect = pg.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
            fill_color = (60, 100, 200)
            pg.draw.rect(screen, fill_color, fill_rect, border_radius=5)

        # Draw track border
        pg.draw.rect(screen, (100, 140, 240), self.rect, 1, border_radius=5)

        # Draw handle
        handle_color = (80, 120, 220) if self.dragging else (60, 90, 180)
        pg.draw.rect(screen, handle_color, self.handle_rect, border_radius=8)

        # Draw handle border
        pg.draw.rect(screen, (140, 180, 255), self.handle_rect, 1, border_radius=8)

        # Draw text
        screen.blit(self.text_surface, self.text_rect)

class Menu:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.running = True
        self.state = 'main'

        # Create buttons for main menu
        button_height = 60

        # Define button texts
        button_texts = ["Start Game", "Settings", "Exit"]

        # Calculate widths based on text length
        button_widths = []
        for text in button_texts:
            # Load the font to measure text width
            font = load_custom_font(36)

            text_width = font.size(text)[0]
            # Add padding to the text width
            button_width = max(300, text_width + 100)
            button_widths.append(button_width)

        # Use the maximum width for all buttons for consistency
        max_button_width = max(button_widths)

        # Create buttons with calculated width
        center_x = HALF_WIDTH - max_button_width // 2

        self.main_buttons = [
            Button(center_x, HALF_HEIGHT - 100, max_button_width, button_height, button_texts[0]),
            Button(center_x, HALF_HEIGHT, max_button_width, button_height, button_texts[1]),
            Button(center_x, HALF_HEIGHT + 100, max_button_width, button_height, button_texts[2])
        ]

        # Create buttons for settings menu
        self.settings_buttons = [
            Button(center_x, HALF_HEIGHT + 200, max_button_width, button_height, "Back")
        ]

        # Create sliders for settings - center them properly
        slider_width = max_button_width
        slider_center_x = HALF_WIDTH - slider_width // 2
        self.sliders = [
            Slider(slider_center_x, HALF_HEIGHT - 100, slider_width, 10, 0, 1,
                   self.game.sound.music_volume, "Music Volume"),
            Slider(slider_center_x, HALF_HEIGHT, slider_width, 10, 0, 1,
                   self.game.sound.sfx_volume, "SFX Volume")
        ]

        # Load background image
        self.bg_image = pg.image.load('resources/teksture/pocetna.png')
        self.bg_image = pg.transform.scale(self.bg_image, RES)

        # Font for title
        self.title_font = load_custom_font(72)

        self.title_text = self.title_font.render("Galaxy's Doom", True, (220, 220, 255))
        self.title_rect = self.title_text.get_rect(center=(HALF_WIDTH, 100))

        # Add a decorative underline for the title
        self.underline_width = self.title_rect.width * 0.8
        self.underline_rect = pg.Rect(
            HALF_WIDTH - self.underline_width // 2,
            self.title_rect.bottom + 10,
            self.underline_width,
            3
        )

        # Version and credits
        self.version = "v1.0"
        self.credits = "2025 PRRI-RT Team"

        # Create font for version and credits
        self.small_font = load_custom_font(16)

        self.version_text = self.small_font.render(self.version, True, (180, 180, 220))
        self.version_rect = self.version_text.get_rect(topright=(WIDTH - 40, 20))

        self.credits_text = self.small_font.render(self.credits, True, (180, 180, 220))
        self.credits_rect = self.credits_text.get_rect(topleft=(40, 20))

    def update_start_button_text(self):
        """Update the text of the start button based on game state"""
        # Determine the appropriate text based on game state
        new_text = "Continue Game" if (hasattr(self.game, 'game_initialized') and
                                      self.game.game_initialized) else "Start Game"

        # Only update if the text has changed
        if self.main_buttons[0].text != new_text:
            # Store original center position
            center_x = self.main_buttons[0].rect.centerx

            # Update button text
            self.main_buttons[0].update_text(new_text)

            # Adjust button width based on text
            if new_text == "Continue Game":
                # Make button wider for longer text
                text_width = self.main_buttons[0].text_surface.get_width()
                new_width = text_width + 100  # Add padding
                self.main_buttons[0].rect.width = new_width
            else:
                # Reset to original width for "Start Game"
                self.main_buttons[0].rect.width = 300

            # Restore center position
            self.main_buttons[0].rect.centerx = center_x

            # Update text position to center in button
            self.main_buttons[0].text_rect = self.main_buttons[0].text_surface.get_rect(
                center=self.main_buttons[0].rect.center)

    def handle_events(self):
        mouse_pos = pg.mouse.get_pos()
        mouse_pressed = pg.mouse.get_pressed()

        # Update start button text based on game state
        self.update_start_button_text()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

            if self.state == 'main':
                # Update and check main menu buttons
                for button in self.main_buttons:
                    button.update(mouse_pos, self.game)
                    if button.is_clicked(event, self.game):
                        if button.text == "Start Game" or button.text == "Continue Game":
                            self.state = 'game'
                            pg.mouse.set_visible(False)
                            return True
                        elif button.text == "Settings":
                            self.state = 'settings'
                        elif button.text == "Exit":
                            pg.quit()
                            exit()

            elif self.state == 'settings':
                # Update and check settings menu buttons
                for button in self.settings_buttons:
                    button.update(mouse_pos, self.game)
                    if button.is_clicked(event, self.game):
                        if button.text == "Back":
                            self.state = 'main'
                            self.apply_settings()

        # Update sliders if in settings menu
        if self.state == 'settings':
            for slider in self.sliders:
                slider.update(mouse_pos, mouse_pressed)

        return False

    def apply_settings(self):
        # Apply music volume
        self.game.sound.music_volume = self.sliders[0].value
        pg.mixer.music.set_volume(self.sliders[0].value)

        # Apply SFX volume
        self.game.sound.sfx_volume = self.sliders[1].value
        self.game.sound.update_sfx_volume()

    def draw_title(self, title_text, y_pos=100):
        """Draw a simplified title"""
        # Render title text if it's a string, otherwise use the provided surface
        if isinstance(title_text, str):
            title_surface = self.title_font.render(title_text, True, (220, 220, 255))
            title_rect = title_surface.get_rect(center=(HALF_WIDTH, y_pos))
        else:
            title_surface = title_text
            title_rect = self.title_rect

        # Draw the title text
        self.screen.blit(title_surface, title_rect)

        # Draw simple underline
        underline_width = title_rect.width * 0.8
        underline_rect = pg.Rect(
            HALF_WIDTH - underline_width // 2,
            title_rect.bottom + 10,
            underline_width,
            3
        )
        pg.draw.rect(self.screen, (140, 180, 240), underline_rect)

        return underline_rect

    def draw(self):
        # Draw background
        self.screen.blit(self.bg_image, (0, 0))

        if self.state == 'main':
            # Draw main title
            self.draw_title(self.title_text)

            # Draw main menu buttons
            for button in self.main_buttons:
                button.draw(self.screen)

            # Draw version and credits
            self.screen.blit(self.version_text, self.version_rect)
            self.screen.blit(self.credits_text, self.credits_rect)

        elif self.state == 'settings':
            # Draw settings title
            self.draw_title("Settings")

            # Draw sliders
            for slider in self.sliders:
                slider.draw(self.screen)

            # Draw settings buttons
            for button in self.settings_buttons:
                button.draw(self.screen)

        pg.display.flip()

    def run(self):
        pg.mouse.set_visible(True)

        while self.state != 'game':
            start_game = self.handle_events()
            if start_game:
                break
            self.draw()
            self.game.clock.tick(60)
