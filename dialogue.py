import pygame as pg
from settings import *
from npc import NPC
from sprite_object import AnimatedSprite
import json
import os
from collections import deque
from font_manager import load_custom_font


class DialogueManager:
    def __init__(self, game):
        self.game = game
        self.dialogues = {}
        self.current_dialogue = None
        self.current_npc = None
        self.current_line_index = 0
        self.dialogue_active = False
        self.last_key_press_time = 0
        self.current_sound = None
        self.sound_playing = False

        self.font = load_custom_font(20)
        self.title_font = load_custom_font(24)
        self.speaker_font = load_custom_font(22)
        self.dialogue_box_height = 200
        self.dialogue_box_padding = 20
        self.line_spacing = 30

        self.speaker_colors = {
            'Marvin': (100, 100, 255),
            'Arthur': (255, 180, 50),
            'Officer': (50, 230, 50)
        }
        self.default_speaker_color = (200, 200, 200)

        self.load_dialogues()

    def load_dialogues(self):
        dialogue_dir = 'resources/dialogues'
        for filename in os.listdir(dialogue_dir):
            if filename.endswith('.json'):
                dialogue_id = filename[:-5]
                file_path = os.path.join(dialogue_dir, filename)
                try:
                    with open(file_path, 'r') as f:
                        self.dialogues[dialogue_id] = json.load(f)
                except Exception as e:
                    print(f"Error loading dialogue {filename}: {e}")

    def start_dialogue(self, dialogue_id, npc):
        if dialogue_id in self.dialogues:
            self.game.player.dialogue_mode = True
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
            pg.mouse.get_rel()

            self.current_dialogue = self.dialogues[dialogue_id]
            self.current_npc = npc
            self.current_line_index = 0
            self.dialogue_active = True

            # Play sound for the first line
            self.play_dialogue_sound()

            return True
        else:
            print(f"Dialogue {dialogue_id} not found")
            return False

    def play_dialogue_sound(self):
        """Play sound for the current dialogue line"""
        if self.current_sound:
            self.current_sound.stop()

        # Dohvati zvuk za trenutnu liniju dijaloga
        dialogue_id = self.get_current_dialogue_id()

        # Dohvati trenutnog govornika
        current_speaker = None
        if "speakers" in self.current_dialogue and self.current_line_index < len(self.current_dialogue["speakers"]):
            current_speaker = self.current_dialogue["speakers"][self.current_line_index]

        # Dohvati zvuk s informacijom o govorniku
        self.current_sound = self.game.sound.get_dialogue_sound(dialogue_id, self.current_line_index, current_speaker)

        # Reproduciraj zvuk samo ako je uspješno učitan
        if self.current_sound:
            self.current_sound.play()
            self.sound_playing = True
        else:
            print(f"No sound to play for {dialogue_id}, line {self.current_line_index}, speaker {current_speaker}")
            self.sound_playing = False

    def get_current_dialogue_id(self):
        """Get the ID of the current dialogue"""
        # Pronađi ID dijaloga iz trenutnog dijaloga
        for dialogue_id, dialogue in self.dialogues.items():
            if dialogue == self.current_dialogue:
                return dialogue_id
        return "unknown"

    def next_line(self):
        if not self.dialogue_active:
            return

        self.current_line_index += 1
        if self.current_line_index >= len(self.current_dialogue["lines"]):
            self.end_dialogue()
            return True
        else:
            # Play sound for the next line
            self.play_dialogue_sound()
        return False

    def end_dialogue(self):
        self.dialogue_active = False
        self.current_dialogue = None
        self.current_npc = None
        self.current_line_index = 0

        # Stop any playing dialogue sound
        if self.current_sound and self.sound_playing:
            self.current_sound.stop()
            self.sound_playing = False
            self.current_sound = None

        pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        pg.mouse.get_rel()
        self.game.player.dialogue_mode = False

    def handle_key_press(self):
        if not self.dialogue_active:
            return

        current_time = pg.time.get_ticks()
        if current_time - self.last_key_press_time > 300:
            self.last_key_press_time = current_time
            if self.current_line_index == len(self.current_dialogue["lines"]) - 1:
                self.end_dialogue()
            else:
                self.next_line()

    def update(self):
        # Check if the current dialogue sound has finished playing
        if self.dialogue_active and self.sound_playing and self.current_sound:
            if not pg.mixer.get_busy():
                self.sound_playing = False

    def draw(self):
        if (hasattr(self.game, 'intro_sequence') and self.game.intro_sequence.active or
            not self.dialogue_active or not self.current_dialogue):
            return

        screen = self.game.screen
        margin_x = int(WIDTH * UI_MARGIN_PERCENT_X)
        margin_y = int(HEIGHT * UI_MARGIN_PERCENT_Y)

        box_width = WIDTH - (margin_x * 4)
        box_height = self.dialogue_box_height
        box_x = (WIDTH - box_width) // 2
        box_y = HEIGHT - box_height - margin_y - 30

        # Draw dialogue box
        dialogue_surface = pg.Surface((box_width, box_height), pg.SRCALPHA)
        dialogue_surface.fill((0, 0, 0, 200))
        screen.blit(dialogue_surface, (box_x, box_y))
        pg.draw.rect(screen, (255, 255, 255), (box_x, box_y, box_width, box_height), 2)

        # Draw speaker name if available
        current_speaker = None
        speaker_color = self.default_speaker_color

        if "speakers" in self.current_dialogue and self.current_line_index < len(self.current_dialogue["speakers"]):
            current_speaker = self.current_dialogue["speakers"][self.current_line_index]
            speaker_color = self.speaker_colors.get(current_speaker, self.default_speaker_color)

        if current_speaker:
            speaker_text = self.speaker_font.render(current_speaker, True, (0, 0, 0))
            speaker_bg_width = speaker_text.get_width() + 30
            speaker_bg_height = speaker_text.get_height() + 12
            speaker_bg_x = box_x + self.dialogue_box_padding
            speaker_bg_y = box_y - speaker_bg_height + 2

            speaker_bg = pg.Surface((speaker_bg_width, speaker_bg_height))
            speaker_bg.fill(speaker_color)

            pg.draw.rect(screen, (0, 0, 0), (speaker_bg_x-2, speaker_bg_y-2, speaker_bg_width+4, speaker_bg_height+4))
            screen.blit(speaker_bg, (speaker_bg_x, speaker_bg_y))

            text_x = speaker_bg_x + (speaker_bg_width - speaker_text.get_width()) // 2
            text_y = speaker_bg_y + (speaker_bg_height - speaker_text.get_height()) // 2
            screen.blit(speaker_text, (text_x, text_y))

        # Draw dialogue text with word wrapping
        if self.current_line_index < len(self.current_dialogue["lines"]):
            line = self.current_dialogue["lines"][self.current_line_index]
            max_width = box_width - 2 * self.dialogue_box_padding

            # Word wrap
            words = line.split(' ')
            lines = []
            current_line = ""

            for word in words:
                test_line = current_line + word + " "
                if self.font.size(test_line)[0] > max_width:
                    lines.append(current_line)
                    current_line = word + " "
                else:
                    current_line = test_line

            if current_line:
                lines.append(current_line)

            # Draw each line
            for i, line in enumerate(lines):
                text_surface = self.font.render(line, True, (255, 255, 255))
                y_pos = box_y + self.dialogue_box_padding + 40 + i * self.line_spacing
                screen.blit(text_surface, (box_x + self.dialogue_box_padding, y_pos))

        # Draw prompt
        is_last_line = self.current_line_index == len(self.current_dialogue["lines"]) - 1
        prompt_text = self.font.render(
            "Press E to exit dialogue..." if is_last_line else "Press E to continue...",
            True, (200, 200, 200)
        )
        prompt_x = box_x + box_width - prompt_text.get_width() - self.dialogue_box_padding
        prompt_y = box_y + box_height - prompt_text.get_height() - self.dialogue_box_padding
        screen.blit(prompt_text, (prompt_x, prompt_y))


