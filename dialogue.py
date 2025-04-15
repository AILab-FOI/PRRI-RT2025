import pygame as pg
from settings import *
from npc import NPC
import json
import os
from font_manager import load_custom_font


class DialogueManager:
    """
    Manages all dialogues in the game.
    Loads dialogue data from JSON files and provides access to dialogues.
    """
    def __init__(self, game):
        self.game = game
        self.dialogues = {}
        self.current_dialogue = None
        self.current_npc = None
        self.current_line_index = 0
        self.dialogue_active = False

        # UI settings
        self.font = load_custom_font(20)
        self.title_font = load_custom_font(24)
        self.speaker_font = load_custom_font(22)
        self.dialogue_box_height = 200
        self.dialogue_box_padding = 20
        self.line_spacing = 30

        # Speaker colors
        self.speaker_colors = {
            'Marvin': (150, 150, 255),  # Light blue for Marvin
            'Arthur': (255, 200, 100),  # Orange-yellow for Arthur
            'Officer': (100, 255, 100)  # Green for other characters
        }
        self.default_speaker_color = (255, 255, 255)  # White for unknown speakers

        # Load dialogues
        self.load_dialogues()

    def load_dialogues(self):
        """Load all dialogue files from the dialogues directory"""
        dialogue_dir = 'resources/dialogues'

        # Create directory if it doesn't exist
        if not os.path.exists(dialogue_dir):
            os.makedirs(dialogue_dir)
            # Create a sample dialogue file
            self._create_sample_dialogue()

        # Load all JSON files in the dialogues directory
        for filename in os.listdir(dialogue_dir):
            if filename.endswith('.json'):
                dialogue_id = filename[:-5]
                file_path = os.path.join(dialogue_dir, filename)
                try:
                    with open(file_path, 'r') as f:
                        self.dialogues[dialogue_id] = json.load(f)
                except Exception as e:
                    print(f"Error loading dialogue {filename}: {e}")

    def _create_sample_dialogue(self):
        """Create a sample dialogue file if none exist"""
        sample_dialogue = {
            "npc_name": "Marvin",
            "lines": [
                "Hello, I'm Marvin, the Paranoid Android.",
                "Who are you?",
                "Life? Don't talk to me about life.",
                "That sounds depressing.",
                "I've been talking to the ship's computer.",
                "And?",
                "It hates me."
            ],
            "speakers": [
                "Marvin",
                "Arthur",
                "Marvin",
                "Arthur",
                "Marvin",
                "Arthur",
                "Marvin"
            ]
        }

        file_path = os.path.join('resources/dialogues', 'marvin_intro.json')
        with open(file_path, 'w') as f:
            json.dump(sample_dialogue, f, indent=4)

    def start_dialogue(self, dialogue_id, npc):
        """Start a dialogue with the given ID"""
        if dialogue_id in self.dialogues:
            # First disable player movement to prevent any unwanted camera movement
            self.game.player.dialogue_mode = True

            # Reset mouse position to center of screen
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
            pg.mouse.get_rel()  # Clear any accumulated mouse movement

            # Set up the dialogue
            self.current_dialogue = self.dialogues[dialogue_id]
            self.current_npc = npc
            self.current_line_index = 0
            self.dialogue_active = True

            return True
        else:
            print(f"Dialogue {dialogue_id} not found")
            return False

    def next_line(self):
        """Advance to the next line of dialogue"""
        if not self.dialogue_active:
            return

        self.current_line_index += 1
        if self.current_line_index >= len(self.current_dialogue["lines"]):
            self.end_dialogue()
            return True
        return False

    def end_dialogue(self):
        """End the current dialogue"""
        self.dialogue_active = False
        self.current_dialogue = None
        self.current_npc = None
        self.current_line_index = 0

        pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        pg.mouse.get_rel()
        self.game.player.dialogue_mode = False

    def handle_key_press(self):
        """Handle key press for dialogue advancement"""
        if not self.dialogue_active:
            return

        current_time = pg.time.get_ticks()

        # Store the last key press time as an attribute if it doesn't exist
        if not hasattr(self, 'last_key_press_time'):
            self.last_key_press_time = 0

        # Add cooldown to prevent multiple advances on a single key press
        if current_time - self.last_key_press_time > 300:
            self.last_key_press_time = current_time

            # If we're on the last line, pressing E will end the dialogue
            if self.current_line_index == len(self.current_dialogue["lines"]) - 1:
                self.end_dialogue()
            else:
                # Otherwise, advance to the next line
                self.next_line()

    def update(self):
        """Update the dialogue system"""
        if not self.dialogue_active:
            return

    def draw(self):
        """Draw the dialogue UI"""
        if not self.dialogue_active or not self.current_dialogue:
            return

        screen = self.game.screen

        # Calculate dialogue box dimensions
        box_width = WIDTH - 200
        box_height = self.dialogue_box_height
        box_x = (WIDTH - box_width) // 2
        box_y = HEIGHT - box_height - 50

        # Draw semi-transparent background
        dialogue_surface = pg.Surface((box_width, box_height), pg.SRCALPHA)
        dialogue_surface.fill((0, 0, 0, 200))
        screen.blit(dialogue_surface, (box_x, box_y))

        # Draw border
        pg.draw.rect(screen, (255, 255, 255), (box_x, box_y, box_width, box_height), 2)

        # Get current speaker if available
        current_speaker = None
        speaker_color = self.default_speaker_color

        if "speakers" in self.current_dialogue and self.current_line_index < len(self.current_dialogue["speakers"]):
            current_speaker = self.current_dialogue["speakers"][self.current_line_index]
            speaker_color = self.speaker_colors.get(current_speaker, self.default_speaker_color)

        # Draw speaker name with colored background if available
        if current_speaker:
            # Create a background for the speaker name
            speaker_text = self.speaker_font.render(current_speaker, True, (255, 255, 255))
            speaker_bg_width = speaker_text.get_width() + 20
            speaker_bg_height = speaker_text.get_height() + 10
            speaker_bg_x = box_x + self.dialogue_box_padding
            speaker_bg_y = box_y - speaker_bg_height // 2

            # Draw speaker background
            speaker_bg = pg.Surface((speaker_bg_width, speaker_bg_height), pg.SRCALPHA)
            speaker_bg.fill((speaker_color[0], speaker_color[1], speaker_color[2], 200))
            screen.blit(speaker_bg, (speaker_bg_x, speaker_bg_y))

            # Draw speaker name
            screen.blit(speaker_text, (speaker_bg_x + 10, speaker_bg_y + 5))

        # Draw current dialogue line
        if self.current_line_index < len(self.current_dialogue["lines"]):
            line = self.current_dialogue["lines"][self.current_line_index]

            # Word wrap the text
            words = line.split(' ')
            lines = []
            current_line = ""

            for word in words:
                test_line = current_line + word + " "
                # If adding this word would exceed the width, start a new line
                if self.font.size(test_line)[0] > box_width - 2 * self.dialogue_box_padding:
                    lines.append(current_line)
                    current_line = word + " "
                else:
                    current_line = test_line

            # Add the last line
            if current_line:
                lines.append(current_line)

            # Draw each line
            for i, line in enumerate(lines):
                text_surface = self.font.render(line, True, (255, 255, 255))
                y_pos = box_y + self.dialogue_box_padding + 40 + i * self.line_spacing
                screen.blit(text_surface, (box_x + self.dialogue_box_padding, y_pos))

        # Draw continue/exit prompt based on whether this is the last line
        if self.current_line_index == len(self.current_dialogue["lines"]) - 1:
            prompt_text = self.font.render("Press E to exit dialogue...", True, (200, 200, 200))
        else:
            prompt_text = self.font.render("Press E to continue...", True, (200, 200, 200))

        prompt_x = box_x + box_width - prompt_text.get_width() - self.dialogue_box_padding
        prompt_y = box_y + box_height - prompt_text.get_height() - self.dialogue_box_padding
        screen.blit(prompt_text, (prompt_x, prompt_y))


