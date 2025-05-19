"""
Level 1 configuration
"""
from npc import KlonoviNPC, StakorNPC, MadracNPC
from levels.base_level import create_base_level_structure

def get_level_data():
    """Return the complete level 5 data"""
    level_data = create_base_level_structure()

    # Level narrative
    

    # Terminals
    level_data['terminals'] = [
        
    ]

    # Doors
    level_data['doors'] = [
        
    ]

    # Weapon pickups
    level_data['weapons'] = [
        {
            'position': (5, 13),
            'weapon_type': 'pistol',
            'path': 'resources/sprites/weapon/puska_stand.png'
        }
    ]

    # Powerups - more powerups for the final level
    level_data['powerups'] = [
        
    ]

    # Decorative sprites - grand finale design
    level_data['sprites'] = [
        
    ]

    # Enemy configuration - challenging final level
    level_data['enemies'] = {
        'count': 0,  # Many enemies in final level
        'types': [KlonoviNPC, StakorNPC, MadracNPC],
        'weights': [30, 30, 40],  # More Madrac enemies in the final level
        'restricted_area': {(i, j) for i in range(9, 12) for j in range(9, 12)},  # Keep center area clear
        'fixed_positions': []  # Strategic enemy positions
    }

    # Dialogue NPCs
    level_data['dialogue_npcs'] = [
        
    ]

    return level_data
