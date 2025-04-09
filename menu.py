import pygame as pg
from settings import *
from random import randint, random

class Button:
    def __init__(self, x, y, width, height, text, font_size=36, text_color=(220, 220, 255),
                 bg_color=(40, 45, 80), hover_color=(60, 70, 120)):
        self.rect = pg.Rect(x, y, width, height)
        self.text = text
        self.font_size = font_size
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.hovered = False
        self.was_hovered = False  # Track previous hover state for sound
        self.pulse = 0  # For pulsing effect
        self.pulse_dir = 1  # Direction of pulse animation
        self.pulse_speed = 0.05  # Speed of pulse animation
        self.glow_size = 0  # For glow effect when hovered

        # Try to load a more futuristic font if available, otherwise use default
        try:
            self.font = pg.font.Font('resources/fonts/kenvector_future.ttf', self.font_size)
        except:
            self.font = pg.font.Font(None, self.font_size)

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

        # Update pulse animation
        self.pulse += self.pulse_speed * self.pulse_dir
        if self.pulse >= 1.0 or self.pulse <= 0.0:
            self.pulse_dir *= -1
            self.pulse = max(0.0, min(1.0, self.pulse))

        # Update glow effect when hovered
        if self.hovered:
            self.glow_size = min(self.glow_size + 0.5, 8)  # Increase glow up to max size
        else:
            self.glow_size = max(self.glow_size - 0.5, 0)  # Decrease glow

    def draw(self, screen):
        # Base color with pulse effect
        if self.hovered:
            # Interpolate between base hover color and brighter hover color
            r = self.hover_color[0] + int(20 * self.pulse)
            g = self.hover_color[1] + int(20 * self.pulse)
            b = self.hover_color[2] + int(40 * self.pulse)
            color = (min(r, 255), min(g, 255), min(b, 255))
        else:
            # Interpolate between base color and slightly brighter color
            r = self.bg_color[0] + int(10 * self.pulse)
            g = self.bg_color[1] + int(10 * self.pulse)
            b = self.bg_color[2] + int(20 * self.pulse)
            color = (min(r, 255), min(g, 255), min(b, 255))

        # Draw glow effect if hovered
        if self.glow_size > 0:
            glow_rect = self.rect.inflate(self.glow_size * 2, self.glow_size * 2)
            pg.draw.rect(screen, (80, 100, 180, 100), glow_rect, border_radius=15)

        # Draw main button with gradient-like effect
        pg.draw.rect(screen, color, self.rect, border_radius=12)

        # Draw futuristic border with accent lines
        pg.draw.rect(screen, (120, 160, 255), self.rect, 2, border_radius=12)  # Main border

        # Draw accent lines on left and right sides
        accent_length = int(self.rect.height * 0.4)
        accent_y = self.rect.centery - accent_length // 2

        # Left accent
        pg.draw.line(screen, (100, 200, 255),
                     (self.rect.left - 1, accent_y),
                     (self.rect.left - 1, accent_y + accent_length),
                     2)

        # Right accent
        pg.draw.line(screen, (100, 200, 255),
                     (self.rect.right + 1, accent_y),
                     (self.rect.right + 1, accent_y + accent_length),
                     2)

        # Draw text with slight shadow for depth
        shadow_offset = 2
        shadow_surface = self.font.render(self.text, True, (20, 20, 40))
        shadow_rect = shadow_surface.get_rect(center=(self.text_rect.centerx + shadow_offset,
                                                     self.text_rect.centery + shadow_offset))
        screen.blit(shadow_surface, shadow_rect)
        screen.blit(self.text_surface, self.text_rect)

    def is_clicked(self, event, game=None):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and self.hovered:
            # Play click sound if game is provided
            if game:
                game.sound.menu_click.play()
            return True
        return False

