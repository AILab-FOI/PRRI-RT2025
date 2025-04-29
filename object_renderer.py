import pygame as pg
from settings import *
from font_manager import load_custom_font


class ObjectRenderer:
    def draw_text_with_background(self, text, font, color, position, center=False, bg_color=(0, 0, 0, 150), padding=(20, 10)):
        """Helper method to draw text with a semi-transparent background"""
        text_surface = font.render(text, True, color)

        # Position the text
        if center:
            text_rect = text_surface.get_rect(center=position)
        else:
            text_rect = text_surface.get_rect(topleft=position)

        # Create background
        bg_rect = text_rect.inflate(padding[0], padding[1])
        bg_surface = pg.Surface((bg_rect.width, bg_rect.height), pg.SRCALPHA)
        bg_surface.fill(bg_color)

        # Draw background and text
        self.screen.blit(bg_surface, bg_rect)
        self.screen.blit(text_surface, text_rect)

        return text_rect

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

        # Preload powerup icon
        self.powerup_icon = self.get_texture('resources/teksture/level1/powerup.png', (100, 100))

        # Preload fonts
        self.message_font = load_custom_font(30)
        self.invulnerability_title_font = load_custom_font(24)
        self.invulnerability_timer_font = load_custom_font(40)
        self.enemy_counter_font = load_custom_font(20)

        # Message display
        self.message = ""
        self.message_time = 0
        self.message_duration = 5000

    def draw(self):
        self.draw_background()
        self.render_game_objects()
        self.draw_player_health()
        self.draw_dash_indicator()
        self.draw_enemy_counter()
        self.draw_message()
        self.draw_invulnerability_indicator()

    def draw_enemy_counter(self):
        """Draw a counter showing the number of remaining enemies"""
        # Get the number of remaining enemies (excluding friendly NPCs)
        remaining_enemies = sum(1 for npc in self.game.object_handler.npc_list
                              if npc.alive and not hasattr(npc, 'is_friendly'))

        # Get total number of hostile enemies
        total_enemies = sum(1 for npc in self.game.object_handler.npc_list
                          if not hasattr(npc, 'is_friendly'))

        # Create the counter text
        counter_text = f"Enemies: {remaining_enemies}/{total_enemies}"

        # Calculate margin based on percentage
        margin_x = int(WIDTH * UI_MARGIN_PERCENT_X)
        margin_y = int(HEIGHT * UI_MARGIN_PERCENT_Y)
        position = (WIDTH - margin_x, HEIGHT - margin_y)

        # Custom positioning for bottom right
        text_surface = self.enemy_counter_font.render(counter_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(bottomright=position)
        bg_rect = text_rect.inflate(20, 10)
        bg_surface = pg.Surface((bg_rect.width, bg_rect.height), pg.SRCALPHA)
        bg_surface.fill((0, 0, 0, 150))
        self.screen.blit(bg_surface, bg_rect)
        self.screen.blit(text_surface, text_rect)

    def win(self):
        self.screen.blit(self.win_image, (0, 0))

    def game_over(self):
        self.screen.blit(self.game_over_image, (0, 0))

    def draw_player_health(self):
        health = str(self.game.player.health)

        # Calculate margin based on percentage
        margin_x = int(WIDTH * UI_MARGIN_PERCENT_X)
        margin_y = int(HEIGHT * UI_MARGIN_PERCENT_Y)

        for i, char in enumerate(health):
            self.screen.blit(self.digits[char], (margin_x + i * self.digit_size, margin_y))
        self.screen.blit(self.digits['10'], (margin_x + (i + 1) * self.digit_size, margin_y))

    def player_damage(self):
        self.screen.blit(self.blood_screen, (0, 0))

    def show_message(self, text):
        """Display a message on screen for a limited time"""
        self.message = text
        self.message_time = pg.time.get_ticks()

    def draw_message(self):
        """Draw the current message if it's active"""
        if self.message and pg.time.get_ticks() - self.message_time < self.message_duration:
            # Calculate margin based on percentage
            margin_y = int(HEIGHT * UI_MARGIN_PERCENT_Y)

            # Use a full-width background for messages
            bg_surface = pg.Surface((WIDTH, 80), pg.SRCALPHA)
            bg_surface.fill((0, 0, 0, 180))
            self.screen.blit(bg_surface, (0, self.digit_size + margin_y + 10))

            # Draw the message text centered
            position = (HALF_WIDTH, self.digit_size + margin_y + 50)
            text_surface = self.message_font.render(self.message, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=position)
            self.screen.blit(text_surface, text_rect)

    def draw_dash_indicator(self):
        current_time = pg.time.get_ticks()
        dash_cooldown_remaining = 0

        if not self.game.player.is_dashing:
            time_since_last_dash = current_time - self.game.player.last_dash_time
            if time_since_last_dash < PLAYER_DASH_COOLDOWN:
                dash_cooldown_remaining = 1 - (time_since_last_dash / PLAYER_DASH_COOLDOWN)

        # Nacrtaj indikator cooldowna
        indicator_width = 200
        indicator_height = 10

        # Calculate margins based on percentage
        margin_x = int(WIDTH * UI_MARGIN_PERCENT_X)
        margin_y = int(HEIGHT * UI_MARGIN_PERCENT_Y)

        indicator_x = WIDTH - indicator_width - margin_x
        indicator_y = margin_y

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

    def draw_invulnerability_indicator(self):
        """Draw the invulnerability powerup indicator and countdown"""
        if not self.game.player.is_invulnerable:
            return

        seconds_left = max(1, int(self.game.player.invulnerability_time_left / 1000) + 1)
        center_x = HALF_WIDTH

        # Calculate top margin based on percentage
        margin_y = int(HEIGHT * UI_MARGIN_PERCENT_Y)

        # Draw title text (using preloaded font)
        title_position = (center_x, margin_y + 30)
        title_surface = self.invulnerability_title_font.render("INVINCIBILITY", True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=title_position)
        self.screen.blit(title_surface, title_rect)

        # Draw icon (using preloaded texture)
        icon_rect = self.powerup_icon.get_rect(center=(center_x, margin_y + 80))
        self.screen.blit(self.powerup_icon, icon_rect)

        # Draw timer (using preloaded font)
        timer_position = (center_x, margin_y + 140)
        timer_surface = self.invulnerability_timer_font.render(f"{seconds_left}s", True, (255, 255, 255))
        timer_rect = timer_surface.get_rect(center=timer_position)
        self.screen.blit(timer_surface, timer_rect)

    def draw_background(self):
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIDTH
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))
        # floor
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def render_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for _, image, pos in list_objects:
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

            6: self.get_texture('resources/teksture/6.jpg'),
            7: self.get_texture('resources/teksture/11.png'),
            8: self.get_texture('resources/teksture/8.png'),
            9: self.get_texture('resources/teksture/9.png'),
            10: self.get_texture('resources/teksture/level2/zid1.png'),
            13: self.get_texture('resources/teksture/level2/zid2.png'),

            11: self.get_texture('resources/teksture/vrata1.png'), ## vrata crna zatvorena
            12: self.get_texture('resources/teksture/ukras4.png'), ## ne korišteno warning terminal

            14: self.get_texture('resources/teksture/ukras1.png'), ## panel za level 1 crno sivi
            15: self.get_texture('resources/teksture/prozor.jpg'), ## prozor ne korišten nema smisla

            4: self.get_texture('resources/teksture/level2/zid2.png'), ## bijeli zid level 1 / level 2 - prijelaz/vanjski
            16: self.get_texture('resources/teksture/level2/vrata1.png'), ##vrata bijela zatvorena
            17: self.get_texture('resources/teksture/uvod/zid5.jpg'), ## zid sa malo krvi (manje od uvod/zid1)
            18: self.get_texture('resources/teksture/level2/zid3.png'), ##zid s kockama sobe
            19: self.get_texture('resources/teksture/level2/panel.png'), ## bijeli panel

            20: self.get_texture('resources/teksture/level2/zagonetka1.png'), ## Zid sa Ultimate
            21: self.get_texture('resources/teksture/level2/zagonetka2.png'), ## Zid sa Six 6
            22: self.get_texture('resources/teksture/level2/zagonetka3.png'), ## Zid sa BY
            23: self.get_texture('resources/teksture/level2/zagonetka4.png'), ## Zid sa Seven 7

            24: self.get_texture('resources/teksture/level2/zid4.png'), ## bijeli zid s drugacijim paternom

            25: self.get_texture('resources/teksture/level3/zid2.png'), ## glavni zid za mapu žučkast
            26: self.get_texture('resources/teksture/level3/zid3.png'), ## sporedni zid za mapu žučkast sa bačvama
            27: self.get_texture('resources/teksture/level3/zid1.png'), ## labaratorijski zid sa najviše detalja alien
            28: self.get_texture('resources/teksture/level3/zid4.png'), ## labaratorijski zid sa manje detalja biljka
            29: self.get_texture('resources/teksture/level3/vrata1.png'), ## žučkasta vrata za mapu zatvorena

        }