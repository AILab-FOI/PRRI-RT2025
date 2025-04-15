import pygame as pg
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *
from weapon import Weapon, Pistol, SMG
from sound import *
from pathfinding import *
from interaction import Interaction
from level_manager import LevelManager
from dialogue import DialogueManager
from menu import Menu
from font_manager import load_custom_font


class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption('PRRI-RT2025')
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)

        self.sound = Sound(self)
        self.menu = Menu(self)
        self.game_initialized = False
        self.show_menu()

    def new_game(self):
        if not hasattr(self, 'level_manager'):
            self.level_manager = LevelManager(self)

        if not hasattr(self, 'map'):
            self.map = Map(self)
        else:
            self.map.load_level(self.level_manager.current_level)

        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)

        if not hasattr(self, 'object_handler'):
            self.object_handler = ObjectHandler(self)
        else:
            self.object_handler.reset()

        self.weapon = Pistol(self)  # Start with a pistol
        self.pathfinding = PathFinding(self)
        self.interaction = Interaction(self)

        # Initialize dialogue manager
        if not hasattr(self, 'dialogue_manager'):
            self.dialogue_manager = DialogueManager(self)

        self.level_manager.setup_dialogue_npcs()
        self.level_manager.setup_interactive_objects()
        self.pathfinding.update_graph()

        # Set player position based on level
        if self.level_manager.current_level == 1:
            self.player.x, self.player.y = PLAYER_POS
        elif self.level_manager.current_level == 2:
            self.player.x, self.player.y = PLAYER_POS_LEVEL2 
        elif self.level_manager.current_level == 3:
            self.player.x, self.player.y = PLAYER_POS_LEVEL3 

        if not pg.mixer.music.get_busy():
            pg.mixer.music.play(-1)

    def update(self):
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        self.weapon.update()
        self.interaction.update()
        self.dialogue_manager.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        self.object_renderer.draw()
        self.weapon.draw()
        self.interaction.draw()
        self.dialogue_manager.draw()

    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE and not self.interaction.input_active:
                self.show_menu()
                return  
            elif event.type == self.global_event:
                self.global_trigger = True

            # Debug key to advance to next level (N key)
            elif event.type == pg.KEYDOWN and event.key == pg.K_n:
                self.next_level()

           
            elif event.type == pg.KEYDOWN and event.key == pg.K_e:
                if self.dialogue_manager.dialogue_active:
                    self.dialogue_manager.handle_key_press()
                else:
                    for npc in self.object_handler.npc_list:
                        if hasattr(npc, 'is_friendly') and npc.is_friendly and hasattr(npc, 'interaction_indicator_visible'):
                            if npc.interaction_indicator_visible:
                                npc.start_dialogue()
                                break

            self.player.single_fire_event(event)
            self.interaction.handle_key_event(event)

    def next_level(self):
        """Advance to the next level"""
        if self.level_manager.next_level():
            font = load_custom_font(30)
            text_surface = font.render("Loading next level...", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(HALF_WIDTH, HALF_HEIGHT))
            self.screen.blit(text_surface, text_rect)
            pg.display.flip()
            pg.time.delay(1000)

    def show_menu(self):
        pg.mouse.set_visible(True)
        self.menu.state = 'main'
        self.menu.run()

        if not self.game_initialized:
            self.new_game()
            self.game_initialized = True

        pg.mouse.set_visible(False)
        self.game_loop()

    def game_loop(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()