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
from menu import *


class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)

        # Initialize sound first so menu can access volume settings
        self.sound = Sound(self)

        # Create menu
        self.menu = Menu(self)

        # Start with menu instead of directly starting the game
        self.game_started = False

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.pathfinding = PathFinding(self)
        pg.mixer.music.play(-1)
        self.game_started = True

    def update(self):
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        self.weapon.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        # Draw the game scene
        self.object_renderer.draw()
        self.weapon.draw()

        # Debug visualization methods - not used in production
        # self.screen.fill('black')
        # self.map.draw()
        # self.player.draw()

    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                # Return to menu when Escape is pressed
                self.game_started = False
                self.menu.state = 'main'
                pg.mouse.set_visible(True)
                return
            elif event.type == self.global_event:
                self.global_trigger = True
            self.player.single_fire_event(event)

    def run(self):
        while True:
            if not self.game_started:
                # Show menu
                self.menu.run()
                if self.menu.state == 'game':
                    # Start or resume game
                    if not hasattr(self, 'map'):
                        self.new_game()
                    else:
                        self.game_started = True
                        pg.mouse.set_visible(False)
            else:
                # Run game
                self.check_events()
                self.update()
                self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()
