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
from interaction import Interaction
from level_manager import LevelManager
from dialogue import DialogueManager


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
        self.new_game()

    def new_game(self):
        # Initialize level manager if it doesn't exist
        if not hasattr(self, 'level_manager'):
            self.level_manager = LevelManager(self)

        # Initialize map if it doesn't exist or reset it for a new game
        if not hasattr(self, 'map'):
            self.map = Map(self)
        # Otherwise, make sure the map is loaded for the current level
        else:
            self.map.load_level(self.level_manager.current_level)

        # Initialize or reset other game components
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)

        # Initialize object handler if it doesn't exist or reset it for a new level
        if not hasattr(self, 'object_handler'):
            self.object_handler = ObjectHandler(self)
        else:
            self.object_handler.reset()  # Reset for new level

        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.pathfinding = PathFinding(self)
        self.interaction = Interaction(self)

        # Initialize dialogue manager
        if not hasattr(self, 'dialogue_manager'):
            self.dialogue_manager = DialogueManager(self)

        # Set up dialogue NPCs for the current level
        self.level_manager.setup_dialogue_npcs()

        # Set up interactive objects for the current level
        self.level_manager.setup_interactive_objects()

        # Update pathfinding graph
        self.pathfinding.update_graph()

        # Set player position based on level
        if self.level_manager.current_level == 1:
            self.player.x, self.player.y = PLAYER_POS  # Starting position for level 1
        elif self.level_manager.current_level == 2:
            self.player.x, self.player.y = PLAYER_POS_LEVEL2  # Starting position for level 2
        elif self.level_manager.current_level == 3:
            self.player.x, self.player.y = PLAYER_POS_LEVEL3  # Starting position for level 3

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
        # Draw the game scene
        self.object_renderer.draw()
        self.weapon.draw()
        self.interaction.draw()
        self.dialogue_manager.draw()

        # Debug visualization methods - not used in production
        # self.screen.fill('black')
        # self.map.draw()
        # self.player.draw()

    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE and not self.interaction.input_active):
                pg.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True
            # Debug key to advance to next level (N key)
            elif event.type == pg.KEYDOWN and event.key == pg.K_n:
                self.next_level()
            # Handle dialogue key events
            elif event.type == pg.KEYDOWN and event.key == pg.K_e:
                # If dialogue is active, advance or end it
                if self.dialogue_manager.dialogue_active:
                    self.dialogue_manager.handle_key_press()
                # Otherwise, check if player is near a dialogue NPC
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
            # Display loading message
            font = pg.font.SysFont('Arial', 36)
            text_surface = font.render("Loading next level...", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(HALF_WIDTH, HALF_HEIGHT))
            self.screen.blit(text_surface, text_rect)
            pg.display.flip()
            pg.time.delay(1000)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()