class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, initial_val, text, font_size=24):
        self.rect = pg.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.text = text
        self.font_size = font_size
        self.dragging = False
        self.pulse = 0  # For pulsing effect
        self.pulse_dir = 1  # Direction of pulse animation
        self.pulse_speed = 0.03  # Speed of pulse animation

        # Try to load a more futuristic font if available, otherwise use default
        try:
            self.font = pg.font.Font('resources/fonts/kenvector_future.ttf', self.font_size)
        except:
            self.font = pg.font.Font(None, self.font_size)

        self.text_surface = self.font.render(f"{self.text}: {int(self.value * 100)}%", True, (220, 220, 255))
        self.text_rect = self.text_surface.get_rect(midleft=(self.rect.x, self.rect.y - 15))
        self.handle_rect = pg.Rect(0, 0, 16, height + 14)
        self.update_handle_position()

    def update_handle_position(self):
        normalized_value = (self.value - self.min_val) / (self.max_val - self.min_val)
        handle_x = self.rect.x + (self.rect.width - self.handle_rect.width) * normalized_value
        self.handle_rect.x = handle_x
        self.handle_rect.y = self.rect.y - 7

    def update(self, mouse_pos, mouse_pressed):
        # Update pulse animation
        self.pulse += self.pulse_speed * self.pulse_dir
        if self.pulse >= 1.0 or self.pulse <= 0.0:
            self.pulse_dir *= -1
            self.pulse = max(0.0, min(1.0, self.pulse))

        if mouse_pressed[0]:
            if self.handle_rect.collidepoint(mouse_pos):
                self.dragging = True
            elif self.dragging:
                # Calculate new value based on mouse position
                normalized_pos = (mouse_pos[0] - self.rect.x) / self.rect.width
                normalized_pos = max(0, min(1, normalized_pos))
                self.value = self.min_val + normalized_pos * (self.max_val - self.min_val)
                self.update_handle_position()
                self.text_surface = self.font.render(f"{self.text}: {int(self.value * 100)}%", True, (220, 220, 255))
        else:
            self.dragging = False

    def draw(self, screen):
        # Draw slider track background with gradient
        track_color = (30, 35, 60)  # Dark blue base color
        pg.draw.rect(screen, track_color, self.rect, border_radius=5)

        # Draw filled portion of the track with a glowing effect
        fill_width = int((self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.width)
        if fill_width > 0:
            fill_rect = pg.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)

            # Base fill color with pulse effect
            r = 60 + int(40 * self.pulse)
            g = 100 + int(40 * self.pulse)
            b = 200 + int(55 * self.pulse)
            fill_color = (min(r, 255), min(g, 255), min(b, 255))

            pg.draw.rect(screen, fill_color, fill_rect, border_radius=5)

        # Draw track border
        pg.draw.rect(screen, (100, 140, 240), self.rect, 1, border_radius=5)

        # Draw handle with glowing effect
        handle_color = (80, 120, 220) if self.dragging else (60, 90, 180)
        pg.draw.rect(screen, handle_color, self.handle_rect, border_radius=8)

        # Draw handle border
        pg.draw.rect(screen, (140, 180, 255), self.handle_rect, 1, border_radius=8)

        # Draw handle accent lines
        line_y1 = self.handle_rect.y + self.handle_rect.height * 0.3
        line_y2 = self.handle_rect.y + self.handle_rect.height * 0.7
        line_x = self.handle_rect.centerx

        pg.draw.line(screen, (180, 220, 255), (line_x, line_y1), (line_x, line_y2), 2)

        # Draw text with slight shadow for depth
        shadow_offset = 1
        shadow_surface = self.font.render(f"{self.text}: {int(self.value * 100)}%", True, (20, 20, 40))
        shadow_rect = shadow_surface.get_rect(midleft=(self.text_rect.x + shadow_offset, self.text_rect.y + shadow_offset))
        screen.blit(shadow_surface, shadow_rect)
        screen.blit(self.text_surface, self.text_rect)

