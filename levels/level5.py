"""
Level 5 configuration - Final level
"""
from npc import KlonoviNPC, StakorNPC
from levels.base_level import create_base_level_structure

def get_level_data():
    """Return the complete level 5 data"""
    level_data = create_base_level_structure()
    
    # Terminals
    level_data['terminals'] = [
        {
            'position': (3, 3),
            'code': '0000',
            'unlocks_door_id': None
        },
        {
            'position': (17, 3),
            'code': '1111',
            'unlocks_door_id': None
        },
        {
            'position': (3, 17),
            'code': '2222',
            'unlocks_door_id': None
        }
    ]
    
    # Doors
    level_data['doors'] = [
        {
            'position': (10, 5),
            'door_id': 1,
            'requires_code': True,
            'code': '0000'
        },
        {
            'position': (15, 10),
            'door_id': 2,
            'requires_code': True,
            'code': '1111',
            'requires_door_id': 1
        },
        {
            'position': (10, 15),
            'door_id': 3,
            'requires_code': True,
            'code': '2222',
            'requires_door_id': 2
        }
    ]
    
    # Weapon pickups
    level_data['weapons'] = [
        {
            'position': (5, 5),
            'weapon_type': 'smg',
            'path': 'resources/sprites/weapon/smg/0.png'
        }
    ]
    
    # Powerups - more powerups for the final level
    level_data['powerups'] = [
        {
            'position': (7, 7),
            'powerup_type': 'invulnerability'
        },
        {
            'position': (13, 7),
            'powerup_type': 'invulnerability'
        },
        {
            'position': (7, 13),
            'powerup_type': 'invulnerability'
        },
        {
            'position': (13, 13),
            'powerup_type': 'invulnerability'
        }
    ]
    
    # Decorative sprites - grand finale design
    level_data['sprites'] = [
        # Create an X pattern across the level
        ('ukras2', (5.5, 5.5)),
        ('ukras2', (6.5, 6.5)),
        ('ukras2', (7.5, 7.5)),
        ('ukras2', (8.5, 8.5)),
        ('ukras2', (9.5, 9.5)),
        ('ukras2', (10.5, 10.5)),
        ('ukras2', (11.5, 11.5)),
        ('ukras2', (12.5, 12.5)),
        ('ukras2', (13.5, 13.5)),
        ('ukras2', (14.5, 14.5)),
        
        ('ukras2', (5.5, 14.5)),
        ('ukras2', (6.5, 13.5)),
        ('ukras2', (7.5, 12.5)),
        ('ukras2', (8.5, 11.5)),
        ('ukras2', (9.5, 10.5)),
        ('ukras2', (10.5, 9.5)),
        ('ukras2', (11.5, 8.5)),
        ('ukras2', (12.5, 7.5)),
        ('ukras2', (13.5, 6.5)),
        ('ukras2', (14.5, 5.5)),
        
        # Add decorations in each corner
        ('ukras1', (3.5, 3.5)),
        ('ukras1', (4.5, 3.5)),
        ('ukras1', (3.5, 4.5)),
        
        ('ukras1', (15.5, 3.5)),
        ('ukras1', (16.5, 3.5)),
        ('ukras1', (16.5, 4.5)),
        
        ('ukras1', (3.5, 15.5)),
        ('ukras1', (3.5, 16.5)),
        ('ukras1', (4.5, 16.5)),
        
        ('ukras1', (15.5, 16.5)),
        ('ukras1', (16.5, 15.5)),
        ('ukras1', (16.5, 16.5)),
    ]
    
    # Enemy configuration - challenging final level
    level_data['enemies'] = {
        'count': 15,  # Many enemies in final level
        'types': [KlonoviNPC, StakorNPC],
        'weights': [50, 50],  # Equal mix of both enemy types
        'restricted_area': {(i, j) for i in range(9, 12) for j in range(9, 12)},  # Keep center area clear
        'fixed_positions': [(5, 5), (15, 5), (5, 15), (15, 15), (10, 10)]  # Strategic enemy positions
    }
    
    # Dialogue NPCs
    level_data['dialogue_npcs'] = [
        {
            'pos': (10.5, 3.5),
            'dialogue_id': 'level5_intro',
            'path': 'resources/sprites/npc/dialogue_npc/0.png'
        }
    ]
    
    return level_data
