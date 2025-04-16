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
        #početna vrata
        (('level2', 'ukras2'), (6.1, 2.9)),
        (('level2', 'ukras2'), (6.1, 4.1)),

        #vrata pored početne sobe
        (('level2', 'ukras2'), (2.9, 8.1)),
        (('level2', 'ukras2'), (4.1, 8.1)),

        #srednja soba 4 stupa
        (('level2', 'ukras1'), (24.9, 16.9)),
        (('level2', 'ukras1'), (26.1, 16.9)),
        (('level2', 'ukras1'), (24.9, 18.1)),
        (('level2', 'ukras1'), (26.1, 18.1)),

        #srednja soba pored gornja vrata
        (('level2', 'ukras2'), (24.9, 14.1)),
        (('level2', 'ukras2'), (26.1, 14.1)),
        #srednja soba pored gornji vrata vanjsko
        (('level2', 'ukras2'), (24.9, 12.9)),
        (('level2', 'ukras2'), (26.1, 12.9)),

        #srednja soba pored desnih vrata
        (('level2', 'ukras2'), (16.1, 16.9)),
        (('level2', 'ukras2'), (16.1, 18.1)),
        #srednja soba pored desnih vrata vanjsko
        (('level2', 'ukras2'), (14.9, 16.9)),
        (('level2', 'ukras2'), (14.9, 18.1)),

        #srednja soba pored lijevih vrata
        (('level2', 'ukras2'), (33.9, 16.9)),
        (('level2', 'ukras2'), (33.9, 18.1)),
        #srednja soba pored lijevih vrata vanjsko
        (('level2', 'ukras2'), (35.1, 16.9)),
        (('level2', 'ukras2'), (35.1, 18.1)),

        #srednja soba donja vrata
        (('level2', 'ukras2'), (24.9, 20.9)),
        (('level2', 'ukras2'), (26.1, 20.9)),
        #srednja soba donja vrata vanjsko
        (('level2', 'ukras2'), (24.9, 22.1)),
        (('level2', 'ukras2'), (26.1, 22.1)),

        #lijeva soba vanjska vrata vanjsko
        (('level2', 'ukras2'), (12.1, 16.9)),
        (('level2', 'ukras2'), (12.1, 18.1)),
        #lijeva soba vanjska vrata
        (('level2', 'ukras2'), (10.9, 16.9)),
        (('level2', 'ukras2'), (10.9, 18.1)),

        #lijeva soba unutarnja vrata vanjsko
        (('level2', 'ukras2'), (8.1, 16.9)),
        (('level2', 'ukras2'), (8.1, 18.1)),
        #lijeva soba unutarnja vrata
        (('level2', 'ukras2'), (6.9, 16.9)),
        (('level2', 'ukras2'), (6.9, 18.1)),

        #desna soba vanjska vrata vanjsko
        (('level2', 'ukras2'), (40.9, 16.9)),
        (('level2', 'ukras2'), (40.9, 18.1)),
        #desna soba vanjska vrata
        (('level2', 'ukras2'), (42.1, 16.9)),
        (('level2', 'ukras2'), (42.1, 18.1)),

        #ukrasi u srednjoj sobi
        (('level2', 'ukras3'), (20.1, 16.1)),
        (('level2', 'ukras3'), (29.9, 16.1)),
        (('level2', 'ukras3'), (20.1, 18.9)),
        (('level2', 'ukras3'), (29.9, 18.9)),

        #hangar
        (('level2', 'ukras1'), (26.9, 43.9)),
        (('level2', 'ukras1'), (26.9, 46.1)),
        (('level2', 'ukras1'), (30.1, 43.9)),
        (('level2', 'ukras1'), (30.1, 46.1)),

        (('level2', 'ukras3'), (18.5, 45.2)),
        (('level2', 'ukras3'), (38.5, 45.2)),
        (('level2', 'ukras3'), (18.5, 45.8)),
        (('level2', 'ukras3'), (38.5, 45.8)),

        (('level2', 'ukras3'), (23.5, 44.5)),
        (('level2', 'ukras3'), (23.5, 45.5)),
        (('level2', 'ukras3'), (33.5, 44.5)),
        (('level2', 'ukras3'), (33.5, 45.5)),

        (('level2', 'ukras3'), (13.5, 44.5)),
        (('level2', 'ukras3'), (13.5, 45.5)),
        (('level2', 'ukras3'), (43.5, 44.5)),
        (('level2', 'ukras3'), (43.5, 45.5)),

        (('level2', 'ukras3'), (8.5, 44.1)),
        (('level2', 'ukras3'), (8.5, 45.9)),
        (('level2', 'ukras3'), (46.5, 44.1)),
        (('level2', 'ukras3'), (46.5, 45.9)),

        #dio nakon početnih vrata
        (('level2', 'ukras3'), (12.5, 6.1)),

        (('level2', 'ukras3'), (11.5, 9.9)),
        (('level2', 'ukras3'), (15.5, 9.9)),

        (('level2', 'ukras3'), (34.5, 9.9)),
        (('level2', 'ukras3'), (41.5, 9.9)),

        (('level2', 'ukras3'), (22.5, 11.1)),
        (('level2', 'ukras3'), (28.5, 11.1)),

        (('level2', 'ukras1'), (43.5, 5.5)),
        (('level2', 'ukras1'), (43.5, 8.5)),
        (('level2', 'ukras1'), (47.5, 5.5)),
        (('level2', 'ukras1'), (47.5, 8.5)),
        (('level2', 'ukras3'), (45.5, 7)),

        #lijevi hodnik
        (('level2', 'ukras3'), (12.1, 12.9)),
        (('level2', 'ukras3'), (14.9, 12.9)),
        (('level2', 'ukras3'), (12.1, 22.1)),
        (('level2', 'ukras3'), (14.9, 22.1)),
        #desni hodnik
        (('level2', 'ukras3'), (35.1, 12.9)),
        (('level2', 'ukras3'), (40.9, 12.9)),
        (('level2', 'ukras3'), (35.1, 22.1)),
        (('level2', 'ukras3'), (40.9, 22.1)),

        #dugi hodnik nakon srednje sobe
        (('level2', 'ukras2'), (5.1, 23.9)),
        (('level2', 'ukras2'), (7.1, 23.9)),
        (('level2', 'ukras2'), (9.1, 23.9)),
        (('level2', 'ukras2'), (11.1, 23.9)),
        (('level2', 'ukras2'), (13.1, 23.9)),
        (('level2', 'ukras2'), (15.1, 23.9)),
        (('level2', 'ukras2'), (17.1, 23.9)),
        (('level2', 'ukras2'), (19.1, 23.9)),
        (('level2', 'ukras2'), (21.1, 23.9)),

        (('level2', 'ukras2'), (29.9, 23.9)),
        (('level2', 'ukras2'), (31.9, 23.9)),
        (('level2', 'ukras2'), (33.9, 23.9)),
        (('level2', 'ukras2'), (35.9, 23.9)),
        (('level2', 'ukras2'), (37.9, 23.9)),
        (('level2', 'ukras2'), (39.9, 23.9)),
        (('level2', 'ukras2'), (41.9, 23.9)),
        (('level2', 'ukras2'), (43.9, 23.9)),

        (('level2', 'ukras2'), (5.1, 25.1)),
        (('level2', 'ukras2'), (7.1, 25.1)),
        (('level2', 'ukras2'), (9.1, 25.1)),
        (('level2', 'ukras2'), (11.1, 25.1)),
        (('level2', 'ukras2'), (13.1, 25.1)),
        (('level2', 'ukras2'), (15.1, 25.1)),
        (('level2', 'ukras2'), (17.1, 25.1)),
        (('level2', 'ukras2'), (19.1, 25.1)),
        (('level2', 'ukras2'), (21.1, 25.1)),

        (('level2', 'ukras2'), (29.9, 25.1)),
        (('level2', 'ukras2'), (31.9, 25.1)),
        (('level2', 'ukras2'), (33.9, 25.1)),
        (('level2', 'ukras2'), (35.9, 25.1)),
        (('level2', 'ukras2'), (37.9, 25.1)),
        (('level2', 'ukras2'), (39.9, 25.1)),
        (('level2', 'ukras2'), (41.9, 25.1)),
        (('level2', 'ukras2'), (43.9, 25.1)),

        #hodnik nakon artificijalnih vrata
        
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
            'pos': (48.8, 14.3),
            'dialogue_id': 'level2_puzzle',
            'path': 'resources/sprites/npc/dialogue_npc/0.png'
       }
    ]
    
    return level_data
