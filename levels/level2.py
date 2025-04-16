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
        
        {
            #početna
            'position': (5, 3),
            'door_id': 1,
            'requires_code': False,
            #'code': '4242',  # Uses code from first terminal
            #'requires_door_id': 2  # Requires second door to be opened

            #soba blizu početka
            'position': (3, 7),
            'door_id': 2,
            'requires_code': False,
            #'code': '4242',  # Uses code from first terminal
            #'requires_door_id': 2  # Requires second door to be opened

            #srednja soba gornja
            'position': (25, 13),
            'door_id': 3,
            'requires_code': False,
            #'code': '4242',  # Uses code from first terminal
            #'requires_door_id': 2  # Requires second door to be opened

            #unutarnja soba lijeve sobe
            'position': (7, 17),
            'door_id': 4,
            'requires_code': False,
            #'code': '4242',  # Uses code from first terminal
            #'requires_door_id': 2  # Requires second door to be opened

            #lijeva soba
            'position': (10, 17),
            'door_id': 5,
            'requires_code': False,
            #'code': '4242',  # Uses code from first terminal
            #'requires_door_id': 2  # Requires second door to be opened

            #srednja soba lijeva
            'position': (15, 17),
            'door_id': 6,
            'requires_code': False,
            #'code': '4242',  # Uses code from first terminal
            #'requires_door_id': 2  # Requires second door to be opened

            #srednja soba desna
            'position': (34, 17),
            'door_id': 7,
            'requires_code': False,
            #'code': '4242',  # Uses code from first terminal
            #'requires_door_id': 2  # Requires second door to be opened

            #desna soba
            'position': (41, 17),
            'door_id': 8,
            'requires_code': False,
            #'code': '4242',  # Uses code from first terminal
            #'requires_door_id': 2  # Requires second door to be opened

            #unutarnja soba desne sobe
            'position': (47, 16),
            'door_id': 9,
            'requires_code': False,
            #'code': '4242',  # Uses code from first terminal
            #'requires_door_id': 2  # Requires second door to be opened

            #srednja soba donja
            'position': (25, 21),
            'door_id': 10,
            'requires_code': False,
            #'code': '4242',  # Uses code from first terminal
            #'requires_door_id': 2  # Requires second door to be opened
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
    
    # Dialogue NPCs
   ## level_data['dialogue_npcs'] = [
     ##   {
       ##     'pos': (12.5, 5.5),
         ##   'dialogue_id': 'level2_intro',
           ## 'path': 'resources/sprites/npc/dialogue_npc/0.png'
        ##}
    ##]
    
    return level_data
