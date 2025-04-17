import pygame as pg
import time
import random
import math
import os
from settings import *

class LoadingScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font_large = pg.font.SysFont('Arial', 48, bold=True)
        self.font_small = pg.font.SysFont('Arial', 24)
        self.font_details = pg.font.SysFont('Arial', 18)

        # Loading state
        self.loading_start_time = 0
        self.progress = 0  # 0 to 100
        self.loading_text = "Loading..."
        self.detail_text = "Initializing..."
        self.fade_alpha = 0  # For fade transitions (0-255)
        self.fade_direction = 1  # 1 for fade in, -1 for fade out
        self.fade_complete = False

        # Tips carousel
        self.tips = [
            "Tip: Defeat all enemies to unlock the exit door!",
            "Tip: Use dash to quickly escape dangerous situations.",
            "Tip: Look for terminals to find door codes.",
            "Tip: Press E to interact with objects and NPCs.",
            "Tip: Some NPCs are friendly and will provide useful information."
        ]
        self.current_tip = 0
        self.tip_text = self.tips[self.current_tip]
        self.last_tip_change = 0

        # Animated loading indicator
        self.pulse_value = 0
        self.pulse_direction = 1
        self.spinner_angle = 0

        # Background particles
        self.particles = []
        self.init_particles()

        # Load background image
        try:
            # Make sure the background image exists
            if os.path.exists(LOADING_BACKGROUND_IMAGE):
                # Special handling for sky.png - it's designed for half-height
                if 'sky.png' in LOADING_BACKGROUND_IMAGE:
                    # Load the sky image at its original size
                    sky_img = self.game.texture_manager.get_texture(LOADING_BACKGROUND_IMAGE, (WIDTH, HALF_HEIGHT))
                    # Create a full-screen surface
                    self.background = pg.Surface(RES)
                    # Draw sky at top
                    self.background.blit(sky_img, (0, 0))
                    # Draw a gradient for the bottom half
                    for y in range(HALF_HEIGHT, HEIGHT):
                        # Calculate gradient color (darker as it goes down)
                        darkness = (y - HALF_HEIGHT) / HALF_HEIGHT  # 0.0 to 1.0
                        # Get color from the bottom row of the sky image
                        bottom_color = sky_img.get_at((WIDTH // 2, HALF_HEIGHT - 1))
                        # Darken the color
                        r = max(0, bottom_color[0] - int(bottom_color[0] * darkness * 0.8))
                        g = max(0, bottom_color[1] - int(bottom_color[1] * darkness * 0.8))
                        b = max(0, bottom_color[2] - int(bottom_color[2] * darkness * 0.8))
                        # Draw a line with this color
                        pg.draw.line(self.background, (r, g, b), (0, y), (WIDTH, y))
                    print(f"Successfully loaded sky image with custom bottom half")
                else:
                    # Normal loading for other images
                    self.background = self.game.texture_manager.get_texture(LOADING_BACKGROUND_IMAGE, RES)
                    print(f"Successfully loaded background image from {LOADING_BACKGROUND_IMAGE}")
            else:
                print(f"Background image not found at {LOADING_BACKGROUND_IMAGE}")
                # Create a simple gradient background instead of using missing texture
                self.background = self.create_gradient_background()
        except Exception as e:
            print(f"Error loading background image: {e}")
            # Create a simple gradient background
            self.background = self.create_gradient_background()

        # Create fade overlay surface
        self.fade_surface = pg.Surface(RES, pg.SRCALPHA)

    def init_particles(self):
        """Initialize background particles"""
        self.particles = []
        for _ in range(LOADING_PARTICLE_COUNT):
            # Use colors that match the sky (whites, light blues, yellows)
            color_type = random.randint(0, 2)
            if color_type == 0:  # White/silver stars
                brightness = random.randint(180, 255)
                color = (brightness, brightness, brightness, random.randint(150, 255))
            elif color_type == 1:  # Light blue stars
                color = (random.randint(150, 200), random.randint(180, 255), random.randint(220, 255), random.randint(150, 255))
            else:  # Yellow/gold stars
                color = (random.randint(220, 255), random.randint(180, 255), random.randint(100, 150), random.randint(150, 255))

            self.particles.append({
                'x': random.randint(0, WIDTH),
                'y': random.randint(0, HEIGHT),
                'size': random.randint(1, 4),  # Slightly smaller particles
                'speed': random.uniform(0.3, 1.5),  # Slightly slower movement
                'color': color
            })

    def start_loading(self, loading_text="Loading...", level=None):
        """Start the loading screen with optional custom text"""
        self.loading_start_time = pg.time.get_ticks()
        self.progress = 0  # Always reset progress to 0
        self.loading_text = loading_text
        self.detail_text = "Initializing..."
        self.fade_alpha = 255  # Start fully faded in
        self.fade_direction = -1  # Start fading out
        self.fade_complete = False

        # Reset tip carousel
        self.current_tip = (pg.time.get_ticks() // 1000) % len(self.tips)
        self.tip_text = self.tips[self.current_tip]
        self.last_tip_change = pg.time.get_ticks()

        # If loading a specific level, customize the text
        if level:
            self.loading_text = f"Loading Level {level}..."

    def update(self, progress=None, detail_text=None):
        """Update the loading progress (0-100) and detail text"""
        current_time = pg.time.get_ticks()

        # Update progress
        if progress is not None:
            self.progress = progress
            # Update detail text if provided
            if detail_text:
                self.detail_text = detail_text
        else:
            # Calculate progress based on time elapsed
            elapsed = current_time - self.loading_start_time
            self.progress = min(100, (elapsed / LOADING_DURATION) * 100)

        # Update fade transition
        if self.fade_direction != 0:
            self.fade_alpha += self.fade_direction * (255 * current_time / LOADING_FADE_DURATION)
            if self.fade_alpha <= 0:
                self.fade_alpha = 0
                self.fade_direction = 0  # Stop fading
                self.fade_complete = True
            elif self.fade_alpha >= 255:
                self.fade_alpha = 255
                self.fade_direction = 0  # Stop fading
                self.fade_complete = True

        # Update tip carousel
        if current_time - self.last_tip_change > LOADING_TIP_CHANGE_INTERVAL:
            self.current_tip = (self.current_tip + 1) % len(self.tips)
            self.tip_text = self.tips[self.current_tip]
            self.last_tip_change = current_time

        # Update animated loading indicator
        self.pulse_value += 0.05 * self.pulse_direction
        if self.pulse_value >= 1.0:
            self.pulse_value = 1.0
            self.pulse_direction = -1
        elif self.pulse_value <= 0.0:
            self.pulse_value = 0.0
            self.pulse_direction = 1

        self.spinner_angle = (self.spinner_angle + 3) % 360

        # Update particles
        for particle in self.particles:
            particle['y'] -= particle['speed']
            if particle['y'] < -particle['size']:
                particle['y'] = HEIGHT + particle['size']
                particle['x'] = random.randint(0, WIDTH)

    def draw(self):
        """Draw the loading screen with all enhancements"""
        # Draw background (black or image)
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill((0, 0, 0))

        # Draw background particles
        for particle in self.particles:
            pg.draw.circle(
                self.screen,
                particle['color'],
                (int(particle['x']), int(particle['y'])),
                particle['size']
            )

        # Draw loading text - moved higher up
        loading_surface = self.font_large.render(self.loading_text, True, (255, 255, 255))
        loading_rect = loading_surface.get_rect(center=(HALF_WIDTH, HALF_HEIGHT - 120))
        self.screen.blit(loading_surface, loading_rect)

        # Draw detail text - increased spacing
        detail_surface = self.font_details.render(self.detail_text, True, (200, 200, 200))
        detail_rect = detail_surface.get_rect(center=(HALF_WIDTH, HALF_HEIGHT - 80))
        self.screen.blit(detail_surface, detail_rect)

        # Draw animated loading indicator
        self.draw_animated_indicator()

        # Draw tip text with a subtle animation
        tip_alpha = int(155 + 100 * math.sin(pg.time.get_ticks() * 0.002))
        # Fix: Use proper color format without alpha in render (pygame doesn't support alpha in text render)
        tip_surface = self.font_small.render(self.tip_text, True, (200, 200, 200))
        # Create a surface with per-surface alpha
        tip_alpha_surface = pg.Surface(tip_surface.get_size(), pg.SRCALPHA)
        tip_alpha_surface.fill((255, 255, 255, tip_alpha))
        # Blit with blend mode
        tip_alpha_surface.blit(tip_surface, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
        # Position further down to avoid overlap
        tip_rect = tip_alpha_surface.get_rect(center=(HALF_WIDTH, HALF_HEIGHT + 120))
        self.screen.blit(tip_alpha_surface, tip_rect)

        # Draw fade overlay
        if self.fade_alpha > 0:
            self.fade_surface.fill((0, 0, 0, int(self.fade_alpha)))
            self.screen.blit(self.fade_surface, (0, 0))

        # Update display
        pg.display.flip()

    def draw_animated_indicator(self):
        """Draw an animated loading indicator"""
        # Base parameters - moved down to avoid overlap
        center_x, center_y = HALF_WIDTH, HALF_HEIGHT
        bar_width = WIDTH // 3
        bar_height = 10
        bar_x = center_x - bar_width // 2
        bar_y = center_y + 50  # Moved down from +20 to +50

        # Draw background bar
        pg.draw.rect(self.screen, (30, 30, 30), (bar_x, bar_y, bar_width, bar_height))

        # Draw progress with pulsing effect
        progress_width = int(bar_width * (self.progress / 100))
        pulse_color = self.pulse_color()
        pg.draw.rect(self.screen, pulse_color, (bar_x, bar_y, progress_width, bar_height))

        # Draw spinner
        spinner_x = bar_x + progress_width
        spinner_y = bar_y + bar_height // 2

        # Ensure spinner stays within the bar
        spinner_x = max(bar_x, min(spinner_x, bar_x + bar_width))

        # Draw spinner circle
        pg.draw.circle(self.screen, (200, 200, 200), (spinner_x, spinner_y), 8)

        # Draw spinner lines
        for i in range(8):
            angle = math.radians(self.spinner_angle + i * 45)
            line_length = 5 + 3 * (i % 4)
            end_x = spinner_x + line_length * math.cos(angle)
            end_y = spinner_y + line_length * math.sin(angle)
            line_alpha = 255 - (i * 30)
            line_color = (255, 255, 255, max(0, line_alpha))
            pg.draw.line(self.screen, line_color, (spinner_x, spinner_y), (end_x, end_y), 2)

        # Draw border
        pg.draw.rect(self.screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height), 1)

    def pulse_color(self):
        """Generate a pulsing color for the progress bar"""
        base_r, base_g, base_b = 0, 180, 0  # Base green color
        pulse_r = int(base_r + 50 * self.pulse_value)
        pulse_g = int(base_g + 75 * self.pulse_value)
        pulse_b = int(base_b + 100 * self.pulse_value)
        return (pulse_r, pulse_g, pulse_b)

    def is_done(self):
        """Check if loading is complete (progress at 100%)"""
        return self.progress >= 100

    def wait_for_minimum_time(self):
        """Wait until the minimum loading time has passed"""
        elapsed = pg.time.get_ticks() - self.loading_start_time
        if elapsed < LOADING_DURATION:
            remaining = LOADING_DURATION - elapsed
            time.sleep(remaining / 1000)  # Convert to seconds

    def fade_in(self):
        """Start fade in transition"""
        self.fade_alpha = 255
        self.fade_direction = -1
        self.fade_complete = False

    def fade_out(self):
        """Start fade out transition"""
        self.fade_alpha = 0
        self.fade_direction = 1
        self.fade_complete = False

    def create_gradient_background(self):
        """Create a simple gradient background as a fallback"""
        # Create a surface for the background
        surface = pg.Surface(RES)

        # Define gradient colors (dark blue to black)
        color1 = (10, 20, 40)  # Dark blue at top
        color2 = (0, 0, 20)    # Almost black at bottom

        # Draw the gradient
        for y in range(HEIGHT):
            # Calculate the color for this line
            r = int(color1[0] + (color2[0] - color1[0]) * y / HEIGHT)
            g = int(color1[1] + (color2[1] - color1[1]) * y / HEIGHT)
            b = int(color1[2] + (color2[2] - color1[2]) * y / HEIGHT)

            # Draw a line with this color
            pg.draw.line(surface, (r, g, b), (0, y), (WIDTH, y))

        # Add some subtle stars
        for _ in range(100):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            size = random.randint(1, 3)
            brightness = random.randint(100, 255)
            pg.draw.circle(surface, (brightness, brightness, brightness), (x, y), size)

        return surface
