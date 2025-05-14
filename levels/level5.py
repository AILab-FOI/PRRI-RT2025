"""
Level 4 configuration
"""
from npc import BossNPC
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
        #{
            #'position': (5, 5),
            #'code': '6789',
            #'unlocks_door_id': None
        #}
    ]
    
    # Doors
    level_data['doors'] = [
        {
            'position': (7, 14),
            'door_id': 1,
            'requires_code': False,
            'code': None,
            'requires_door_id': None
        },
        {
            'position': (27, 14),
            'door_id': 2,
            'requires_code': False,
            'code': None,
            'requires_door_id': None
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
        
    ]
    
    # Enemy configuration
    level_data['enemies'] = {
        'count': 0,
        'types': [BossNPC],
        'weights': [50, 50],
        'restricted_area': {(i, j) for i in range(10) for j in range(10)},  
        'fixed_positions': [
            {'type': BossNPC, 'position': (17, 14)},  # Boss
        ]
    }
    
    # Dialogue NPCs
    level_data['dialogue_npcs'] = [
        {
            'pos': (3.5, 11.5),
            'dialogue_id': 'level4_intro',
            'path': 'resources/sprites/npc/dialogue_npc/0.png'
        }
    ]
    
    return level_data
