"""
Level 2 configuration
"""
from npc import StakorNPC
from levels.base_level import create_base_level_structure

def get_level_data():
    """Return the complete level 2 data"""
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
            'code': '8332',
            'unlocks_door_id': None,  # Terminal doesn't automatically unlock any doors
            #'dialogue_id': None
        }
    ]

    # Doors
    level_data['doors'] = [
        {
            'position': (15, 9),
            'door_id': 1,
            'requires_code': True,
            'code': '8332'
        },
        {
            'position': (15, 24),
            'door_id': 2,
            'requires_code': True,
            'code': '8332',
            'requires_door_id': 1  # This door requires door 1 to be opened first
        }
    ]

    # Weapon pickups - removed for level 1
    level_data['weapons'] = []

    # Powerups - removed for level 1
    level_data['powerups'] = []

    # Decorative sprites
    level_data['sprites'] = [
        # Format: (sprite_info, position) where sprite_info can be:
        # - A string (sprite_type) for backward compatibility, using static_sprites folder
        # - A tuple (folder, sprite_type) to specify a folder

        # Using static sprites folder (default)
        ## pored vrata
        (('level2', 'ukras2'), (12.9, 33.5)),
        (('level2', 'ukras2'), (12.1, 33.5)),

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

        ## donji desni kut
        (('level2', 'ukras2'), (23.2, 33.5)),

        # po mapi 3. sektor


        (('level2', 'ukras2'), (8.9, 33.8)),

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
        'count': 25,  # Number of enemies to spawn - infestacija stakora
        'types': [StakorNPC],  # Types of enemies that can spawn
        'weights': [100],  # Equal spawn weights for each enemy type
        'restricted_area': {(i, j) for i in range(10) for j in range(10)},  # Areas where enemies cannot spawn
        'fixed_positions': []
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
