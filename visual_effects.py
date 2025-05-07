import pygame as pg
import math
import random
import time
from settings import *

class DisorientingEffects:
    def __init__(self, game):
        self.game = game
        self.active = False
        self.start_time = 0
        self.duration = 60.0  # Extended to 60 seconds
        
        # Distortion effect parameters
        self.distortion_intensity = 0
        self.max_distortion = 0.55  # Increased from 0.45
        self.distortion_speed = 0.001
        self.distortion_direction = 1
        
        # Tilt effect parameters
        self.tilt_angle = 0
        self.max_tilt = 0.15  # Increased from 0.12
        self.tilt_speed = 0.0006
        self.tilt_direction = 1
        
        # Flash effect parameters
        self.flash_intensity = 0
        self.flash_timer = 0
        self.flash_interval = 3.5  # Decreased from 4.0 for more frequent flashes
        self.flash_duration = 2.5  # Increased from 2.0
        
        # Create surfaces for effects
        self.screen = game.screen
        self.screen_width, self.screen_height = self.screen.get_size()
        self.effect_surface = pg.Surface((self.screen_width, self.screen_height), pg.SRCALPHA)
        
        # Pulse parameters
        self.pulse_frequency = 0.9
        self.pulse_amplitude = 0.5  # Increased from 0.4
        self.pulse_offset = 0
        
        # Blur effect parameters
        self.blur_intensity = 0
        self.max_blur = 1.0  # Increased from 0.8
        self.blur_speed = 0.002
        self.blur_direction = 1
        self.blur_surface = pg.Surface((self.screen_width, self.screen_height))
        
        # Double vision effect parameters
        self.double_vision_offset = 0
        self.max_double_vision = 50  # Increased from 40
        self.double_vision_speed = 0.3

    def start(self):
        """Start the disorienting effects"""
        # Only start effects if on level 1
        if self.game.level_manager.current_level != 1:
            return
        
        self.active = True
        self.start_time = time.time()
        print("Starting disorienting effects")
        
    def update(self):
        """Update the disorienting effects"""
        if not self.active:
            return
        
        # Check if effects duration has ended
        elapsed = time.time() - self.start_time
        if elapsed >= self.duration:
            self.end_effects()
            return
        
        # Calculate intensity based on time with FASTER decay
        # Use a mix of quadratic and cubic curves with more weight on cubic for faster decrease
        time_factor = 1.0 - (elapsed / self.duration)
        quadratic = time_factor * time_factor
        cubic = time_factor * time_factor * time_factor
        # Increased cubic component (0.7) for faster initial decrease
        base_intensity = cubic * 0.7 + quadratic * 0.3
        
        # Ensure minimum intensity of 0.1 at the end
        intensity_factor = base_intensity * 0.9 + 0.1
        
        # Print intensity factor occasionally for debugging
        if random.random() < 0.005:
            print(f"Disorienting effects intensity: {intensity_factor:.2f}")
        
        # Update distortion effect
        self._update_distortion(intensity_factor)
        
        # Update tilt effect
        self._update_tilt(intensity_factor)
        
        # Update flash effect - flash interval increases as time passes
        self._update_flash(elapsed, intensity_factor)
        
        # Update pulse effect
        self._update_pulse(elapsed, intensity_factor)
        
        # Update blur effect with balanced decay
        self._update_blur(intensity_factor)
        
        # Update double vision effect with balanced decay
        self._update_double_vision(elapsed, intensity_factor)
    
    def _update_distortion(self, intensity):
        """Update the distortion effect"""
        # Change distortion direction if limits reached
        # Use a faster decay curve
        # Mix of quadratic and linear for faster decrease
        adjusted_max = self.max_distortion * ((intensity * intensity * 0.6) + (intensity * 0.4))
        
        if self.distortion_intensity >= adjusted_max:
            self.distortion_direction = -1
        elif self.distortion_intensity <= 0:
            self.distortion_direction = 1
        
        # Update distortion - speed decreases over time with faster curve
        adjusted_speed = self.distortion_speed * 1.3 * intensity
        self.distortion_intensity += adjusted_speed * self.distortion_direction * intensity
        self.distortion_intensity = min(adjusted_max, self.distortion_intensity)
    
    def _update_tilt(self, intensity):
        """Update the tilt effect"""
        # Change tilt direction if limits reached
        # Use a faster decay curve
        # Mix of quadratic and linear for faster decrease
        adjusted_max_tilt = self.max_tilt * ((intensity * intensity * 0.6) + (intensity * 0.4))
        
        if self.tilt_angle >= adjusted_max_tilt:
            self.tilt_direction = -1
        elif self.tilt_angle <= -adjusted_max_tilt:
            self.tilt_direction = 1
        
        # Update tilt with faster decay
        adjusted_speed = self.tilt_speed * 1.3 * intensity
        self.tilt_angle += adjusted_speed * self.tilt_direction * intensity
    
    def _update_flash(self, elapsed, intensity):
        """Update the flash effect"""
        # Apply faster decay for flash frequency
        # Mix of quadratic and linear for faster decrease
        flash_intensity_factor = (intensity * intensity * 0.6) + (intensity * 0.4)
        
        # Adjust flash interval based on intensity (moderate increase in interval)
        adjusted_interval = self.flash_interval * (2.5 - intensity * 1.5)  # Faster increase in interval
        
        # Check if it's time for a flash
        if elapsed - self.flash_timer >= adjusted_interval:
            self.flash_timer = elapsed
            self.flash_intensity = flash_intensity_factor  # Flash max brightness decreases faster
        
        # Decrease flash intensity over time with a faster fade-out
        if self.flash_intensity > 0:
            time_since_flash = elapsed - self.flash_timer
            adjusted_duration = self.flash_duration * flash_intensity_factor  # Flash duration decreases faster
            
            if time_since_flash < adjusted_duration:
                # Flash is still active - use a faster fade
                progress = time_since_flash / adjusted_duration
                self.flash_intensity = flash_intensity_factor * (1.0 - (progress * 1.2))  # Faster fade-out
                self.flash_intensity = max(0, self.flash_intensity)  # Ensure non-negative
            else:
                # Flash is over
                self.flash_intensity = 0

    def _update_pulse(self, elapsed, intensity):
        """Update the pulse effect"""
        # Pulse amplitude decreases over time
        adjusted_amplitude = self.pulse_amplitude * intensity
        self.pulse_offset = math.sin(elapsed * self.pulse_frequency * 2 * math.pi) * adjusted_amplitude
        
    def draw(self):
        """Draw the disorienting effects"""
        if not self.active:
            return
        
        # Apply blur effect first (as base effect)
        if self.blur_intensity > 0.1:
            self._apply_blur()
        
        # Apply double vision effect
        if abs(self.double_vision_offset) > 1:
            self._apply_double_vision()
        
        # Apply distortion effect
        if self.distortion_intensity > 0:
            self._apply_distortion()
        
        # Apply flash effect (always on top)
        if self.flash_intensity > 0:
            self._apply_flash()
        
    def _apply_distortion(self):
        """Apply a wavy distortion effect to the screen"""
        # Create a copy of the screen
        screen_copy = self.screen.copy()
        
        # Clear the screen
        self.screen.fill((0, 0, 0))
        
        # Apply wavy distortion with increased wave height and frequency
        for y in range(0, self.screen_height, 2):
            # Further increased wave amplitude from 25 to 30
            wave_offset = int(math.sin(y * 0.09 + time.time() * 2.0) * 30 * self.distortion_intensity)
            self.screen.blit(screen_copy, (wave_offset, y), (0, y, self.screen_width, 2))
            
    def _apply_flash(self):
        """Apply a flash effect to the screen"""
        flash_surface = pg.Surface((self.screen_width, self.screen_height), pg.SRCALPHA)
        # Use a brighter white with higher alpha
        flash_surface.fill((255, 255, 255, int(180 * self.flash_intensity)))  # Increased brightness and alpha
        self.screen.blit(flash_surface, (0, 0))

    def _apply_blur(self):
        """Apply a blur effect to simulate dizziness"""
        # Create a copy of the screen
        screen_copy = self.screen.copy()
        
        # Calculate blur size based on intensity
        blur_size = int(self.blur_intensity * 10)
        if blur_size < 1:
            return
        
        # Create a smaller surface (this creates the blur effect)
        scale_factor = max(0.1, 1.0 - (self.blur_intensity * 0.5))
        small_surface = pg.transform.scale(
            screen_copy,
            (int(self.screen_width * scale_factor),
             int(self.screen_height * scale_factor))
        )
        
        # Scale back up to original size (blurry)
        blurred = pg.transform.scale(
            small_surface,
            (self.screen_width, self.screen_height)
        )
        
        # Apply the blurred surface
        self.screen.blit(blurred, (0, 0))

    def _apply_double_vision(self):
        """Apply a double vision effect to simulate dizziness"""
        # Create a copy of the screen
        screen_copy = self.screen.copy()
        
        # Apply a semi-transparent copy offset to the side
        offset_x = int(self.double_vision_offset)
        if abs(offset_x) < 1:
            return
        
        # Create a semi-transparent surface for the double vision
        ghost_surface = pg.Surface((self.screen_width, self.screen_height), pg.SRCALPHA)
        ghost_surface.blit(screen_copy, (0, 0))
        ghost_surface.set_alpha(128)  # 50% opacity
        
        # Blit the ghost image offset to create double vision
        self.screen.blit(ghost_surface, (offset_x, 0))

    def _update_blur(self, intensity):
        """Update the blur effect"""
        # Apply a faster decay curve for blur
        # This creates a faster decrease while maintaining minimum
        blur_intensity_factor = (intensity * intensity * 0.6) + (intensity * 0.4)  # Mix of quadratic and linear
        
        # Adjust max blur based on the decay curve
        adjusted_max = self.max_blur * blur_intensity_factor
        
        # Change blur direction if limits reached
        if self.blur_intensity >= adjusted_max:
            self.blur_direction = -1
        elif self.blur_intensity <= 0.15 * blur_intensity_factor:
            self.blur_direction = 1
        
        # Update blur intensity - balanced speed
        adjusted_speed = self.blur_speed * 1.3 * blur_intensity_factor
        self.blur_intensity += adjusted_speed * self.blur_direction * blur_intensity_factor
        self.blur_intensity = max(0.15 * blur_intensity_factor, min(adjusted_max, self.blur_intensity))
        
        # Print blur intensity occasionally for debugging
        if random.random() < 0.005:
            print(f"Blur intensity: {self.blur_intensity:.3f}, Max: {adjusted_max:.3f}")

    def _update_double_vision(self, elapsed, intensity):
        """Update the double vision effect"""
        # Apply a faster decay curve for double vision
        # Mix of quadratic and linear for faster decrease
        double_vision_factor = (intensity * intensity * 0.6) + (intensity * 0.4)
        
        # Maximum offset decreases at faster pace
        adjusted_max = self.max_double_vision * double_vision_factor
        
        # Calculate a sine wave for the double vision offset
        self.double_vision_offset = math.sin(elapsed * self.double_vision_speed) * adjusted_max

    def end_effects(self):
        """End the disorienting effects"""
        self.active = False
        print("Disorienting effects ended")
