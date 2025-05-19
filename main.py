import pygame as pg
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *
from weapon import Pistol, SMG, PlasmaGun
from sound import *
from pathfinding import *
from interaction import Interaction
from level_manager import LevelManager
from dialogue import DialogueManager
from menu import Menu
from intro_sequence import IntroSequence
from loading_screen import LoadingScreen
from level_transition import LevelTransition
from game_events import GameEvents
from death_screen import DeathScreen
from victory_screen import VictoryScreen
from ui import GameUI
from visual_effects import DisorientingEffects


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
        self.intro_sequence = IntroSequence(self)
        self.loading_screen = LoadingScreen(self)
        self.level_transition = LevelTransition(self)
        self.death_screen = DeathScreen(self)
        self.victory_screen = VictoryScreen(self)
        self.game_events = GameEvents(self)
        self.disorienting_effects = DisorientingEffects(self)
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


        # Create the appropriate weapon based on the stored weapon type
        if self.level_manager.current_level == 1:
            # No weapon for level 1 until pickup
            self.weapon = None
        elif hasattr(self, 'level_manager'):
            if self.level_manager.current_weapon_type == 'smg':
                self.weapon = SMG(self)
            elif self.level_manager.current_weapon_type == 'plasmagun':
                self.weapon = PlasmaGun(self)
            else:
                self.weapon = Pistol(self)
        else:
            self.weapon = Pistol(self)

        self.pathfinding = PathFinding(self)
        self.interaction = Interaction(self)

        # Initialize dialogue manager
        if not hasattr(self, 'dialogue_manager'):
            self.dialogue_manager = DialogueManager(self)

        # Initialize or update UI
        if not hasattr(self, 'game_ui'):
            self.game_ui = GameUI(self)
        else:
            # Update UI for the current level
            self.game_ui.update_level(self.level_manager.current_level)

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
        elif self.level_manager.current_level == 4:
            self.player.x, self.player.y = PLAYER_POS_LEVEL4
        elif self.level_manager.current_level == 5:
            self.player.x, self.player.y = PLAYER_POS_LEVEL5

        self.object_renderer.update_sky_image()

        # Promijeni glazbu ovisno o trenutnoj razini
        self.sound.change_music_for_level(self.level_manager.current_level)

        if self.level_manager.current_level == 1:
            self.intro_sequence.start()

    def update(self):
        if self.death_screen.active:
            self.death_screen.update()
            return

        if self.victory_screen.active:
            self.victory_screen.update()
            return

        # Update game components
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        if self.weapon:  # Only update weapon if it exists
            self.weapon.update()
        self.interaction.update()
        self.dialogue_manager.update()

        self.intro_sequence.update()
        self.intro_sequence.update_music_fade()
        self.disorienting_effects.update()
        self.loading_screen.update()
        self.level_transition.update()

        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)

    def draw(self):
        if self.death_screen.active:
            self.death_screen.draw()
            return

        if self.victory_screen.active:
            self.victory_screen.draw()
            return

        # Draw game components
        self.object_renderer.draw()
        if self.weapon:  # Only draw weapon if it exists
            self.weapon.draw()
        self.game_ui.draw()
        self.interaction.draw()
        self.dialogue_manager.draw()

        # Apply visual effects
        self.disorienting_effects.draw()

        # Draw overlays
        self.intro_sequence.draw()
        self.loading_screen.draw()
        self.level_transition.draw()

    def check_events(self):
        if self.death_screen.active:
            return self.death_screen.handle_events()

        if self.victory_screen.active:
            return self.victory_screen.handle_events()

        return self.game_events.process_events()

    def next_level(self):
        """Advance to the next level"""
        return self.level_transition.transition_to_next_level()

    def reset_current_level(self):
        """Reset the current level when player dies"""
        current_level = self.level_manager.current_level
        self.map.load_level(current_level)
        self.new_game()  # new_game() će promijeniti glazbu
        pg.mouse.set_visible(False)

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
            if self.check_events():
                return
            self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
