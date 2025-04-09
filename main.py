import pygame as pg
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *
from weapon import *
from sound import *
from pathfinding import *


class Game:
    def __init__(self): 
        pg.init()
        try:
            pg.mixer.init()  # Pokušaj inicijalizacije Pygame-ovog audio sistema
        except pg.error as e:
            print(f"Greška prilikom inicijalizacije miksera: {e}")
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)
        self.new_game()

    def new_game(self):
     self.map = Map(self)
     self.player = Player(self)
     self.object_renderer = ObjectRenderer(self)
     self.raycasting = RayCasting(self)
     self.object_handler = ObjectHandler(self)
     self.weapon = Weapon(self)
     self.sound = Sound(self)
     self.pathfinding = PathFinding(self)
     self.enemy_count = len(self.object_handler.npc_list)  # Dodajemo broj neprijatelja
     if pg.mixer.get_init():  # Proverite da li je mikser inicijalizovan
            pg.mixer.music.play(-1)
     else:
            print("Mikser nije inicijalizovan. Muzika neće biti puštena.")

    def update(self):
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        self.weapon.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        # self.screen.fill('black')
        self.object_renderer.draw()
        self.weapon.draw()
        self.draw_enemy_count()  # Dodajemo prikaz broja neprijatelja
        # self.map.draw()
        # self.player.draw()
    
    def draw_enemy_count(self):
     font = pg.font.SysFont('Arial', 30, True)
     text_surface = font.render(f'Neprijatelji: {self.enemy_count}', True, (255, 0, 0))
     text_rect = text_surface.get_rect()
     text_rect.bottomright = (self.screen.get_width() -50, self.screen.get_height() - 20)  # Donji desni ugao
     self.screen.blit(text_surface, text_rect)


    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True
            self.player.single_fire_event(event)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw() 

    def enemy_defeated(self):
     if self.enemy_count > 0:  # Proverite da broj neprijatelja ne ide ispod nule
        self.enemy_count -= 1
        print(f"Preostali neprijatelji: {self.enemy_count}")
        if self.enemy_count <= 0:
            print("Svi neprijatelji su poraženi!")
     else:
        print("Greška: Broj neprijatelja je već 0!")

if __name__ == '__main__':
    game = Game()
    game.run()
