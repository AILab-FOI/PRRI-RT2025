"""
Level 3 configuration
"""
from npc import KlonoviNPC, StakorNPC
from levels.base_level import create_base_level_structure

def get_level_data():
    """Return the complete level 3 data"""
    level_data = create_base_level_structure()
    
    # Terminals
    level_data['terminals'] = [
        {
            'position': (5, 5),
            'code': '9999',
            'unlocks_door_id': None
        }
    ]
    
    # Doors
    level_data['doors'] = [
        {
            'position': (11, 10),
            'door_id': 1,
            'requires_code': True,
            'code': '9999'
        }
    ]
    
    # Decorative sprites
    level_data['sprites'] = [
        # Different decorations for level 3 - more intense
        ('ukras1', (7.5, 7.5)),
        ('ukras1', (8.5, 7.5)),
        ('ukras1', (9.5, 7.5)),
        ('ukras1', (10.5, 7.5)),
        ('ukras1', (11.5, 7.5)),
        ('ukras1', (12.5, 7.5)),
        
        ('ukras2', (7.5, 12.5)),
        ('ukras2', (8.5, 12.5)),
        ('ukras2', (9.5, 12.5)),
        ('ukras2', (10.5, 12.5)),
        ('ukras2', (11.5, 12.5)),
        ('ukras2', (12.5, 12.5)),
        
        # Create a pattern in the corners
        ('ukras1', (3.5, 3.5)),
        ('ukras1', (4.5, 3.5)),
        ('ukras1', (3.5, 4.5)),
        
        ('ukras1', (16.5, 3.5)),
        ('ukras1', (17.5, 3.5)),
        ('ukras1', (17.5, 4.5)),
        
        ('ukras1', (3.5, 16.5)),
        ('ukras1', (3.5, 17.5)),
        ('ukras1', (4.5, 17.5)),
        
        ('ukras1', (16.5, 17.5)),
        ('ukras1', (17.5, 16.5)),
        ('ukras1', (17.5, 17.5)),
    ]
    
    # Enemy configuration
    level_data['enemies'] = {
        'count': 10,  # Many enemies in level 3
        'types': [StakorNPC],  # Only StakorNPC in this level
        'weights': [100],  # 100% StakorNPC
        'restricted_area': {(i, j) for i in range(3) for j in range(3)},  # Small restricted area
        'fixed_positions': [(5, 5), (15, 5), (10, 10)]  # Some enemies at fixed positions
    }
    
    # Dialogue NPCs
    level_data['dialogue_npcs'] = [
        {
            'pos': (12.5, 5.5),
            'dialogue_id': 'level3_intro',
            'path': 'resources/sprites/npc/dialogue_npc/0.png'
        }
    ]
    
    return level_data
