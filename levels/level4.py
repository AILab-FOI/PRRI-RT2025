"""
Level 4 configuration
"""
from npc import MadracNPC, ParazitNPC, TosterNPC
from levels.base_level import create_base_level_structure

def get_level_data():
    """Return the complete level 3 data"""
    level_data = create_base_level_structure()

    # Terminals
    level_data['terminals'] = [
        #{
            #'position': (5, 5),
            #'code': '9999',
            #'unlocks_door_id': None
        #}
    ]
    level_data['powerups'] = [
        {
            'position': (24, 27),
            'powerup_type': 'invulnerability'
        },
        {
            'position': (10, 27),
            'powerup_type': 'invulnerability'
        },
    ]

    # Doors
    level_data['doors'] = [

        {
            #glavna vrata prema mini bosss
            'position': (17, 21),
            'door_id': 1,
            'requires_code': False,
            'code': None,
            'requires_door_id': None
        },

        #prvi lijevi hodnik
        {
            #prva vrata desno
            'position': (10, 4),
            'door_id': 2,
            'requires_code': False,
            'code': None,
            'requires_door_id': None
        },
        {
            #druga vrata desno
            'position': (4, 4),
            'door_id': 3,
            'requires_code': False,
            'code': None,
            'requires_door_id': None
        },
        {
            #prva vrata lijevo
            'position': (6, 7),
            'door_id': 4,
            'requires_code': False,
            'code': None,
            'requires_door_id': None
        },
        {
            #druga vrata lijevo
            'position': (3, 7),
            'door_id': 5,
            'requires_code': False,
            'code': None,
            'requires_door_id': None
        },

        #prvi desni hodnik
        {
            #prva vrata lijevo
            'position': (24, 4),
            'door_id': 6,
            'requires_code': False,
            'code': None,
            'requires_door_id': None
        },
        {
            #druga vrata lijevo
            'position': (30, 4),
            'door_id': 7,
            'requires_code': False,
            'code': None,
            'requires_door_id': None
        },
        {
            #prva vrata desno
            'position': (28, 7),
            'door_id': 8,
            'requires_code': False,
            'code': None,
            'requires_door_id': None
        },
        {
            #druga vrata desno
            'position': (31, 7),
            'door_id': 9,
            'requires_code': False,
            'code': None,
            'requires_door_id': None
        },

        #drugi lijevi hodnik
        {
            #prva vrata desno
            'position': (10, 12),
            'door_id': 10,
            'requires_code': False,
            'code': None,
            'requires_door_id': None
        },
        {
            #prva vrata lijevo
            'position': (10, 15),
            'door_id': 11,
            'requires_code': False,
            'code': None,
            'requires_door_id': None
        },
        {
            #druga vrata lijevo
            'position': (4, 15),
            'door_id': 12,
            'requires_code': False,
            'code': None,
            'requires_door_id': None
        },

        #drugi desni hodnik
        {
            #prva vrata lijevo
            'position': (24, 12),
            'door_id': 13,
            'requires_code': False,
            'code': None,
            'requires_door_id': None
        },
        {
            #prva vrata desno
            'position': (24, 15),
            'door_id': 14,
            'requires_code': False,
            'code': None,
            'requires_door_id': None
        },
        {
            #druga vrata desno
            'position': (30, 15),
            'door_id': 15,
            'requires_code': False,
            'code': None,
            'requires_door_id': None
        },

    ]

    # Decorative sprites
    level_data['sprites'] = [

    ]

    # Enemy configuration
    level_data['enemies'] = {
        'count': 10,
        'types': [TosterNPC, MadracNPC],
        'weights': [50, 50],
        'restricted_area': {
            #*{(i, j) for i in range(10) for j in range(10)
            *{(i, j) for i in range(15, 20) for j in range(6)}
            },  # Larger restricted area like in level 1
        'fixed_positions': [
            {'type': ParazitNPC, 'position': (17, 27)},  # Miniboss Parazit in the arena area
        ]
    }

    # Dialogue NPCs
    level_data['dialogue_npcs'] = [
        #{
            #'pos': (12.5, 5.5),
            #'dialogue_id': 'level3_intro',
            #'path': 'resources/sprites/npc/dialogue_npc/0.png'
        #}
    ]

    # Powerups in the arena area
    level_data['powerups'] = [
        {
            'position': (10, 27),
            'powerup_type': 'invulnerability'
        },
        {
            'position': (24, 27),
            'powerup_type': 'invulnerability'
        },
        {
            'position': (14, 31),
            'powerup_type': 'invulnerability'
        },
        {
            'position': (20, 31),
            'powerup_type': 'invulnerability'
        },
        {
            'position': (17, 32),
            'powerup_type': 'invulnerability'
        }
    ]

    return level_data
