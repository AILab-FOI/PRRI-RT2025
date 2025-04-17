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
            self.loading_screen.update(10, "Initializing level manager...")
            self.loading_screen.draw()
            self.level_manager = LevelManager(self)
            self.loading_screen.update(20, "Level manager initialized")
            self.loading_screen.draw()

        # Initialize map if it doesn't exist or reset it for a new game
        self.loading_screen.update(25, "Loading map data...")
        self.loading_screen.draw()
        if not hasattr(self, 'map'):
            self.map = Map(self)
        # Otherwise, make sure the map is loaded for the current level
        else:
            self.map.load_level(self.level_manager.current_level)
        self.loading_screen.update(30, "Map data loaded")
        self.loading_screen.draw()

        # Initialize or reset other game components
        self.loading_screen.update(35, "Initializing player...")
        self.loading_screen.draw()
        self.player = Player(self)

        self.loading_screen.update(40, "Loading textures...")
        self.loading_screen.draw()
        self.object_renderer = ObjectRenderer(self)

        self.loading_screen.update(45, "Setting up raycasting...")
        self.loading_screen.draw()
        self.raycasting = RayCasting(self)

        # Initialize object handler if it doesn't exist or reset it for a new level
        self.loading_screen.update(50, "Loading game objects...")
        self.loading_screen.draw()
        if not hasattr(self, 'object_handler'):
            self.object_handler = ObjectHandler(self)
        else:
            self.object_handler.reset()  # Reset for new level
        self.loading_screen.update(55, "Game objects loaded")
        self.loading_screen.draw()

        self.loading_screen.update(60, "Loading weapons...")
        self.loading_screen.draw()
        self.weapon = Weapon(self)

        self.loading_screen.update(65, "Initializing sound system...")
        self.loading_screen.draw()
        self.sound = Sound(self)

        self.loading_screen.update(70, "Setting up pathfinding...")
        self.loading_screen.draw()
        self.pathfinding = PathFinding(self)

        self.loading_screen.update(75, "Initializing interaction system...")
        self.loading_screen.draw()
        self.interaction = Interaction(self)

        # Initialize dialogue manager
        self.loading_screen.update(80, "Loading dialogue system...")
        self.loading_screen.draw()
        if not hasattr(self, 'dialogue_manager'):
            self.dialogue_manager = DialogueManager(self)

        # Set up dialogue NPCs for the current level
        self.loading_screen.update(85, "Setting up NPCs...")
        self.loading_screen.draw()
        self.level_manager.setup_dialogue_npcs()

        # Set up interactive objects for the current level
        self.loading_screen.update(90, "Setting up interactive objects...")
        self.loading_screen.draw()
        self.level_manager.setup_interactive_objects()

        # Update pathfinding graph
        self.loading_screen.update(92, "Calculating pathfinding graph...")
        self.loading_screen.draw()
        self.pathfinding.update_graph()

        # Set player position based on level
        self.loading_screen.update(95, "Finalizing level setup...")
        self.loading_screen.draw()
        if self.level_manager.current_level == 1:
            self.player.x, self.player.y = PLAYER_POS  # Starting position for level 1
        elif self.level_manager.current_level == 2:
            self.player.x, self.player.y = PLAYER_POS_LEVEL2  # Starting position for level 2
        elif self.level_manager.current_level == 3:
            self.player.x, self.player.y = PLAYER_POS_LEVEL3  # Starting position for level 3

        self.loading_screen.update(97, "Starting background music...")
        self.loading_screen.draw()
        pg.mixer.music.play(-1)

        # Complete loading and wait for minimum time
        self.loading_screen.update(100, "Loading complete!")
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

            # Start fade out transition
            self.loading_screen.fade_out()

            # Wait for fade to complete
            fade_start = pg.time.get_ticks()
            while not self.loading_screen.fade_complete and pg.time.get_ticks() - fade_start < LOADING_FADE_DURATION * 1.2:
                self.loading_screen.update()
                self.loading_screen.draw()
                pg.time.delay(10)  # Small delay to not hog CPU

            # Reset loading screen progress and start loading
            self.loading_screen.progress = 0
            self.loading_screen.start_loading(f"Loading Level {next_level}...", next_level)
            self.loading_screen.draw()

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