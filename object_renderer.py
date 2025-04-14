import pygame as pg
from settings import *


class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.sky_image = self.get_texture('resources/textures/sky.png', (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0
        self.blood_screen = self.get_texture('resources/textures/blood_screen.png', RES)
        self.digit_size = 90
        self.digit_images = [self.get_texture(f'resources/teksture/brojevi/{i}.png', [self.digit_size] * 2)
                             for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.digit_images))
        self.game_over_image = self.get_texture('resources/textures/game_over.png', RES)
        self.win_image = self.get_texture('resources/textures/win.png', RES)

        # Message display
        self.message = ""
        self.message_time = 0
        self.message_duration = 5000  # 5 seconds
        self.message_font = pg.font.SysFont('Arial', 36)

    def draw(self):
        self.draw_background()
        self.render_game_objects()
        self.draw_player_health()
        self.draw_dash_indicator()
        self.draw_enemy_counter()
        self.draw_message()

    def draw_enemy_counter(self):
        """Draw a counter showing the number of remaining enemies"""
        # Get the number of remaining enemies
        remaining_enemies = len(self.game.object_handler.npc_positions)
        total_enemies = self.game.object_handler.enemies

        # Create the counter text
        counter_text = f"Enemies: {remaining_enemies}/{total_enemies}"

        # Render the text
        font = pg.font.SysFont('Arial', 24)
        text_surface = font.render(counter_text, True, (255, 255, 255))

        # Position in bottom right corner
        text_rect = text_surface.get_rect(bottomright=(WIDTH - 20, HEIGHT - 20))

        # Draw a semi-transparent background
        bg_rect = text_rect.inflate(20, 10)  # Make background slightly larger
        bg_surface = pg.Surface((bg_rect.width, bg_rect.height), pg.SRCALPHA)
        bg_surface.fill((0, 0, 0, 150))  # Semi-transparent black
        self.screen.blit(bg_surface, bg_rect)

        # Draw the text
        self.screen.blit(text_surface, text_rect)

    def win(self):
        self.screen.blit(self.win_image, (0, 0))

    def game_over(self):
        self.screen.blit(self.game_over_image, (0, 0))

    def draw_player_health(self):
        health = str(self.game.player.health)
        for i, char in enumerate(health):
            self.screen.blit(self.digits[char], (i * self.digit_size, 0))
        self.screen.blit(self.digits['10'], ((i + 1) * self.digit_size, 0))

    def player_damage(self):
        self.screen.blit(self.blood_screen, (0, 0))

    def show_message(self, text):
        """Display a message on screen for a limited time"""
        self.message = text
        self.message_time = pg.time.get_ticks()

    def draw_message(self):
        """Draw the current message if it's active"""
        if self.message and pg.time.get_ticks() - self.message_time < self.message_duration:
            # Create a semi-transparent background
            bg_surface = pg.Surface((WIDTH, 80), pg.SRCALPHA)
            bg_surface.fill((0, 0, 0, 180))
            self.screen.blit(bg_surface, (0, self.digit_size + 10))  # Position below the health display

            # Render the message text
            text_surface = self.message_font.render(self.message, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(HALF_WIDTH, self.digit_size + 50))  # Center text in the background
            self.screen.blit(text_surface, text_rect)

    def draw_dash_indicator(self):
        # Izračunaj preostalo vrijeme cooldowna
        current_time = pg.time.get_ticks()
        dash_cooldown_remaining = 0

        if not self.game.player.is_dashing:
            time_since_last_dash = current_time - self.game.player.last_dash_time
            if time_since_last_dash < PLAYER_DASH_COOLDOWN:
                dash_cooldown_remaining = 1 - (time_since_last_dash / PLAYER_DASH_COOLDOWN)

        # Nacrtaj indikator cooldowna
        indicator_width = 200
        indicator_height = 10
        indicator_x = WIDTH - indicator_width - 20
        indicator_y = 20

        # Pozadina indikatora
        pg.draw.rect(self.screen, (50, 50, 50),
                     (indicator_x, indicator_y, indicator_width, indicator_height))

        # Popunjeni dio indikatora
        if dash_cooldown_remaining > 0:
            fill_width = int(indicator_width * (1 - dash_cooldown_remaining))
            pg.draw.rect(self.screen, (0, 200, 0),
                         (indicator_x, indicator_y, fill_width, indicator_height))
        else:
            # Dash je spreman - prikaži puni indikator
            pg.draw.rect(self.screen, (0, 255, 0),
                         (indicator_x, indicator_y, indicator_width, indicator_height))

    def draw_background(self):
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIDTH
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))
        # floor
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def render_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for _, image, pos in list_objects:  # Use _ to indicate unused variable
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_wall_textures(self):
        return {

            1: self.get_texture('resources/teksture/1.jpg'),
            2: self.get_texture('resources/teksture/2.jpg'),
            3: self.get_texture('resources/teksture/3.jpg'),
            4: self.get_texture('resources/teksture/4.jpg'),
            5: self.get_texture('resources/teksture/5.jpg'),
            6: self.get_texture('resources/teksture/6.jpg'),
            7: self.get_texture('resources/teksture/11.png'),
            8: self.get_texture('resources/teksture/8.png'),
            9: self.get_texture('resources/teksture/9.png'),
            10: self.get_texture('resources/teksture/10.png'),

            11: self.get_texture('resources/teksture/vrata1.png'),
            12: self.get_texture('resources/teksture/ukras4.png'),

            14: self.get_texture('resources/teksture/ukras1.png'),
            15: self.get_texture('resources/teksture/prozor.jpg'),
        }