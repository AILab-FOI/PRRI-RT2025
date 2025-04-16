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
        
    ]
    
    # Doors
    level_data['doors'] = [
        
        ##{
        ##    'position': (16, 21),
        ##    'door_id': 3,
        ##    'requires_code': True,
        ##    'code': '4242',  # Uses code from first terminal
        ##    'requires_door_id': 2  # Requires second door to be opened
        ##}
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
    
    # Dialogue NPCs
   ## level_data['dialogue_npcs'] = [
     ##   {
       ##     'pos': (12.5, 5.5),
         ##   'dialogue_id': 'level2_intro',
           ## 'path': 'resources/sprites/npc/dialogue_npc/0.png'
        ##}
    ##]
    
    return level_data
