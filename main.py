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

        # Initialize sound first since menu needs it
        self.sound = Sound(self)

        # Create menu
        self.menu = Menu(self)

        # Track if game is already initialized
        self.game_initialized = False

        # Start with the menu, then transition to the game
        self.show_menu()

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

        self.weapon = Pistol(self)  # Start with a pistol
        # Sound is already initialized in __init__
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

        # Start music if it's not already playing
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
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            # Handle Escape key - return to menu if not in dialogue or input mode
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE and not self.interaction.input_active:
                # Return to menu
                self.show_menu()
                return  # Exit the event loop since we're going back to menu
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
            # Display loading message with custom font
            font = load_custom_font(30)
            text_surface = font.render("Loading next level...", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(HALF_WIDTH, HALF_HEIGHT))
            self.screen.blit(text_surface, text_rect)
            pg.display.flip()
            pg.time.delay(1000)

    def show_menu(self):
        """Show the main menu and start the game when ready"""
        # Make mouse visible for menu
        pg.mouse.set_visible(True)

        # Reset menu state if returning from game
        self.menu.state = 'main'

        # Let music continue playing in the menu
        # We don't need to do anything special here since we're not pausing the music

        # Run the menu loop
        self.menu.run()

        # When menu.run() returns, start or continue the game
        if not self.game_initialized:
            # First time starting the game
            self.new_game()
            self.game_initialized = True
        # else: game is already initialized, just continue

        # Make sure mouse is invisible for game
        pg.mouse.set_visible(False)

        # Start the game loop
        self.game_loop()

    def game_loop(self):
        """Main game loop"""
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
    # The game starts from show_menu() which is called in __init__