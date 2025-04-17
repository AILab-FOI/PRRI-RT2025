import pygame as pg
import time
from settings import *

class LoadingScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font_large = pg.font.SysFont('Arial', 48, bold=True)
        self.font_small = pg.font.SysFont('Arial', 24)
        self.loading_start_time = 0
        self.loading_duration = 2000  # 2 seconds minimum loading time
        self.progress = 0  # 0 to 100
        self.loading_text = "Loading..."
        self.tip_text = "Tip: Defeat all enemies to unlock the exit door!"
        self.tips = [
            "Tip: Defeat all enemies to unlock the exit door!",
            "Tip: Use dash to quickly escape dangerous situations.",
            "Tip: Look for terminals to find door codes.",
            "Tip: Press E to interact with objects and NPCs.",
            "Tip: Some NPCs are friendly and will provide useful information."
        ]
        self.current_tip = 0

        # Use a direct image as background from settings
        try:
            self.background = self.game.texture_manager.get_texture(LOADING_BACKGROUND_IMAGE, RES)
        except Exception as e:
            print(f"Error loading background image: {e}")
            self.background = None

    def start_loading(self, loading_text="Loading...", level=None):
        """Start the loading screen with optional custom text"""
        self.loading_start_time = pg.time.get_ticks()
        self.progress = 0  # Always reset progress to 0
        self.loading_text = loading_text

        # Select a random tip based on the current time
        self.current_tip = (pg.time.get_ticks() // 1000) % len(self.tips)
        self.tip_text = self.tips[self.current_tip]

        # If loading a specific level, customize the text
        if level:
            self.loading_text = f"Loading Level {level}..."

    def update(self, progress=None):
        """Update the loading progress (0-100)"""
        if progress is not None:
            self.progress = progress
        else:
            # Calculate progress based on time elapsed
            elapsed = pg.time.get_ticks() - self.loading_start_time
            self.progress = min(100, (elapsed / self.loading_duration) * 100)

    def draw(self):
        """Draw the loading screen"""
        # Draw background (black or image)
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill((0, 0, 0))

        # Draw loading text
        loading_surface = self.font_large.render(self.loading_text, True, (255, 255, 255))
        loading_rect = loading_surface.get_rect(center=(HALF_WIDTH, HALF_HEIGHT - 50))
        self.screen.blit(loading_surface, loading_rect)

        # Draw progress bar
        bar_width = WIDTH // 2
        bar_height = 20
        bar_x = (WIDTH - bar_width) // 2
        bar_y = HALF_HEIGHT

        # Draw background bar
        pg.draw.rect(self.screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))

        # Draw progress
        progress_width = int(bar_width * (self.progress / 100))
        pg.draw.rect(self.screen, (0, 200, 0), (bar_x, bar_y, progress_width, bar_height))

        # Draw border
        pg.draw.rect(self.screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)

        # Draw tip text
        tip_surface = self.font_small.render(self.tip_text, True, (200, 200, 200))
        tip_rect = tip_surface.get_rect(center=(HALF_WIDTH, HALF_HEIGHT + 50))
        self.screen.blit(tip_surface, tip_rect)

        # Update display
        pg.display.flip()

    def is_done(self):
        """Check if loading is complete (progress at 100%)"""
        return self.progress >= 100

    def wait_for_minimum_time(self):
        """Wait until the minimum loading time has passed"""
        elapsed = pg.time.get_ticks() - self.loading_start_time
        if elapsed < self.loading_duration:
            remaining = self.loading_duration - elapsed
            time.sleep(remaining / 1000)  # Convert to seconds
