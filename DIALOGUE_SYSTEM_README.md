# Dialogue System Documentation

This document explains how to use the dialogue system to add story-telling NPCs to your game.

## Overview

The dialogue system allows you to create NPCs that players can interact with to receive information, story elements, or instructions. These NPCs are non-hostile and will display dialogue when the player approaches them and presses the E key.

## How to Add New Dialogue NPCs

### 1. Create a Dialogue File

Dialogue files are stored in the `resources/dialogues/` directory as JSON files. Each file contains the dialogue for a specific NPC or conversation.

Example dialogue file structure (`resources/dialogues/example.json`):

```json
{
    "npc_name": "Character Name",
    "lines": [
        "This is the first line of dialogue.",
        "This is the second line of dialogue.",
        "This is the third line of dialogue.",
        "Press E to continue or exit the conversation."
    ]
}
```

### 2. Add the NPC to a Level

To add a dialogue NPC to a level, modify the level data in the `initialize_levels` method in the `LevelManager` class in `level_manager.py`:

```python
# In level_manager.py, inside the initialize_levels method

# Level 1 data
self.level_data[1] = {
    # ... other level data ...

    # Dialogue NPCs for level 1
    'dialogue_npcs': [
        {
            'pos': (3.5, 2.5),  # Position in the map (x, y)
            'dialogue_id': 'guide',  # Must match the JSON filename without extension
            'path': 'resources/sprites/npc/dialogue_npc/0.png'  # Sprite path
        }
    ]
}

# Level 2 data
self.level_data[2] = {
    # ... other level data ...

    # Dialogue NPCs for level 2
    'dialogue_npcs': [
        {
            'pos': (12.5, 5.5),
            'dialogue_id': 'level2_intro',
            'path': 'resources/sprites/npc/dialogue_npc/0.png'
        }
    ]
}
```

The dialogue NPCs are automatically created when a level is loaded through the `setup_dialogue_npcs` method in the `LevelManager` class.

### 3. Optional Parameters

When adding a dialogue NPC, you can customize several parameters:

- `pos`: (required) The position of the NPC in the map (x, y)
- `dialogue_id`: (required) The ID of the dialogue file (without .json extension)
- `path`: (optional) Path to the NPC sprite
- `scale`: (optional) Scale of the NPC sprite (default: 0.6)
- `shift`: (optional) Height shift of the NPC sprite (default: 0.38)
- `animation_time`: (optional) Animation time in milliseconds (default: 180)
- `interaction_radius`: (optional) Radius within which the player can interact with the NPC (default: 2.0)

Example with all parameters:

```python
{
    'pos': (3.5, 2.5),
    'dialogue_id': 'guide',
    'path': 'resources/sprites/npc/dialogue_npc/0.png',
    'scale': 0.7,
    'shift': 0.4,
    'animation_time': 200,
    'interaction_radius': 2.5
}
```

## Dialogue System Features

1. **Interactive NPCs**: NPCs show an interaction indicator when the player is nearby
2. **Multi-line Dialogues**: Support for multiple lines of dialogue that the player can navigate through
3. **Pause Gameplay**: When in dialogue mode, player movement and shooting are disabled
4. **Visual Feedback**: Clear visual indicators for when dialogue is available and active
5. **Easy to Extend**: Simple JSON format makes it easy to add new dialogues
6. **Non-Hostile NPCs**: Dialogue NPCs are marked as friendly and don't count toward enemy totals
7. **Smooth Camera Handling**: The system properly handles mouse position to prevent camera jumps
8. **Clear Exit Indication**: The last dialogue line shows a prompt to exit the dialogue

## NPC Sprite Structure

For dialogue NPCs, the following sprite structure is recommended:

```
resources/sprites/npc/dialogue_npc/
├── 0.png (main sprite)
├── idle/
│   ├── 0.png
│   ├── 1.png
│   └── ...
└── death/
    ├── 0.png
    ├── 1.png
    └── ...
```

## Modifying Existing Dialogues

To modify an existing dialogue:

1. Navigate to the `resources/dialogues/` directory
2. Open the JSON file for the dialogue you want to modify (e.g., `guide.json`)
3. Edit the `npc_name` or `lines` array as needed
4. Save the file

Changes will take effect the next time the game is started or when the level is reloaded.

### Example: Modifying the Guide Dialogue

Original `guide.json`:
```json
{
    "npc_name": "Guide",
    "lines": [
        "Welcome to the game! I'm here to guide you.",
        "You need to defeat all enemies to progress to the next level.",
        "Good luck on your journey!"
    ]
}
```

Modified `guide.json`:
```json
{
    "npc_name": "Tutorial Guide",
    "lines": [
        "Welcome to the game! I'm here to help you get started.",
        "Use WASD to move and mouse to look around.",
        "Left-click to shoot and press SPACE to dash.",
        "You need to defeat all enemies to progress to the next level.",
        "Good luck on your journey, brave warrior!"
    ]
}
```

## Tips for Writing Effective Dialogue

1. **Keep it Brief**: Players don't want to read walls of text
2. **Break it Up**: Split long explanations into multiple dialogue lines
3. **Character Voice**: Give each NPC a distinct personality and way of speaking
4. **Progressive Disclosure**: Reveal information gradually as the player progresses
5. **Contextual Relevance**: Make sure the dialogue is relevant to the player's current situation
6. **Provide Guidance**: Use dialogue to teach game mechanics and provide hints
7. **Add Personality**: Make NPCs memorable with unique speech patterns or quirks

## How to Use the Dialogue System

### Player Interaction

1. **Starting a Dialogue**: Approach a dialogue NPC and press the E key when the interaction indicator appears
2. **Advancing Dialogue**: Press the E key to advance to the next line of dialogue
3. **Ending a Dialogue**: When on the last line of dialogue, press the E key to exit the conversation

### Technical Implementation

The dialogue system uses event-based handling for key presses and is organized as follows:

1. **Level Data**: Dialogue NPC data is stored in the level data in `level_manager.py`
2. **NPC Creation**: The `setup_dialogue_npcs` method in `LevelManager` creates dialogue NPCs for each level
3. **Event Handling**: Key events are processed in the main game loop in `main.py`
4. **Interaction Flow**: When the E key is pressed:
   - If a dialogue is active, it advances or ends the dialogue
   - If no dialogue is active, it checks if the player is near a dialogue NPC and starts a dialogue if possible
5. **Core Components**:
   - The `DialogueManager` class handles dialogue loading, display, and navigation
   - The `DialogueNPC` class extends the base NPC class with dialogue capabilities
   - The `create_dialogue_npcs` function in `dialogue.py` creates NPC instances from data

## Troubleshooting

- If an NPC doesn't appear, check that the dialogue file exists and has the correct format
- If the dialogue doesn't display, ensure the dialogue_id in the NPC definition matches the JSON filename
- If sprites don't appear correctly, verify the path to the sprite files is correct
- If dialogue interaction doesn't work, ensure the E key event is being properly handled in `main.py`
- If the dialogue doesn't end, check that the dialogue file has at least one line of text
- If the camera jumps after dialogue, verify that the mouse position reset is working correctly
