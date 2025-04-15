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
            'position': (5, 5),
            'code': '4242',
            'unlocks_door_id': None
        },
        {
            'position': (16, 5),
            'code': '8888',
            'unlocks_door_id': None
        }
    ]
    
    # Doors
    level_data['doors'] = [
        {
            'position': (11, 10),
            'door_id': 1,
            'requires_code': True,
            'code': '4242'  # Uses code from first terminal
        },
        {
            'position': (5, 21),
            'door_id': 2,
            'requires_code': True,
            'code': '8888',  # Uses code from second terminal
            'requires_door_id': 1  # Requires first door to be opened
        },
        {
            'position': (16, 21),
            'door_id': 3,
            'requires_code': True,
            'code': '4242',  # Uses code from first terminal
            'requires_door_id': 2  # Requires second door to be opened
        }
    ]
    
    # Decorative sprites
    level_data['sprites'] = [
        # Different decorations for level 2
        ('ukras2', (3.5, 3.5)),
        ('ukras2', (4.5, 3.5)),
        ('ukras2', (5.5, 3.5)),
        
        ('ukras1', (10.5, 3.5)),
        ('ukras1', (11.5, 3.5)),
        ('ukras1', (12.5, 3.5)),
        
        ('ukras2', (18.5, 3.5)),
        ('ukras2', (19.5, 3.5)),
        
        ('ukras1', (3.5, 18.5)),
        ('ukras1', (4.5, 18.5)),
        
        ('ukras2', (18.5, 18.5)),
        ('ukras2', (19.5, 18.5)),
    ]
    
    # Enemy configuration
    level_data['enemies'] = {
        'count': 6,  # More enemies in level 2
        'types': [KlonoviNPC, StakorNPC],
        'weights': [70, 30],  # More KlonoviNPC in level 2
        'restricted_area': {(i, j) for i in range(5) for j in range(5)},  # Different restricted area
        'fixed_positions': []  # No fixed positions for this level
    }
    
    # Dialogue NPCs
    level_data['dialogue_npcs'] = [
        {
            'pos': (12.5, 5.5),
            'dialogue_id': 'level2_intro',
            'path': 'resources/sprites/npc/dialogue_npc/0.png'
        }
    ]
    
    return level_data
