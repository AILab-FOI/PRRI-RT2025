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

    def draw(self):
        self.draw_background()
        self.render_game_objects()
        self.draw_player_health()
        self.draw_dash_indicator()
        self.draw_enemy_counter()

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

    def draw_enemy_counter(self):
        """Draw a counter showing remaining enemies"""
        # Get the number of remaining enemies
        enemy_count = len(self.game.object_handler.npc_positions)

        # Position in bottom right corner
        counter_x = WIDTH - 120
        counter_y = HEIGHT - 60

        # Draw background panel
        panel_rect = pg.Rect(counter_x - 10, counter_y - 10, 110, 50)
        pg.draw.rect(self.screen, (40, 45, 80), panel_rect, border_radius=8)
        pg.draw.rect(self.screen, (100, 140, 240), panel_rect, 2, border_radius=8)

        # Draw enemy icon (placeholder - a red square)
        icon_rect = pg.Rect(counter_x, counter_y, 30, 30)
        pg.draw.rect(self.screen, (200, 60, 60), icon_rect, border_radius=5)
        pg.draw.rect(self.screen, (255, 100, 100), icon_rect, 1, border_radius=5)

        # Draw enemy count text
        font = pg.font.Font(None, 36)
        text = font.render(f"x {enemy_count}", True, (220, 220, 255))
        text_rect = text.get_rect(midleft=(counter_x + 40, counter_y + 15))
        self.screen.blit(text, text_rect)

    def draw_background(self):
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIDTH
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))
        # floor
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def render_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
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