class DialogueNPC(NPC):
    def __init__(self, game, path=None, pos=(10.5, 5.5),
                 scale=0.6, shift=0.38, animation_time=180, dialogue_id=None, interaction_radius=2.0):
        if path is None:
            path = 'resources/sprites/npc/dialogue_npc/0.png'

        AnimatedSprite.__init__(self, game, path, pos, scale, shift, animation_time)

        # Basic NPC properties
        self.attack_dist = 0
        self.speed = 0
        self.size = 20
        self.health = 100
        self.attack_damage = 0
        self.accuracy = 0
        self.alive = True
        self.pain = False
        self.ray_cast_value = False
        self.death_frame = 0
        self.player_search_trigger = False
        self.is_friendly = True

        # Set up animations - use current image for animations we don't need
        self.attack_images = self.death_images = self.pain_images = deque([self.image])
        self.idle_images = self.get_images(self.path + '/idle')
        self.walk_images = self.get_images(self.path + '/walk')

        # Dialogue properties
        self.dialogue_id = dialogue_id or "marvin_intro"
        self.interaction_radius = interaction_radius
        self.can_interact = True
        self.interaction_cooldown = 1000
        self.last_interaction_time = 0
        self.interaction_indicator_visible = False

        # Pre-load font for interaction indicator
        self.indicator_font = load_custom_font(16)

    def update(self):
        super().update()

        if self.game.dialogue_manager.dialogue_active:
            self.interaction_indicator_visible = False
            return

        player_dist = ((self.game.player.x - self.x) ** 2 + (self.game.player.y - self.y) ** 2) ** 0.5
        self.interaction_indicator_visible = player_dist <= self.interaction_radius

    def start_dialogue(self):
        if not self.game.dialogue_manager.dialogue_active:
            self.last_interaction_time = pg.time.get_ticks()
            self.game.dialogue_manager.start_dialogue(self.dialogue_id, self)

    def draw_interaction_indicator(self):
        if hasattr(self.game, 'intro_sequence') and self.game.intro_sequence.active:
            return

        if not self.interaction_indicator_visible:
            return

        screen_x = self.screen_x
        screen_y = HALF_HEIGHT - 100
        margin_y = int(HEIGHT * UI_MARGIN_PERCENT_Y)

        text = self.indicator_font.render("Press E to talk", True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen_x, screen_y - 25 - margin_y))

        bg_rect = text_rect.inflate(20, 10)
        bg_surface = pg.Surface((bg_rect.width, bg_rect.height), pg.SRCALPHA)
        bg_surface.fill((0, 0, 0, 180))
        self.game.screen.blit(bg_surface, bg_rect)
        self.game.screen.blit(text, text_rect)

    def run_logic(self):
        if self.alive:
            self.ray_cast_value = self.ray_cast_player_npc()
            self.animate(self.idle_images)

            if self.interaction_indicator_visible:
                self.draw_interaction_indicator()
        else:
            self.animate_death()


def create_dialogue_npcs(game, npc_data):
    npcs = []
    for data in npc_data:
        # Create NPC with parameters from data dict, using defaults if not specified
        npc = DialogueNPC(
            game=game,
            pos=data.get('pos', (10.5, 5.5)),
            dialogue_id=data.get('dialogue_id', 'marvin_intro'),
            path=data.get('path', 'resources/sprites/npc/dialogue_npc/0.png'),
            scale=data.get('scale', 0.6),
            shift=data.get('shift', 0.38),
            animation_time=data.get('animation_time', 180),
            interaction_radius=data.get('interaction_radius', 2.0)
        )
        npcs.append(npc)
        game.object_handler.add_npc(npc)
    return npcs
