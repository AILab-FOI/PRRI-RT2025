import pygame as pg
import sys
import time
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
from texture_manager import TextureManager
from loading_screen import LoadingScreen


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

        # Initialize texture manager before other components
        self.texture_manager = TextureManager()

        # Initialize loading screen
        self.loading_screen = LoadingScreen(self)

        # Show initial loading screen
        self.loading_screen.start_loading("Starting game...")
        self.loading_screen.draw()

        # Start the game
        self.new_game()

    def new_game(self, skip_loading_screen=False):
        # Show loading screen (unless we're skipping it)
        if not skip_loading_screen:
            self.loading_screen.start_loading("Loading game...", self.level_manager.current_level if hasattr(self, 'level_manager') else 1)
            self.loading_screen.draw()

        # Initialize level manager if it doesn't exist
        if not hasattr(self, 'level_manager'):
            self.level_manager = LevelManager(self)
            self.loading_screen.update(20)
            self.loading_screen.draw()

        # Initialize map if it doesn't exist or reset it for a new game
        if not hasattr(self, 'map'):
            self.map = Map(self)
        # Otherwise, make sure the map is loaded for the current level
        else:
            self.map.load_level(self.level_manager.current_level)
        self.loading_screen.update(30)
        self.loading_screen.draw()

        # Initialize or reset other game components
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.loading_screen.update(40)
        self.loading_screen.draw()

        # Initialize object handler if it doesn't exist or reset it for a new level
        if not hasattr(self, 'object_handler'):
            self.object_handler = ObjectHandler(self)
        else:
            self.object_handler.reset()  # Reset for new level
        self.loading_screen.update(50)
        self.loading_screen.draw()

        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.pathfinding = PathFinding(self)
        self.interaction = Interaction(self)
        self.loading_screen.update(60)
        self.loading_screen.draw()

        # Initialize dialogue manager
        if not hasattr(self, 'dialogue_manager'):
            self.dialogue_manager = DialogueManager(self)
        self.loading_screen.update(70)
        self.loading_screen.draw()

        # Set up dialogue NPCs for the current level
        self.level_manager.setup_dialogue_npcs()
        self.loading_screen.update(80)
        self.loading_screen.draw()

        # Set up interactive objects for the current level
        self.level_manager.setup_interactive_objects()
        self.loading_screen.update(90)
        self.loading_screen.draw()

        # Update pathfinding graph
        self.pathfinding.update_graph()

        # Set player position based on level
        if self.level_manager.current_level == 1:
            self.player.x, self.player.y = PLAYER_POS  # Starting position for level 1
        elif self.level_manager.current_level == 2:
            self.player.x, self.player.y = PLAYER_POS_LEVEL2  # Starting position for level 2
        elif self.level_manager.current_level == 3:
            self.player.x, self.player.y = PLAYER_POS_LEVEL3  # Starting position for level 3
        self.loading_screen.update(95)
        self.loading_screen.draw()

        pg.mixer.music.play(-1)

        # Complete loading and wait for minimum time
        self.loading_screen.update(100)
        self.loading_screen.draw()
        self.loading_screen.wait_for_minimum_time()

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
            # Show loading screen for next level
            next_level = self.level_manager.current_level

            # Reset loading screen progress and start loading
            self.loading_screen.progress = 0
            self.loading_screen.start_loading(f"Loading Level {next_level}...", next_level)
            self.loading_screen.draw()

            # Wait a moment to show the loading screen with 0% progress
            pg.time.delay(500)

            # Now initialize the new level
            self.new_game(skip_loading_screen=True)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()