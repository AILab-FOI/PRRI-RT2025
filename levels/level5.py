"""
Level 4 configuration
"""
from npc import KlonoviNPC, StakorNPC
from levels.base_level import create_base_level_structure

def get_level_data():
    """Return the complete level 4 data"""
    level_data = create_base_level_structure()
    level_data['narrative'] = {
        'intro': "Ovo je posljednji nivo. Probij se do mosta broda da oslobodiš posadu i završiš svoju misiju.",
        'conclusion': "Brod je tih i ekrani trepere. Arthur stoji na mostu broda, iscrpljen i pun prašine i osušene krvi, dok kraj njega stoji Marvin gledajući ga pogledom čiste ravnodušnosti. Na ekranu titra poruka: 'IDENTIFIKACIJA POTVRĐENA: VI STE SLUŽBENI KAPETAN SVEMIRSKOG BRODA BESMISLENO BEZNAĐE.'"
    }
    
    # Terminals
    level_data['terminals'] = [
        {
            'position': (5, 5),
            'code': '6789',
            'unlocks_door_id': None
        }
    ]
    
    # Doors
    level_data['doors'] = [
        {
            'position': (10, 10),
            'door_id': 1,
            'requires_code': True,
            'code': '6789'
        }
    ]
    
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
    
    # Decorative sprites - unique to level 4
    level_data['sprites'] = [
        # Create a circular pattern in the center
        ('ukras2', (10.5, 10.5)),
        
        # Create a ring around the center
        ('ukras1', (9.5, 9.5)),
        ('ukras1', (10.5, 9.5)),
        ('ukras1', (11.5, 9.5)),
        ('ukras1', (9.5, 10.5)),
        ('ukras1', (11.5, 10.5)),
        ('ukras1', (9.5, 11.5)),
        ('ukras1', (10.5, 11.5)),
        ('ukras1', (11.5, 11.5)),
        
        # Add some decorations along the walls
        ('ukras2', (2.5, 2.5)),
        ('ukras2', (2.5, 17.5)),
        ('ukras2', (17.5, 2.5)),
        ('ukras2', (17.5, 17.5)),
        
        # Add some decorations in the middle of each wall
        ('ukras1', (10.0, 2.5)),
        ('ukras1', (10.0, 17.5)),
        ('ukras1', (2.5, 10.0)),
        ('ukras1', (17.5, 10.0)),
    ]
    
    # Enemy configuration
    level_data['enemies'] = {
        'count': 8,
        'types': [KlonoviNPC, StakorNPC],
        'weights': [40, 60],  # More StakorNPC in this level
        'restricted_area': {(i, j) for i in range(8, 13) for j in range(8, 13)},  # Keep center area clear
        'fixed_positions': [(5, 15), (15, 5)]  # Some enemies at fixed positions
    }
    
    # Dialogue NPCs
    level_data['dialogue_npcs'] = [
        {
            'pos': (5.5, 5.5),
            'dialogue_id': 'level4_intro',
            'path': 'resources/sprites/npc/dialogue_npc/0.png'
        }
    ]
    
    return level_data