class DialogueNPC(NPC):
    """
    An NPC that can engage in dialogue with the player.
    Extends the base NPC class with dialogue capabilities.
    """
    def __init__(self, game, path=None, pos=(10.5, 5.5),
                 scale=0.6, shift=0.38, animation_time=180, dialogue_id=None, interaction_radius=2.0):
        # Use a default path if none is provided
        if path is None:
            # Try to use a friendly NPC sprite, or fall back to a default
            path = 'resources/sprites/npc/dialogue_npc/0.png'

        # Initialize the NPC with the path
        super().__init__(game, path, pos, scale, shift, animation_time)

        # Dialogue properties
        self.dialogue_id = dialogue_id or "marvin_intro"  # Default to Marvin's intro dialogue
        self.interaction_radius = interaction_radius
        self.can_interact = True
        self.interaction_cooldown = 1000  # ms
        self.last_interaction_time = 0

        # Override NPC properties to make it non-hostile
        self.attack_dist = 0
        self.health = 100
        self.attack_damage = 0
        self.speed = 0
        self.accuracy = 0

        # Mark as friendly NPC - this will be used to exclude it from enemy counts
        self.is_friendly = True

        # Visual indicator for interaction
        self.interaction_indicator_visible = False

    def update(self):
        """Update the dialogue NPC"""
        super().update()

        # Skip interaction handling if dialogue is already active
        if self.game.dialogue_manager.dialogue_active:
            self.interaction_indicator_visible = False
            return

        # Check if player is within interaction radius
        player_dist = ((self.game.player.x - self.x) ** 2 + (self.game.player.y - self.y) ** 2) ** 0.5

        # Show interaction indicator if player is close enough
        self.interaction_indicator_visible = player_dist <= self.interaction_radius

    def start_dialogue(self):
        """Start dialogue with this NPC"""
        if not self.game.dialogue_manager.dialogue_active:
            # Update the last interaction time
            self.last_interaction_time = pg.time.get_ticks()
            # Start the dialogue
            self.game.dialogue_manager.start_dialogue(self.dialogue_id, self)

    def draw_interaction_indicator(self):
        """Draw an indicator showing the player can interact with this NPC"""
        if not self.interaction_indicator_visible:
            return

        # Calculate screen position
        screen_x = self.screen_x
        screen_y = HALF_HEIGHT - 100

        # Circular indicator removed

        # Draw "Press E to talk" text with background
        font = load_custom_font(16)  # Smaller size for this text
        text = font.render("Press E to talk", True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen_x, screen_y - 25))

        # Draw text background
        bg_rect = text_rect.inflate(20, 10)
        bg_surface = pg.Surface((bg_rect.width, bg_rect.height), pg.SRCALPHA)
        bg_surface.fill((0, 0, 0, 180))  # Semi-transparent black
        self.game.screen.blit(bg_surface, bg_rect)

        # Draw text
        self.game.screen.blit(text, text_rect)

    def run_logic(self):
        """Override the NPC logic to be non-hostile"""
        if self.alive:
            self.ray_cast_value = self.ray_cast_player_npc()

            # Don't attack or chase the player
            self.animate(self.idle_images)

            # Draw interaction indicator if visible
            if self.interaction_indicator_visible:
                self.draw_interaction_indicator()
        else:
            self.animate_death()


