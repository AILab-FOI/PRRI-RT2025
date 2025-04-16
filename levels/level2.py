"""
Level 2 configuration
"""
from npc import KlonoviNPC, StakorNPC
from levels.base_level import create_base_level_structure

def get_level_data():
    """Return the complete level 2 data"""
    level_data = create_base_level_structure()
    
    # Terminals
    level_data['terminals'] = [
        {
            'position': (47, 17), # Neka pozicija blizu vrata sobe s oružjem (16)
            'code': None,
            'unlocks_door_id': None,
            #'dialogue_id': 'level2_puzzle'
        }
    ]
    
    # Doors
    level_data['doors'] = [
        
        {
            #početna
            'position': (5, 3),
            'door_id': 1,
            'requires_code': False,
            'code': None,  # Uses code from first terminal
            'requires_door_id': None  # Requires second door to be opened
        },
        {
            #soba blizu početka
            'position': (3, 7),
            'door_id': 2,
            'requires_code': False,
            'code': None,  # Uses code from first terminal
            'requires_door_id': None  # Requires second door to be opened
        },
        {
            #srednja soba gornja
            'position': (25, 13),
            'door_id': 3,
            'requires_code': False,
            'code': None,  # Uses code from first terminal
            'requires_door_id': None  # Requires second door to be opened
        },
        {
            #unutarnja soba lijeve sobe
            'position': (7, 17),
            'door_id': 4,
            'requires_code': False,
            'code': None,  # Uses code from first terminal
            'requires_door_id': None  # Requires second door to be opened
        },
        {
            #lijeva soba
            'position': (11, 17),
            'door_id': 5,
            'requires_code': False,
            'code': None,  # Uses code from first terminal
            'requires_door_id': None  # Requires second door to be opened
        },
        {
            #srednja soba lijeva
            'position': (15, 17),
            'door_id': 6,
            'requires_code': False,
            'code': None,  # Uses code from first terminal
            'requires_door_id': None  # Requires second door to be opened
        },
        {
            #srednja soba desna
            'position': (34, 17),
            'door_id': 7,
            'requires_code': False,
            'code': None,  # Uses code from first terminal
            'requires_door_id': None  # Requires second door to be opened
        },
        {
            #desna soba
            'position': (41, 17),
            'door_id': 8,
            'requires_code': False,
            'code': None,  # Uses code from first terminal
            'requires_door_id': None  # Requires second door to be opened
        },
        {
            #unutarnja soba desne sobe
            'position': (47, 16),
            'door_id': 9,
            'requires_code': True,
            'code': '42',  # Uses code from first terminal
            'requires_door_id': None  # Requires second door to be opened
        },
        {
            #srednja soba donja
            'position': (25, 21),
            'door_id': 10,
            'requires_code': False,
            'code': None,  # Uses code from first terminal
            'requires_door_id': None  # Requires second door to be opened
        }
    ]

    level_data['weapons'] = [
        {
            'position': (44, 16),
            'weapon_type': 'smg',
            'path': 'resources/sprites/weapon/puska_stand.png'
        }
    ]

    # Decorative sprites
    level_data['sprites'] = [
        
    ]
    
    # Enemy configuration
    level_data['enemies'] = {
        'count': 6,  # More enemies in level 2
        'types': [KlonoviNPC, StakorNPC],
        'weights': [70, 30],  # More KlonoviNPC in level 2
        'restricted_area': {(i, j) for i in range(5) for j in range(5)},  # Different restricted area
        'fixed_positions': []  # No fixed positions for this level
    }
    
    #Dialogue NPCs
    level_data['dialogue_npcs'] = [
       {
            'pos': (48.2, 15),
            'dialogue_id': 'level2_puzzle',
            'path': 'resources/sprites/npc/dialogue_npc/0.png'
       }
    ]
    
    return level_data
