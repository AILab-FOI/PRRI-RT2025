import pygame as pg
import time
import math
import json
import random
from settings import *
from font_manager import load_custom_font

class LoadingScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.active = False
        self.start_time = 0
        self.duration = 3.0
        self.progress = 0.0
        self.completed = False
        self.next_level_num = None
        self.loading_successful = True

        self.tips = []
        self.lore = []
        self.current_tip = ""
        self.load_tips_and_lore()

        # Load background image
        self.bg_image = pg.image.load('resources/tekstures/loading_bg.png')
        self.bg_image = pg.transform.scale(self.bg_image, RES)

        # Load fonts
        self.title_font = load_custom_font(60)  # Larger font for title
        self.info_font = load_custom_font(30)   # Larger font for info
        self.tip_font = load_custom_font(20)    # Smaller font for tips

        # Loading circle settings
        self.circle_radius = 40
        self.circle_width = 4
        self.circle_y = HALF_HEIGHT + 100
        self.num_segments = 8  # Fewer segments for smoother animation

        # Colors
        self.text_color = (220, 220, 255)  # Light blue text
        self.circle_color = (120, 180, 255)  # Brighter blue for the circle
        self.circle_bg_color = (40, 40, 60, 80)  # More subtle background
        self.tip_bg_color = (30, 30, 50, 180)  # More opaque background for tips

    def load_tips_and_lore(self):
        """Load tips and lore from JSON file"""
        try:
            with open('resources/loading_tips.json', 'r') as f:
                data = json.load(f)
                self.tips = data.get('tips', [])
                self.lore = data.get('lore', [])
        except Exception as e:
            print(f"Error loading tips and lore: {e}")
            # Fallback tips if file can't be loaded
            self.tips = ["Press E to interact with objects."]
            self.lore = ["The ship was attacked by Vogons."]

    def start(self, level_number=None):
        """Start the loading screen"""
        self.active = True
        self.completed = False
        self.start_time = time.time()
        self.progress = 0.0
        self.level_number = level_number
        self.next_level_num = level_number
        self.loading_successful = True

        # Select a random tip or lore
        if random.random() < 0.5 and self.tips:  # 50% chance for a tip
            self.current_tip = random.choice(self.tips)
        elif self.lore:  # Otherwise use lore
            self.current_tip = random.choice(self.lore)

    def update(self):
        """Update the loading screen progress"""
        if not self.active:
            return

        # Calculate progress based on elapsed time
        elapsed = time.time() - self.start_time
        self.progress = min(elapsed / self.duration, 1.0)

        # Check if loading is complete
        if self.progress >= 1.0:
            self.completed = True
            self.active = False

    def set_custom_message(self, message, position=None, color=None):
        """Display a custom message on the loading screen"""
        if not color:
            color = self.text_color

        if not position:
            position = (HALF_WIDTH, HALF_HEIGHT + 300)

        message_text = self.info_font.render(message, True, color)
        message_rect = message_text.get_rect(center=position)
        self.game.screen.blit(message_text, message_rect)

    def draw(self):
        """Draw the loading screen"""
        if not self.active:
            return

        # Draw background
        self.screen.blit(self.bg_image, (0, 0))

        # Draw loading text with smoother pulsating effect
        # Use sine wave for smoother pulsation
        alpha = int(180 + 75 * math.sin(time.time() * 1.5))  # Smoother pulsation between 180 and 255
        loading_text = self.title_font.render("LOADING", True, self.text_color)
        loading_text.set_alpha(alpha)
        loading_text_rect = loading_text.get_rect(center=(HALF_WIDTH, HALF_HEIGHT - 60))
        self.screen.blit(loading_text, loading_text_rect)

        # Draw level info if available
        if self.level_number is not None:
            level_text = self.info_font.render(f"LEVEL {self.level_number}", True, self.text_color)
            level_rect = level_text.get_rect(center=(HALF_WIDTH, HALF_HEIGHT))
            self.screen.blit(level_text, level_rect)

        # Draw tip/lore text
        if self.current_tip:
            # Create a semi-transparent background for the tip
            tip_bg_surface = pg.Surface((WIDTH - 200, 70), pg.SRCALPHA)
            tip_bg_surface.fill(self.tip_bg_color)

            # Position the tip further down
            tip_y_position = HALF_HEIGHT + 200
            tip_bg_rect = tip_bg_surface.get_rect(center=(HALF_WIDTH, tip_y_position))

            # Add a subtle border to the tip box
            border_rect = tip_bg_rect.copy()
            border_rect.inflate_ip(4, 4)
            pg.draw.rect(self.screen, (80, 100, 180, 100), border_rect, border_radius=10)

            # Draw the background with rounded corners
            self.screen.blit(tip_bg_surface, tip_bg_rect)

            # Render and draw the tip text
            tip_text = self.tip_font.render(self.current_tip, True, self.text_color)
            tip_rect = tip_text.get_rect(center=(HALF_WIDTH, tip_y_position))
            self.screen.blit(tip_text, tip_rect)

        # Draw loading circle
        circle_center = (HALF_WIDTH, self.circle_y)

        # Draw background circle (full circle with semi-transparent color)
        pg.draw.circle(self.screen, self.circle_bg_color, circle_center,
                      self.circle_radius, self.circle_width)

        # Calculate rotation based on time only (constant speed)
        rotation_speed = 0.3  # Fixed rotation speed
        base_angle = time.time() * rotation_speed * 360  # Convert to degrees

        # Draw the rotating segments
        for i in range(self.num_segments):
            # Calculate the angle for this segment
            angle = base_angle - (i * (360 / self.num_segments))  # Negative for clockwise rotation

            # Calculate the opacity based on position in the rotation with smoother falloff
            # The leading segment is fully opaque, trailing segments fade out more gradually
            opacity = 255 - int(180 * (i / self.num_segments) ** 1.5)  # Exponential falloff for smoother transition

            # Create a color with the calculated opacity
            segment_color = (*self.circle_color[:3], opacity)

            # Convert angle to radians for sin/cos
            start_angle = math.radians(angle)
            end_angle = math.radians(angle + (360 / self.num_segments) * 0.8)  # Larger segments with smaller gaps

            # Draw the arc segment
            pg.draw.arc(self.screen, segment_color,
                       (circle_center[0] - self.circle_radius,
                        circle_center[1] - self.circle_radius,
                        self.circle_radius * 2,
                        self.circle_radius * 2),
                       start_angle, end_angle, self.circle_width)
