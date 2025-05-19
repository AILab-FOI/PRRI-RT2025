import pygame as pg
import math
from settings import *
from sprite_object import SpriteObject
from weapon import Pistol, SMG, PlasmaGun
from font_manager import load_custom_font

class Interaction:
    def __init__(self, game):
        self.game = game
        self.interaction_objects = []
        self.interaction_distance = 1.5
        self.active_object = None
        self.show_interaction_prompt = False
        self.font = load_custom_font(30)
        self.small_font = load_custom_font(20)
        self.input_code = ""
        self.input_active = False
        self.unlocked_doors = set()
        self.message = ""
        self.message_time = 0
        self.message_duration = 3000

    def add_object(self, obj):
        self.interaction_objects.append(obj)

    def update(self):
        player_pos = self.game.player.pos
        self.active_object = None
        self.show_interaction_prompt = False

        for obj in self.interaction_objects:
            distance = math.hypot(player_pos[0] - obj.x, player_pos[1] - obj.y)
            if distance < self.interaction_distance:
                self.active_object = obj
                self.show_interaction_prompt = True
                break

        if self.message and pg.time.get_ticks() - self.message_time > self.message_duration:
            self.message = ""

    def draw(self):
        if hasattr(self.game, 'intro_sequence') and self.game.intro_sequence.active:
            return

        if self.show_interaction_prompt and not self.input_active:
            # Draw + sign in center
            indicator_size = 15
            line_width = 2
            pg.draw.line(self.game.screen, (255, 255, 255),
                        (HALF_WIDTH - indicator_size, HALF_HEIGHT),
                        (HALF_WIDTH + indicator_size, HALF_HEIGHT), line_width)
            pg.draw.line(self.game.screen, (255, 255, 255),
                        (HALF_WIDTH, HALF_HEIGHT - indicator_size),
                        (HALF_WIDTH, HALF_HEIGHT + indicator_size), line_width)

            # Get appropriate prompt text
            if self.active_object.interaction_type == "level_door":
                # For the last level (level 5), show "Finish the game" instead of "Go to next level"
                if hasattr(self.game, 'level_manager') and self.game.level_manager.current_level == 5:
                    prompt_text = "Press 'E' to finish the game"
                else:
                    prompt_text = "Press 'E' to go to the next level"
            elif self.active_object.interaction_type == "door":
                prompt_text = "Press 'E' to open the door"
            elif self.active_object.interaction_type == "terminal":
                prompt_text = "Press 'E' to access terminal"
            elif self.active_object.interaction_type == "weapon":
                prompt_text = f"Press 'E' to pick up {self.active_object.weapon_type}"
            else:
                prompt_text = f"Press 'E' to {self.active_object.interaction_type}"

            # Draw prompt text
            margin_y = int(HEIGHT * UI_MARGIN_PERCENT_Y)
            text_surface = self.font.render(prompt_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(HALF_WIDTH, HEIGHT - 100 - margin_y))
            self.game.screen.blit(text_surface, text_rect)

        if self.input_active:
            # Draw main background
            bg_width, bg_height = 600, 300
            bg_rect = (HALF_WIDTH - bg_width//2, HALF_HEIGHT - bg_height//2, bg_width, bg_height)

            bg_surface = pg.Surface((bg_width, bg_height), pg.SRCALPHA)
            bg_surface.fill((0, 0, 0, 180))
            self.game.screen.blit(bg_surface, bg_rect[:2])
            pg.draw.rect(self.game.screen, (50, 50, 50), bg_rect, 2)

            # Draw title
            title_surface = self.font.render("Enter Code:", True, (255, 255, 255))
            title_rect = title_surface.get_rect(center=(HALF_WIDTH, HALF_HEIGHT - 100))
            self.game.screen.blit(title_surface, title_rect)

            # Draw input field
            input_text = self.input_code + "_" if len(self.input_code) < 4 else self.input_code
            large_font = load_custom_font(60)

            code_bg_width, code_bg_height = 300, 80
            code_bg = pg.Surface((code_bg_width, code_bg_height), pg.SRCALPHA)
            code_bg.fill((0, 0, 0, 120))
            self.game.screen.blit(code_bg, (HALF_WIDTH - code_bg_width//2, HALF_HEIGHT - code_bg_height//2))

            input_surface = large_font.render(input_text, True, (255, 255, 255))
            input_rect = input_surface.get_rect(center=(HALF_WIDTH, HALF_HEIGHT))
            self.game.screen.blit(input_surface, input_rect)

            # Draw instructions
            instructions = [
                ("Press Enter to confirm", HALF_HEIGHT + 80),
                ("Press Escape to cancel", HALF_HEIGHT + 110)
            ]

            for text, y_pos in instructions:
                instr_surface = self.small_font.render(text, True, (200, 200, 200))
                instr_rect = instr_surface.get_rect(center=(HALF_WIDTH, y_pos))
                self.game.screen.blit(instr_surface, instr_rect)

        if self.message:
            margin_y = int(HEIGHT * UI_MARGIN_PERCENT_Y)
            message_surface = self.font.render(self.message, True, (255, 255, 255))
            message_rect = message_surface.get_rect(center=(HALF_WIDTH, HEIGHT - 150 - margin_y))
            self.game.screen.blit(message_surface, message_rect)

    def handle_key_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_e and self.show_interaction_prompt and not self.input_active:
                self.interact()
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
                if self.active_object.requires_door_id and self.active_object.requires_door_id not in self.unlocked_doors:
                    self.message = f"You need to open door {self.active_object.requires_door_id} first!"
                    self.message_time = pg.time.get_ticks()
                    return

                if self.active_object.requires_code:
                    if self.active_object.is_unlocked or self.active_object.door_id in self.unlocked_doors:
                        self.open_door()
                    else:
                        self.input_active = True
                else:
                    self.open_door()
            elif self.active_object.interaction_type == "level_door":
                if self.active_object.is_level_exit:
                    if hasattr(self.game.object_handler, 'all_enemies_defeated') and self.game.object_handler.all_enemies_defeated:
                        if self.active_object.is_enabled:
                            self.game.next_level()
                        else:
                            self.message = "This door is locked."
                            self.message_time = pg.time.get_ticks()
                    else:
                        self.message = "You must defeat all enemies first!"
                        self.message_time = pg.time.get_ticks()
            elif self.active_object.interaction_type == "weapon":
                self.pickup_weapon()

    def show_terminal_code(self):
        self.message = f"Terminal Code: {self.active_object.code}"
        self.message_time = pg.time.get_ticks()
        self.game.sound.terminal_beep.play()

    def check_code(self):
        correct_code = self.active_object.code

        if self.input_code == correct_code:
            self.active_object.is_unlocked = True
            self.unlocked_doors.add(self.active_object.door_id)
            self.open_door()
        else:
            # Incorrect code - damage the player and play hurt sound
            self.game.player.get_damage(10)  # Apply 10 damage to player
            self.message = "Incorrect code! Security system activated!"
            self.message_time = pg.time.get_ticks()

        self.input_active = False
        self.input_code = ""

    def open_door(self):
        door_pos = self.active_object.map_pos
        if door_pos in self.game.map.world_map:
            del self.game.map.world_map[door_pos]

            if self.active_object in self.game.object_handler.sprite_list:
                self.game.object_handler.sprite_list.remove(self.active_object)

            if self.active_object in self.interaction_objects:
                self.interaction_objects.remove(self.active_object)

            self.message = "Door opened!"
            self.message_time = pg.time.get_ticks()
            self.game.sound.door_open.play()

            self.game.pathfinding.update_graph()

            self.active_object = None
            self.show_interaction_prompt = False


    def pickup_weapon(self):
        weapon_type = self.active_object.weapon_type

        if weapon_type == "smg":
            new_weapon = SMG(self.game)
        elif weapon_type == "plasmagun":
            new_weapon = PlasmaGun(self.game)
        else:
            new_weapon = Pistol(self.game)
            weapon_type = "pistol"

        self.game.level_manager.current_weapon_type = weapon_type
        self.game.weapon = new_weapon
        self.game.sound.weapon_pickup.play()

        self.message = f"Picked up {weapon_type}!"
        self.message_time = pg.time.get_ticks()

        if self.active_object in self.game.object_handler.sprite_list:
            self.game.object_handler.sprite_list.remove(self.active_object)

        if self.active_object in self.interaction_objects:
            self.interaction_objects.remove(self.active_object)

        self.active_object = None
        self.show_interaction_prompt = False


class InteractiveObject(SpriteObject):
    def __init__(self, game, path, pos, interaction_type, door_id=None, code=None,
                 unlocks_door_id=None, requires_code=False, requires_door_id=None,
                 is_level_exit=False, weapon_type=None):
        # Add 0.5 to position for proper sprite rendering in the center of the tile
        adjusted_pos = (pos[0] + 0.5, pos[1] + 0.5) if isinstance(pos, tuple) else pos
        super().__init__(game, path, adjusted_pos)
        self.interaction_type = interaction_type  # "terminal", "door", "level_door", or "weapon"
        self.door_id = door_id  # Unique ID for this door
        self.original_pos = pos  # Store original position for map reference
        self.code = code  # Code displayed by terminal or required by door
        self.unlocks_door_id = unlocks_door_id  # Door ID that this terminal unlocks
        self.requires_code = requires_code  # Whether this door requires a code
        self.requires_door_id = requires_door_id  # Door ID that must be opened first
        self.is_unlocked = False  # Whether this door has been unlocked
        self.is_level_exit = is_level_exit  # Whether this door leads to the next level
        self.is_enabled = False  # Whether this door is enabled (for level exits)
        self.weapon_type = weapon_type  # Type of weapon ("smg", "pistol", etc.)

    @property
    def map_pos(self):
        return self.original_pos
