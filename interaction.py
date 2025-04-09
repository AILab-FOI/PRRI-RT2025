import pygame as pg
import math
from settings import *
from sprite_object import SpriteObject

class Interaction:
    def __init__(self, game):
        self.game = game
        self.interaction_objects = []
        self.interaction_distance = 1.5  # Maximum distance for interaction
        self.active_object = None
        self.show_interaction_prompt = False
        self.font = pg.font.SysFont('Arial', 36)
        self.small_font = pg.font.SysFont('Arial', 24)
        self.input_code = ""  # Code being entered by player
        self.input_active = False
        self.unlocked_doors = set()  # Set of door IDs that have been unlocked
        self.message = ""
        self.message_time = 0
        self.message_duration = 3000  # 3 seconds

    def add_object(self, obj):
        self.interaction_objects.append(obj)

    def update(self):
        # Check if player is near any interaction object
        player_pos = self.game.player.pos
        self.active_object = None
        self.show_interaction_prompt = False

        for obj in self.interaction_objects:
            distance = math.hypot(player_pos[0] - obj.x, player_pos[1] - obj.y)
            if distance < self.interaction_distance:
                self.active_object = obj
                self.show_interaction_prompt = True
                break

        # Clear message after duration
        if self.message and pg.time.get_ticks() - self.message_time > self.message_duration:
            self.message = ""

    def draw(self):
        # Draw interaction prompt if player is near an interactive object
        if self.show_interaction_prompt and not self.input_active:
            # Draw a crosshair/indicator in the center of the screen
            indicator_size = 20
            pg.draw.circle(self.game.screen, (255, 255, 255), (HALF_WIDTH, HALF_HEIGHT), indicator_size, 2)
            pg.draw.line(self.game.screen, (255, 255, 255),
                        (HALF_WIDTH - indicator_size, HALF_HEIGHT),
                        (HALF_WIDTH + indicator_size, HALF_HEIGHT), 2)
            pg.draw.line(self.game.screen, (255, 255, 255),
                        (HALF_WIDTH, HALF_HEIGHT - indicator_size),
                        (HALF_WIDTH, HALF_HEIGHT + indicator_size), 2)

            # Draw the prompt text
            prompt_text = f"Press E to {self.active_object.interaction_type}"
            text_surface = self.font.render(prompt_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(HALF_WIDTH, HEIGHT - 100))
            self.game.screen.blit(text_surface, text_rect)

        # Draw code input interface
        if self.input_active:
            # Background - create a semi-transparent surface
            bg_surface = pg.Surface((400, 200), pg.SRCALPHA)
            bg_surface.fill((0, 0, 0, 180))
            self.game.screen.blit(bg_surface, (HALF_WIDTH - 200, HALF_HEIGHT - 100))

            # Border
            pg.draw.rect(self.game.screen, (50, 50, 50), (HALF_WIDTH - 200, HALF_HEIGHT - 100, 400, 200), 2)

            # Title
            title_text = "Enter Code:"
            title_surface = self.font.render(title_text, True, (255, 255, 255))
            title_rect = title_surface.get_rect(center=(HALF_WIDTH, HALF_HEIGHT - 60))
            self.game.screen.blit(title_surface, title_rect)

            # Input field
            input_text = self.input_code + "_" if len(self.input_code) < 4 else self.input_code
            input_surface = self.font.render(input_text, True, (255, 255, 255))
            input_rect = input_surface.get_rect(center=(HALF_WIDTH, HALF_HEIGHT))
            self.game.screen.blit(input_surface, input_rect)

            # Instructions
            instr_text = "Press Enter to confirm, Escape to cancel"
            instr_surface = self.small_font.render(instr_text, True, (200, 200, 200))
            instr_rect = instr_surface.get_rect(center=(HALF_WIDTH, HALF_HEIGHT + 60))
            self.game.screen.blit(instr_surface, instr_rect)

        # Draw message if there is one
        if self.message:
            message_surface = self.font.render(self.message, True, (255, 255, 255))
            message_rect = message_surface.get_rect(center=(HALF_WIDTH, HEIGHT - 150))
            self.game.screen.blit(message_surface, message_rect)

    def handle_key_event(self, event):
        # Handle E key press for interaction
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_e and self.show_interaction_prompt and not self.input_active:
                self.interact()

            # Handle input for door code
            elif self.input_active:
                if event.key == pg.K_ESCAPE:
                    self.input_active = False
                    self.input_code = ""
                elif event.key == pg.K_RETURN:
                    self.check_code()
                elif event.key == pg.K_BACKSPACE:
                    self.input_code = self.input_code[:-1]
                elif event.unicode.isdigit() and len(self.input_code) < 4:
                    self.input_code += event.unicode

    def interact(self):
        if self.active_object:
            if self.active_object.interaction_type == "terminal":
                self.show_terminal_code()
            elif self.active_object.interaction_type == "door":
                # Check if this door requires another door to be opened first
                if self.active_object.requires_door_id and self.active_object.requires_door_id not in self.unlocked_doors:
                    self.message = f"You need to open door {self.active_object.requires_door_id} first!"
                    self.message_time = pg.time.get_ticks()
                    return

                # Check if door requires a code
                if self.active_object.requires_code:
                    if self.active_object.is_unlocked or self.active_object.door_id in self.unlocked_doors:
                        self.open_door()
                    else:
                        self.input_active = True
                else:
                    # Door doesn't require a code, just open it
                    self.open_door()

    def show_terminal_code(self):
        if self.active_object and self.active_object.code:
            self.message = f"Terminal Code: {self.active_object.code}"
            self.message_time = pg.time.get_ticks()
            self.game.sound.terminal_beep.play()

            # Note: We no longer automatically unlock doors when viewing the terminal code
            # The player must enter the code at each door

    def check_code(self):
        if self.active_object and self.active_object.requires_code:
            # Get the correct code directly from the door object
            correct_code = self.active_object.code

            if self.input_code == correct_code:
                self.active_object.is_unlocked = True
                self.unlocked_doors.add(self.active_object.door_id)
                self.open_door()
            else:
                self.message = "Incorrect code!"
                self.message_time = pg.time.get_ticks()

        self.input_active = False
        self.input_code = ""

    def open_door(self):
        # Remove door from world map to allow passage
        door_pos = self.active_object.map_pos
        if door_pos in self.game.map.world_map:
            # Remove from world map
            del self.game.map.world_map[door_pos]

            # Remove the door sprite from sprite list
            if self.active_object in self.game.object_handler.sprite_list:
                self.game.object_handler.sprite_list.remove(self.active_object)

            # Remove from interaction objects
            if self.active_object in self.interaction_objects:
                self.interaction_objects.remove(self.active_object)

            self.message = "Door opened!"
            self.message_time = pg.time.get_ticks()
            self.game.sound.door_open.play()

            # Update pathfinding graph to include the new walkable area
            self.game.pathfinding.update_graph()

            # Reset active object
            self.active_object = None
            self.show_interaction_prompt = False


class InteractiveObject(SpriteObject):
    def __init__(self, game, path, pos, interaction_type, door_id=None, code=None,
                 unlocks_door_id=None, requires_code=False, requires_door_id=None):
        # Add 0.5 to position for proper sprite rendering in the center of the tile
        adjusted_pos = (pos[0] + 0.5, pos[1] + 0.5) if isinstance(pos, tuple) else pos
        super().__init__(game, path, adjusted_pos)
        self.interaction_type = interaction_type  # "terminal" or "door"
        self.door_id = door_id  # Unique ID for this door
        self.original_pos = pos  # Store original position for map reference
        self.code = code  # Code displayed by terminal or required by door
        self.unlocks_door_id = unlocks_door_id  # Door ID that this terminal unlocks
        self.requires_code = requires_code  # Whether this door requires a code
        self.requires_door_id = requires_door_id  # Door ID that must be opened first
        self.is_unlocked = False  # Whether this door has been unlocked

    @property
    def map_pos(self):
        # Return the original map position, not the adjusted sprite position
        return self.original_pos if hasattr(self, 'original_pos') else (int(self.x), int(self.y))