class Menu:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.running = True
        self.state = 'main'  # 'main', 'settings', 'game'

        # Background animation elements
        self.particles = []
        self.create_particles()
        self.last_particle_time = pg.time.get_ticks()
        self.particle_spawn_delay = 200  # ms between particle spawns

        # Create buttons for main menu
        button_width, button_height = 300, 60
        center_x = HALF_WIDTH - button_width // 2

        self.main_buttons = [
            Button(center_x, HALF_HEIGHT - 100, button_width, button_height, "Start Game"),
            Button(center_x, HALF_HEIGHT, button_width, button_height, "Settings"),
            Button(center_x, HALF_HEIGHT + 100, button_width, button_height, "Exit")
        ]

        # Create buttons for settings menu
        self.settings_buttons = [
            Button(center_x, HALF_HEIGHT + 200, button_width, button_height, "Back")
        ]

        # Create sliders for settings
        slider_width = 300
        self.sliders = [
            Slider(center_x, HALF_HEIGHT - 100, slider_width, 10, 0, 1,
                   self.game.sound.music_volume, "Music Volume"),
            Slider(center_x, HALF_HEIGHT, slider_width, 10, 0, 1,
                   self.game.sound.sfx_volume, "SFX Volume")
        ]

        # Load background image
        self.bg_image = pg.image.load('resources/textures/menu_bg.png')
        self.bg_image = pg.transform.scale(self.bg_image, RES)

        # Font for title - try to use futuristic font
        try:
            self.title_font = pg.font.Font('resources/fonts/kenvector_future.ttf', 72)
        except:
            self.title_font = pg.font.Font(None, 72)

        self.title_text = self.title_font.render("PRRI-RT2025", True, (220, 220, 255))
        self.title_rect = self.title_text.get_rect(center=(HALF_WIDTH, 150))

        # Add a decorative underline for the title
        self.underline_width = self.title_rect.width * 0.8
        self.underline_rect = pg.Rect(
            HALF_WIDTH - self.underline_width // 2,
            self.title_rect.bottom + 10,
            self.underline_width,
            3
        )

        # Animation variables for title effects
        self.title_pulse = 0
        self.title_pulse_dir = 1

        # Version and credits
        self.version = "v1.0"
        self.credits = "© 2025 PRRI-RT Team"

        # Create font for version and credits
        try:
            self.small_font = pg.font.Font('resources/fonts/kenvector_future.ttf', 16)
        except:
            self.small_font = pg.font.Font(None, 16)

        self.version_text = self.small_font.render(self.version, True, (180, 180, 220))
        self.version_rect = self.version_text.get_rect(bottomright=(WIDTH - 20, HEIGHT - 10))

        self.credits_text = self.small_font.render(self.credits, True, (180, 180, 220))
        self.credits_rect = self.credits_text.get_rect(bottomleft=(20, HEIGHT - 10))

    def create_particles(self, count=15):
        """Create initial background particles"""
        for _ in range(count):
            # Random position, size, speed and color
            x = randint(0, WIDTH)
            y = randint(0, HEIGHT)
            size = randint(1, 3)
            speed = random() * 0.5 + 0.2
            color = (randint(40, 100), randint(80, 150), randint(180, 255), randint(20, 100))
            self.particles.append({'x': x, 'y': y, 'size': size, 'speed': speed, 'color': color})

    def update_particles(self):
        """Update particle positions and create new ones as needed"""
        # Move existing particles
        for particle in self.particles[:]:  # Use a copy to allow removal
            particle['y'] -= particle['speed']  # Move upward

            # Remove particles that have moved off screen
            if particle['y'] < -10:
                self.particles.remove(particle)

        # Add new particles occasionally
        current_time = pg.time.get_ticks()
        if current_time - self.last_particle_time > self.particle_spawn_delay:
            self.last_particle_time = current_time
            # Add 1-3 new particles
            for _ in range(randint(1, 3)):
                x = randint(0, WIDTH)
                y = HEIGHT + 5  # Start just below the screen
                size = randint(1, 3)
                speed = random() * 0.5 + 0.2
                color = (randint(40, 100), randint(80, 150), randint(180, 255), randint(20, 100))
                self.particles.append({'x': x, 'y': y, 'size': size, 'speed': speed, 'color': color})

    def draw_particles(self):
        """Draw background particles"""
        for particle in self.particles:
            # Create a small surface with alpha for the particle
            particle_surface = pg.Surface((particle['size'] * 2, particle['size'] * 2), pg.SRCALPHA)
            pg.draw.circle(particle_surface, particle['color'],
                          (particle['size'], particle['size']), particle['size'])
            self.screen.blit(particle_surface, (particle['x'], particle['y']))

    def handle_events(self):
        mouse_pos = pg.mouse.get_pos()
        mouse_pressed = pg.mouse.get_pressed()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

            if self.state == 'main':
                # Update and check main menu buttons
                for button in self.main_buttons:
                    button.update(mouse_pos, self.game)
                    if button.is_clicked(event, self.game):
                        if button.text == "Start Game":
                            self.state = 'game'
                            pg.mouse.set_visible(False)
                            return True  # Start the game
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

        return False  # Don't start the game yet

    def apply_settings(self):
        # Apply music volume
        self.game.sound.music_volume = self.sliders[0].value
        pg.mixer.music.set_volume(self.sliders[0].value)

        # Apply SFX volume
        self.game.sound.sfx_volume = self.sliders[1].value
        self.game.sound.update_sfx_volume()

        # No mouse sensitivity setting anymore

    def draw(self):
        # Draw background
        self.screen.blit(self.bg_image, (0, 0))

        # Update and draw particles
        self.update_particles()
        self.draw_particles()

        # Update title pulse effect
        self.title_pulse += 0.02 * self.title_pulse_dir
        if self.title_pulse >= 1.0 or self.title_pulse <= 0.0:
            self.title_pulse_dir *= -1
            self.title_pulse = max(0.0, min(1.0, self.title_pulse))

        # Calculate pulse color for titles and accents
        underline_color = (100 + int(80 * self.title_pulse),
                          140 + int(60 * self.title_pulse),
                          240)

        # Set up common variables for accent lines
        accent_length = 20
        accent_gap = 5

        if self.state == 'main':
            # Draw title with glow effect (only in main menu)
            glow_size = 2 + int(self.title_pulse * 3)
            glow_color = (80, 100, 200, 150)  # Blue glow
            glow_rect = self.title_rect.inflate(glow_size * 2, glow_size * 2)

            # Create a temporary surface for the glow effect
            glow_surface = pg.Surface((glow_rect.width, glow_rect.height), pg.SRCALPHA)
            pg.draw.rect(glow_surface, glow_color, (0, 0, glow_rect.width, glow_rect.height), border_radius=15)

            # Apply the glow effect
            self.screen.blit(glow_surface, glow_rect)

            # Draw the title text
            self.screen.blit(self.title_text, self.title_rect)

            # Draw decorative underline with pulse effect
            pg.draw.rect(self.screen, underline_color, self.underline_rect)

            # Left accent
            pg.draw.line(self.screen, underline_color,
                        (self.underline_rect.left - accent_gap, self.underline_rect.centery),
                        (self.underline_rect.left - accent_gap - accent_length, self.underline_rect.centery),
                        3)

            # Right accent
            pg.draw.line(self.screen, underline_color,
                        (self.underline_rect.right + accent_gap, self.underline_rect.centery),
                        (self.underline_rect.right + accent_gap + accent_length, self.underline_rect.centery),
                        3)

            # Draw main menu buttons
            for button in self.main_buttons:
                button.draw(self.screen)

            # Draw version and credits
            self.screen.blit(self.version_text, self.version_rect)
            self.screen.blit(self.credits_text, self.credits_rect)

        elif self.state == 'settings':
            # Draw settings title with same style as main title
            settings_title = self.title_font.render("Settings", True, (220, 220, 255))
            settings_rect = settings_title.get_rect(center=(HALF_WIDTH, 150))
            self.screen.blit(settings_title, settings_rect)

            # Draw decorative underline for settings title
            settings_underline_width = settings_rect.width * 0.8
            settings_underline_rect = pg.Rect(
                HALF_WIDTH - settings_underline_width // 2,
                settings_rect.bottom + 10,
                settings_underline_width,
                3
            )
            pg.draw.rect(self.screen, underline_color, settings_underline_rect)

            # Draw accent lines on both sides of the settings underline
            # Left accent
            pg.draw.line(self.screen, underline_color,
                        (settings_underline_rect.left - accent_gap, settings_underline_rect.centery),
                        (settings_underline_rect.left - accent_gap - accent_length, settings_underline_rect.centery),
                        3)

            # Right accent
            pg.draw.line(self.screen, underline_color,
                        (settings_underline_rect.right + accent_gap, settings_underline_rect.centery),
                        (settings_underline_rect.right + accent_gap + accent_length, settings_underline_rect.centery),
                        3)

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
