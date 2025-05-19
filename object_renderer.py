import pygame as pg
import os
import sys
from settings import *
from font_manager import load_custom_font, resource_path


class ObjectRenderer:
    def draw_text_with_background(self, text, font, color, position, center=False, bg_color=(0, 0, 0, 150), padding=(20, 10)):
        text_surface = font.render(text, True, color)

        if center:
            text_rect = text_surface.get_rect(center=position)
        else:
            text_rect = text_surface.get_rect(topleft=position)

        bg_rect = text_rect.inflate(padding[0], padding[1])
        bg_surface = pg.Surface((bg_rect.width, bg_rect.height), pg.SRCALPHA)
        bg_surface.fill(bg_color)
        self.screen.blit(bg_surface, bg_rect)
        self.screen.blit(text_surface, text_rect)

        return text_rect

    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()

        self.sky_images = {
            1: self.get_texture('resources/teksture/level2/sky2.png', (WIDTH, HALF_HEIGHT)),
            2: self.get_texture('resources/teksture/level1/sky1.png', (WIDTH, HALF_HEIGHT)),
            3: self.get_texture('resources/teksture/level2/sky2.png', (WIDTH, HALF_HEIGHT)),
            4: self.get_texture('resources/teksture/level3/sky.png', (WIDTH, HALF_HEIGHT)),
            5: self.get_texture('resources/teksture/level4/sky1.png', (WIDTH, HALF_HEIGHT))
        }
        self.sky_image = self.sky_images[1]
        self.sky_offset = 0

        self.blood_screen = self.get_texture('resources/teksture/blood_screen.png', RES)
        self.game_over_image = self.get_texture('resources/teksture/theEnd.png', RES)
        self.win_image = self.get_texture('resources/teksture/win.png', RES)
        self.message_font = load_custom_font(30)
        self.message = ""
        self.message_time = 0
        self.message_duration = 5000

    def draw(self):
        self.draw_background()
        self.render_game_objects()
        self.draw_message()

    def win(self):
        self.screen.blit(self.win_image, (0, 0))

    def game_over(self):
        self.screen.blit(self.game_over_image, (0, 0))

    def player_damage(self):
        self.screen.blit(self.blood_screen, (0, 0))

    def show_message(self, text):
        self.message = text
        self.message_time = pg.time.get_ticks()

    def draw_message(self):
        if self.message and pg.time.get_ticks() - self.message_time < self.message_duration:
            margin_y = int(HEIGHT * UI_MARGIN_PERCENT_Y)

            bg_surface = pg.Surface((WIDTH, 80), pg.SRCALPHA)
            bg_surface.fill((0, 0, 0, 180))
            self.screen.blit(bg_surface, (0, margin_y + 100))

            position = (HALF_WIDTH, margin_y + 140)
            text_surface = self.message_font.render(self.message, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=position)
            self.screen.blit(text_surface, text_rect)

    def update_sky_image(self):
        if hasattr(self.game, 'level_manager'):
            current_level = self.game.level_manager.current_level
            if current_level in self.sky_images:
                self.sky_image = self.sky_images[current_level]
            else:
                self.sky_image = self.sky_images[3]

    def draw_background(self):
        self.update_sky_image()

        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIDTH
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))

        floor_color = FLOOR_COLOR
        if hasattr(self.game, 'level_manager'):
            current_level = self.game.level_manager.current_level
            if current_level in FLOOR_COLORS:
                floor_color = FLOOR_COLORS[current_level]

        pg.draw.rect(self.screen, floor_color, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def render_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for _, image, pos in list_objects:
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture_path = resource_path(path)
        print(f"Loading texture: {texture_path}")
        texture = pg.image.load(texture_path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_wall_textures(self):
        return {
            #1. level
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

            #2. level
            4: self.get_texture('resources/teksture/level2/zid2.png'), ## bijeli zid level 1 / level 2 - prijelaz/vanjski
            16: self.get_texture('resources/teksture/level2/vrata1.png'), ##vrata bijela zatvorena
            17: self.get_texture('resources/teksture/uvod/zid5.jpg'), ## zid sa malo krvi (manje od uvod/zid1)
            18: self.get_texture('resources/teksture/level2/zid3.png'), ##zid s kockama sobe
            19: self.get_texture('resources/teksture/level2/panel.png'), ## bijeli panel

            20: self.get_texture('resources/teksture/level2/zagonetka1.png'), ## Zid sa Ultimate
            21: self.get_texture('resources/teksture/level2/zagonetka2.png'), ## Zid sa Six 6
            22: self.get_texture('resources/teksture/level2/zagonetka3.png'), ## Zid sa Multiply
            23: self.get_texture('resources/teksture/level2/zagonetka4.png'), ## Zid sa Seven 7

            24: self.get_texture('resources/teksture/level2/zid4.png'), ## bijeli zid s drugacijim paternom
            30: self.get_texture('resources/teksture/level2/vrataPrelaz2.png'), ## završna vrata na levelu 2
            31: self.get_texture('resources/teksture/level2/vrataZagonetka.png'), ## vrata za zagonetku

            #3. level
            25: self.get_texture('resources/teksture/level3/zid2.png'), ## glavni zid za mapu žučkast
            26: self.get_texture('resources/teksture/level3/zid3.png'), ## sporedni zid za mapu žučkast sa bačvama
            27: self.get_texture('resources/teksture/level3/zid1.png'), ## labaratorijski zid sa najviše detalja alien
            28: self.get_texture('resources/teksture/level3/zid4.png'), ## labaratorijski zid sa manje detalja biljka
            29: self.get_texture('resources/teksture/level3/vrata2.jpg'), ## žučkasta vrata za mapu lagano otvorena
            32: self.get_texture('resources/teksture/level3/ekstenzije/VrataPrijelaz/0.png'),
            39: self.get_texture('resources/teksture/level3/ekstenzije/VrataPrijelaz/1.png'), #vrata prijelaz na sljedeci level


            #uvodni level
            33: self.get_texture('resources/teksture/uvod/zid1.jpg'), #bijeli zid crvena svjetla manja količina krvi u sredini
            34: self.get_texture('resources/teksture/uvod/zid2.jpg'), #bijeli zid s srednjom količinom krvi
            35: self.get_texture('resources/teksture/uvod/zid3.jpg'), #bijeli zid s velikom količinom krvi
            36: self.get_texture('resources/teksture/uvod/zid4.jpg'), #bijeli zid s krvavom rukom u sredini
            37: self.get_texture('resources/teksture/uvod/zid5.jpg'), #bijeli zid s manjom količinom krvi niže od prvog zida
            38: self.get_texture('resources/teksture/uvod/vrata5.jpg'),

            #boss level (zadnji level)
            40: self.get_texture('resources/teksture/level4/zid1.png'), #base zid
            41: self.get_texture('resources/teksture/level4/zid2.png'), #base zid sa malim prozorom
            42: self.get_texture('resources/teksture/level4/zid3.png'), #base zid s konzolom i prozor
            43: self.get_texture('resources/teksture/level4/zid4.png'), #base zid s velikim prozorom


        }