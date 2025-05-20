"""
Level 5 configuration
"""
from npc import BossNPC
from levels.base_level import create_base_level_structure

def get_level_data():
    """Return the complete level 5 data"""
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

    # Doors - only keeping the exit door which is handled by level_manager.py
    level_data['doors'] = []

    # Add the plasma gun at the beginning of level 5
    level_data['weapons'] = [
        {
            'position': (14, 5),
            'weapon_type': 'plasmagun',
            'path': 'resources/sprites/weapon/plasma_stand.png'
        }
    ]

    level_data['powerups'] = [
        {
            'position': (6, 11),
            'powerup_type': 'invulnerability'
        },
        {
            'position': (20, 22),
            'powerup_type': 'invulnerability'
        },

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
            {'type': BossNPC, 'position': (13, 17)},  # Boss
        ]
    }

    # Dialogue NPCs
    level_data['dialogue_npcs'] = [
        {
            'pos': (14.5, 31.5),
            'dialogue_id': 'marvin_ending',
            'path': 'resources/sprites/npc/dialogue_npc/0.png'
        }
    ]

    return level_data
