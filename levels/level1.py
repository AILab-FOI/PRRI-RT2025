"""
Level 1 configuration
"""
from npc import KlonoviNPC, StakorNPC
from levels.base_level import create_base_level_structure

def get_level_data():
    """Return the complete level 1 data"""
    level_data = create_base_level_structure()

    # Level narrative
    level_data['narrative'] = {
        'intro': "Arthur Dent se budi na hladnom metalnom podu svemirskog broda. Vid mu je mutan a glava mu pulsira. Ne sjeća se ničeg te jedina stvar o kojoj može razmišljati je koliko mu se pije čaj. Iznad njega stoji Marvin, depresivan robot, gledajući ga sa svojim zelenim očima punim besmisla.",
        'objective': "Probij se kroz brod i pronađi izlaz s ovog nivoa."
    }

    # Terminals
    level_data['terminals'] = [
        {
            'position': (2, 14),
            'code': '1337',
            'unlocks_door_id': None  # Terminal doesn't automatically unlock any doors
        }
    ]

    # Doors
    level_data['doors'] = [
        {
            'position': (15, 9),
            'door_id': 1,
            'requires_code': True,
            'code': '1337'  # First door uses code 1337
        },
        {
            'position': (15, 24),
            'door_id': 2,
            'requires_code': True,
            'code': '1337',  # Second door also uses code 1337
            'requires_door_id': 1  # This door requires door 1 to be opened first
        }
    ]

    # Weapon pickups
    level_data['weapons'] = [
        {
            'position': (5, 5),
            'weapon_type': 'smg',
            'path': 'resources/sprites/weapon/puska_stand.png'
        }
    ]

    # Powerups
    level_data['powerups'] = [
        {
            'position': (2, 3.5),
            'powerup_type': 'invulnerability'
        },
        {
            'position': (18, 18),
            'powerup_type': 'invulnerability'
        }
    ]

    # Decorative sprites
    level_data['sprites'] = [
        # Format: (sprite_info, position) where sprite_info can be:
        # - A string (sprite_type) for backward compatibility, using static_sprites folder
        # - A tuple (folder, sprite_type) to specify a folder

        # Using static sprites folder (default)
        ('ukras1', (12.9, 33.5)),
        ('ukras1', (12.2, 33.5)),

        # Using level1 folder
        (('level1', 'powerup'), (1.5, 26.1)),

        # Using static sprites folder
        ('ukras2', (1.9, 26.1)),
        ('ukras2', (2.3, 26.1)),
        ('ukras2', (1.1, 26.5)),
        ('ukras2', (1.1, 27.0)),
        ('ukras2', (1.1, 27.5)),
        ('ukras1', (1.1, 28.0)),
        ('ukras1', (1.1, 28.5)),
        ('ukras1', (1.1, 29.0)),
        ('ukras2', (1.1, 29.5)),
        ('ukras2', (1.1, 30.0)),
        ('ukras2', (1.1, 30.5)),
        ('ukras2', (1.1, 31.0)),
        ('ukras2', (1.1, 31.5)),
        ('ukras1', (1.1, 32.0)),
        ('ukras1', (1.1, 32.5)),
        ('ukras1', (1.5, 32.9)),
        ('ukras1', (1.9, 32.9)),
        ('ukras1', (2.3, 32.9)),

        ('ukras2', (2, 27.0)),
        ('ukras2', (2, 27.5)),
        ('ukras1', (2, 28.0)),
        ('ukras1', (2, 28.5)),
        ('ukras1', (2, 29.0)),
        ('ukras2', (2, 29.5)),
        ('ukras2', (2, 30.0)),
        ('ukras2', (2, 30.5)),
        ('ukras2', (2, 31.0)),
        ('ukras2', (2, 31.5)),
        ('ukras1', (2, 32.0)),

        ('ukras2', (3, 27.0)),
        ('ukras2', (3, 27.5)),
        ('ukras1', (3, 28.0)),
        ('ukras1', (3, 28.5)),
        ('ukras1', (3, 29.0)),
        ('ukras2', (3, 29.5)),
        ('ukras2', (3, 30.0)),
        ('ukras2', (3, 30.5)),
        ('ukras2', (3, 31.0)),
        ('ukras2', (3, 31.5)),
        ('ukras1', (3, 32.0)),

        ('ukras1', (23.2, 31.2)),
        ('ukras1', (23.2, 33.5)),
        # Using static sprites folder
        ('ukras1', (20.2, 31.8)),
        ('ukras1', (15.2, 32.3)),
        ('ukras1', (8.9, 32.3)),

        ('ukras1', (20.2, 12.2)),
        ('ukras2', (20.2, 12.7)),
        ('ukras1', (20.2, 13.2)),
        ('ukras2', (20.2, 13.7)),
        ('ukras1', (20.2, 14.2)),
        ('ukras2', (20.2, 14.7)),

        ('ukras1', (20.8, 12.7)),
        ('ukras1', (21.4, 12.7)),
        ('ukras2', (22, 12.7)),
        ('ukras1', (22.6, 12.7)),

        ('ukras2', (20.8, 13.7)),
        ('ukras1', (21.4, 13.7)),
        ('ukras2', (22, 13.7)),
        ('ukras2', (22.6, 13.7)),

        ('ukras2', (20.8, 14.7)),
        ('ukras1', (21.4, 14.7)),
        ('ukras2', (22, 14.7)),
        ('ukras1', (22.6, 14.7)),

    ]

    # Enemy configuration
    level_data['enemies'] = {
        'count': 4,  # Number of enemies to spawn
        'types': [KlonoviNPC, StakorNPC],  # Types of enemies that can spawn
        'weights': [50, 50],  # Spawn weights for each enemy type
        'restricted_area': {(i, j) for i in range(10) for j in range(10)},  # Areas where enemies cannot spawn
        'fixed_positions': []  # Optional list of fixed positions for enemies: [(x, y), (x, y), ...]
    }

    # Dialogue NPCs
    level_data['dialogue_npcs'] = [
        {
            'pos': (3.5, 2.5),
            'dialogue_id': 'marvin_intro',
            'path': 'resources/sprites/npc/dialogue_npc/0.png'
        }
    ]

    return level_data
