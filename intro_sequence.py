import pygame as pg
import time
from settings import *
import math

class IntroSequence:

    def __init__(self, game):
        self.game = game
        self.active = False
        self.start_time = 0
        self.black_screen_duration = 9.5
        self.blur_duration = 6.0
        self.total_duration = self.black_screen_duration + self.blur_duration

        # Sound timing parameters
        self.high_pitch_delay = self.black_screen_duration
        self.music_delay = self.total_duration + 1.0

        # Music fade-in parameters
        self.music_fade_duration = 8.0
        self.original_music_volume = 0.3

        # Load sounds
        try:
            self.crash_sound = pg.mixer.Sound('resources/sound/crash.wav')
            self.high_pitch_sound = pg.mixer.Sound('resources/sound/high_pitch.wav')
            self.sounds_loaded = True
        except:
            self.sounds_loaded = False

        # Create surfaces for effects
        self.screen = game.screen
        self.screen_width, self.screen_height = self.screen.get_size()
        self.black_overlay = pg.Surface((self.screen_width, self.screen_height))
        self.black_overlay.fill((0, 0, 0))

        # Blur effect parameters
        self.blur_surface = pg.Surface((self.screen_width, self.screen_height), pg.SRCALPHA)

        # Pulsing effect parameters
        self.pulse_frequency = 0.8  # Pulses per second
        self.pulse_amplitude = 1.0  # Maximum pulse intensity

    def start(self):
        """Start the intro sequence"""
        self.active = True
        self.start_time = time.time()

        # Initialize sound flags
        self.crash_sound_started = False
        self.high_pitch_sound_started = False
        self.music_started = False

        # Store the original music volume and stop the music
        self.original_music_volume = pg.mixer.music.get_volume()
        pg.mixer.music.stop()

    def update(self):
        """Update the intro sequence"""
        if not self.active:
            return

        # Check for spacebar press to skip intro sequence
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            self._end_sequence()
            return

        # Calculate elapsed time
        elapsed = time.time() - self.start_time

        # PHASE 1: Start crash sound immediately
        if not self.crash_sound_started and self.sounds_loaded:
            self.crash_sound_started = True
            self.crash_sound.set_volume(1.0)
            self.crash_sound.play()

        # Fade out crash sound as we approach the transition to blur phase
        transition_point = self.black_screen_duration - 0.5
        if self.crash_sound_started and elapsed >= transition_point and elapsed < self.black_screen_duration:
            progress = (elapsed - transition_point) / (self.black_screen_duration - transition_point)
            volume = 1.0 - (progress * 0.8)
            self.crash_sound.set_volume(max(0.2, volume))

        transition_point = self.black_screen_duration - 0.5

        if not self.high_pitch_sound_started and elapsed >= transition_point and self.sounds_loaded:
            self.high_pitch_sound_started = True
            self.high_pitch_sound.set_volume(0.1)
            self.high_pitch_sound.play()

        # Gradually increase high pitch volume as we transition to blur phase
        if self.high_pitch_sound_started and elapsed < self.black_screen_duration + 1.0:
            # Calculate transition progress (0.0 to 1.0)
            if elapsed < self.black_screen_duration:
                # Ramping up during black screen
                progress = (elapsed - transition_point) / (self.black_screen_duration - transition_point)
                volume = 0.1 + (progress * 0.4)
            else:
                # Continue ramping up during first second of blur
                progress = (elapsed - self.black_screen_duration) / 1.0
                volume = 0.5 + (progress * 0.5)

            self.high_pitch_sound.set_volume(min(1.0, volume))

        # Start fading out high pitch sound near the end of the sequence
        high_pitch_fade_start = self.total_duration - 1.5

        if self.high_pitch_sound_started and elapsed >= high_pitch_fade_start and elapsed < self.total_duration:
            # Calculate fade-out progress (0.0 to 1.0)
            fade_progress = (elapsed - high_pitch_fade_start) / 1.5
            volume = 1.0 - fade_progress
            self.high_pitch_sound.set_volume(max(0.0, volume))

        # Check if sequence is complete
        if elapsed >= self.total_duration:
            self._end_sequence()
            return

    def _end_sequence(self):
        self.active = False

        # Stop sounds if they're still playing
        if self.sounds_loaded:
            self.crash_sound.stop()
            self.high_pitch_sound.stop()

        # Start music immediately after sequence ends
        if not self.music_started:
            self.music_started = True
            # Start the music with fade-in directly
            self.start_music_with_fade()

        # Reset mouse position and clear accumulated movement to prevent jerking
        pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        pg.mouse.get_rel()

        # Start disorienting effects ONLY if on level 1
        if self.game.level_manager.current_level == 1:
            self.game.disorienting_effects.start()

    def draw(self):
        """Draw the intro sequence effects"""
        if not self.active:
            return

        # Calculate elapsed time
        elapsed = time.time() - self.start_time

        if elapsed < self.black_screen_duration:
            self.screen.blit(self.black_overlay, (0, 0))
            return

        blur_elapsed = elapsed - self.black_screen_duration
        blur_progress = min(blur_elapsed / self.blur_duration, 1.0)

        # Get the current game screen as a starting point
        current_screen = self.screen.copy()

        # Apply blur effect that decreases over time
        blur_intensity = max(0, 1.0 - blur_progress)
        self._apply_blur(current_screen, blur_intensity)

        # Apply pulsing effect
        pulse_intensity = self._calculate_pulse(blur_elapsed, blur_progress)
        self._apply_pulse(pulse_intensity)

    def _apply_blur(self, surface, intensity):
        """Apply a blur effect to the screen"""
        if intensity <= 0:
            return

        # Simple blur implementation
        blur_size = int(intensity * 10)
        if blur_size <= 0:
            return

        # Create a smaller surface (this creates the blur effect)
        scale_factor = max(0.1, 1.0 - (intensity * 0.5))
        small_surface = pg.transform.scale(
            surface,
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

    def _calculate_pulse(self, elapsed, progress):
        # Maintain strong pulse throughout the blur phase, only slightly decreasing
        max_pulse = self.pulse_amplitude * (1.0 - (progress * 0.3))

        # Calculate sine wave for pulsing
        pulse = math.sin(elapsed * self.pulse_frequency * 2 * math.pi) * max_pulse

        # Ensure pulse is positive
        return max(0, pulse + (max_pulse * 0.5))

    def _apply_pulse(self, intensity):
        """Apply a pulsing darkness effect"""
        if intensity <= 0:
            return

        # Create a black overlay with the pulse intensity as alpha
        pulse_overlay = pg.Surface((self.screen_width, self.screen_height), pg.SRCALPHA)
        pulse_overlay.fill((0, 0, 0, int(intensity * 150)))
        self.screen.blit(pulse_overlay, (0, 0))

    def start_music_with_fade(self):
        """Start the background music with fade-in effect"""
        pg.mixer.music.set_volume(0.0)
        pg.mixer.music.play(-1)

        # Create a timer for the fade-in effect
        self.fade_start_time = time.time()
        self.fading_music = True

    def update_music_fade(self):
        """Update the music fade-in effect"""
        if not hasattr(self, 'fading_music') or not self.fading_music:
            return

        # Calculate elapsed time since fade started
        elapsed = time.time() - self.fade_start_time

        fade_progress = min(1.0, elapsed / self.music_fade_duration)

        if fade_progress < 0.5:
            curve_progress = fade_progress * fade_progress * 2
        else:
            quadratic = fade_progress * fade_progress * 2
            linear = fade_progress
            blend_factor = (fade_progress - 0.5) * 2
            curve_progress = quadratic * (1 - blend_factor) + linear * blend_factor

        current_volume = curve_progress * self.original_music_volume
        pg.mixer.music.set_volume(current_volume)

        if fade_progress >= 1.0:
            self.fading_music = False