# Helper function to create dialogue NPCs for a level
def create_dialogue_npcs(game, npc_data):
    """
    Create dialogue NPCs for a level based on the provided data.

    npc_data should be a list of dictionaries with the following keys:
    - pos: tuple (x, y) - Position of the NPC
    - dialogue_id: str - ID of the dialogue to use
    - path: str (optional) - Path to the NPC sprite
    - scale: float (optional) - Scale of the NPC sprite
    - shift: float (optional) - Height shift of the NPC sprite
    """
    npcs = []

    for data in npc_data:
        # Extract required parameters
        pos = data.get('pos', (10.5, 5.5))
        dialogue_id = data.get('dialogue_id', 'marvin_intro')

        # Extract optional parameters with defaults
        path = data.get('path', 'resources/sprites/npc/dialogue_npc/0.png')
        scale = data.get('scale', 0.6)
        shift = data.get('shift', 0.38)
        animation_time = data.get('animation_time', 180)
        interaction_radius = data.get('interaction_radius', 2.0)

        # Create the NPC
        npc = DialogueNPC(
            game=game,
            path=path,
            pos=pos,
            scale=scale,
            shift=shift,
            animation_time=animation_time,
            dialogue_id=dialogue_id,
            interaction_radius=interaction_radius
        )

        npcs.append(npc)

        # Add to game's object handler
        game.object_handler.add_npc(npc)

    return npcs
