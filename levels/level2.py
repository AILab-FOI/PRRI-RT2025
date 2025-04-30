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
            'position': (5, 2),
            'door_id': 1,
            'requires_code': False,
            'code': None,  # Uses code from first terminal
            'requires_door_id': None  # Requires second door to be opened
        },
        {
            #soba blizu početka
            'position': (3, 6),
            'door_id': 2,
            'requires_code': False,
            'code': None,  # Uses code from first terminal
            'requires_door_id': None  # Requires second door to be opened
        },
        {
            #srednja soba gornja
            'position': (15, 12),
            'door_id': 3,
            'requires_code': False,
            'code': None,  # Uses code from first terminal
            'requires_door_id': None  # Requires second door to be opened
        },
        {
            #unutarnja soba lijeve sobe
            'position': (4, 16),
            'door_id': 4,
            'requires_code': False,
            'code': None,  # Uses code from first terminal
            'requires_door_id': None  # Requires second door to be opened
        },
        #{
        #    #lijeva soba
        #    'position': (7, 16),
        #    'door_id': 5,
        #    'requires_code': False,
        #    'code': None,  # Uses code from first terminal
        #    'requires_door_id': None  # Requires second door to be opened
        #},
        {
            #srednja soba lijeva
            'position': (10, 16),
            'door_id': 6,
            'requires_code': False,
            'code': None,  # Uses code from first terminal
            'requires_door_id': None  # Requires second door to be opened
        },
        {
            #srednja soba desna
            'position': (20, 16),
            'door_id': 7,
            'requires_code': False,
            'code': None,  # Uses code from first terminal
            'requires_door_id': None  # Requires second door to be opened
        },
        #{
        #    #desna soba
        #    'position': (23, 16),
        #    'door_id': 8,
        #    'requires_code': False,
        #    'code': None,  # Uses code from first terminal
        #    'requires_door_id': None  # Requires second door to be opened
        #},
        {
            #unutarnja soba desne sobe
            'position': (29, 16),
            'door_id': 9,
            'requires_code': True,
            'code': '42',  # Uses code from first terminal
            'requires_door_id': None  # Requires second door to be opened
        },
        {
            #srednja soba donja
            'position': (15, 20),
            'door_id': 10,
            'requires_code': False,
            'code': None,  # Uses code from first terminal
            'requires_door_id': None  # Requires second door to be opened
        }
    ]

    level_data['weapons'] = [
        {
            'position': (26, 15),
            'weapon_type': 'smg',
            'path': 'resources/sprites/weapon/puska_stand.png'
        }
    ]

    # Decorative sprites
    level_data['sprites'] = [
        #POČETAK
        #početna vrata
        (('level2', 'ukras2'), (6.1, 1.9)),
        (('level2', 'ukras2'), (6.1, 3.1)),

        #vrata pored početne sobe
        (('level2', 'ukras2'), (2.9, 7.1)),
        (('level2', 'ukras2'), (4.1, 7.1)),

        #dio nakon početnih vrata
        (('level2', 'ukras3'), (11.5, 5.1)),

        #pocetak mape skroz desno odjeljak
        (('level2', 'ukras1'), (27.9, 4.5)),
        (('level2', 'ukras1'), (30.1, 4.5)),
        (('level2', 'ukras1'), (27.9, 6.5)),
        (('level2', 'ukras1'), (30.1, 6.5)),
        (('level2', 'ukras3'), (29.1, 5.5)),


        #SREDNJA SOBA
        #srednja soba 4 stupa
        (('level2', 'ukras1'), (14.9, 15.9)),
        (('level2', 'ukras1'), (16.1, 15.9)),
        (('level2', 'ukras1'), (14.9, 17.1)),
        (('level2', 'ukras1'), (16.1, 17.1)),

        #srednja soba pored gornja vrata
        (('level2', 'ukras2'), (14.9, 13.1)),
        (('level2', 'ukras2'), (16.1, 13.1)),

        #srednja soba pored gornji vrata vanjsko
        (('level2', 'ukras2'), (14.9, 11.9)),
        (('level2', 'ukras2'), (16.1, 11.9)),

        #srednja soba pored lijevih vrata
        (('level2', 'ukras2'), (11.1, 15.9)),
        (('level2', 'ukras2'), (11.1, 17.1)),

        #srednja soba pored lijevih vrata vanjsko
        (('level2', 'ukras2'), (9.9, 15.9)),
        (('level2', 'ukras2'), (9.9, 17.1)),

        #srednja soba pored desnih vrata
        (('level2', 'ukras2'), (19.9, 15.9)),
        (('level2', 'ukras2'), (19.9, 17.1)),

        #srednja soba pored desnih vrata vanjsko
        (('level2', 'ukras2'), (21.1, 15.9)),
        (('level2', 'ukras2'), (21.1, 17.1)),

        #srednja soba donja vrata
        (('level2', 'ukras2'), (14.9, 19.9)),
        (('level2', 'ukras2'), (16.1, 19.9)),

        #srednja soba donja vrata vanjsko
        (('level2', 'ukras2'), (14.9, 21.1)),
        (('level2', 'ukras2'), (16.1, 21.1)),

        #ukrasi u srednjoj sobi
        (('level2', 'ukras3'), (14.1, 15.1)),
        (('level2', 'ukras3'), (16.9, 15.1)),
        (('level2', 'ukras3'), (14.1, 17.9)),
        (('level2', 'ukras3'), (16.9, 17.9)),


        #LIJEVA SOBA
        #lijeva soba vanjska vrata vanjsko
        #(('level2', 'ukras2'), (8.1, 15.9)),
        #(('level2', 'ukras2'), (8.1, 17.1)),

        #lijeva soba vanjska vrata
        #(('level2', 'ukras2'), (6.9, 15.9)),
        #(('level2', 'ukras2'), (6.9, 17.1)),

        #lijeva soba unutarnja vrata vanjsko
        (('level2', 'ukras2'), (5.1, 15.9)),
        (('level2', 'ukras2'), (5.1, 17.1)),

        #lijeva soba unutarnja vrata
        (('level2', 'ukras2'), (3.9, 15.9)),
        (('level2', 'ukras2'), (3.9, 17.1)),


        #DESNA SOBA
        #desna soba vanjska vrata vanjsko
        #(('level2', 'ukras2'), (22.9, 15.9)),
        #(('level2', 'ukras2'), (22.9, 17.1)),

        #desna soba vanjska vrata
        #(('level2', 'ukras2'), (24.1, 15.9)),
        #(('level2', 'ukras2'), (24.1, 17.1)),
      

        #PROLAZI
        
        #prvi prolaz ulaz
        (('level2', 'ukras3'), (7.5, 8.9)),
        (('level2', 'ukras3'), (10.5, 8.9)),

        #drugi prolaz ulaz
        (('level2', 'ukras3'), (12.5, 8.9)),
        (('level2', 'ukras3'), (18.5, 8.9)),

        #treći prolaz ulaz
        (('level2', 'ukras3'), (26.5, 8.9)),
        (('level2', 'ukras3'), (29.5, 8.9)),

        #prvi prolaz izlaz
        (('level2', 'ukras3'), (12.5, 10.1)),
        (('level2', 'ukras3'), (18.5, 10.1)),

        #drugi prolaz izlaz
        (('level2', 'ukras3'), (7.5, 10.1)),
        (('level2', 'ukras3'), (10.5, 10.1)),

        #treći prolaz izlaz
        (('level2', 'ukras3'), (26.5, 10.1)),
        (('level2', 'ukras3'), (29.5, 10.1)),

        #LIJEVI HODNIK
        #ulaz lijevi hodnik
        #(('level2', 'ukras3'), (7.5, 11.9)),
        (('level2', 'ukras3'), (10.5, 11.9)),

        #izlaz lijevi hodnik
        #(('level2', 'ukras3'), (7.5, 21.1)),
        (('level2', 'ukras3'), (10.5, 21.1)),


        #DESNO HODNIK
        #ulaz desni hodnik
        (('level2', 'ukras3'), (20.5, 11.9)),
        #(('level2', 'ukras3'), (23.5, 11.9)),

        #izlaz desni hodnik
        (('level2', 'ukras3'), (20.5, 21.1)),
        #(('level2', 'ukras3'), (23.5, 21.1)),


        #DUGI HODNIK NAKON SREDNJE SOBE
        #lijevi zid gornji dio
        (('level2', 'ukras2'), (3.1, 22.9)),
        (('level2', 'ukras2'), (5.1, 22.9)),
        (('level2', 'ukras2'), (7.1, 22.9)),
        (('level2', 'ukras2'), (9.1, 22.9)),
        (('level2', 'ukras2'), (11.1, 22.9)),
        (('level2', 'ukras2'), (13.1, 22.9)),

        #desni zid gornji dio
        (('level2', 'ukras2'), (17.9, 22.9)),
        (('level2', 'ukras2'), (19.9, 22.9)),
        (('level2', 'ukras2'), (21.9, 22.9)),
        (('level2', 'ukras2'), (23.9, 22.9)),
        (('level2', 'ukras2'), (25.9, 22.9)),
        (('level2', 'ukras2'), (27.9, 22.9)),

        #lijevi zid donji dio
        (('level2', 'ukras2'), (3.1, 24.1)),
        (('level2', 'ukras2'), (5.1, 24.1)),
        (('level2', 'ukras2'), (7.1, 24.1)),
        (('level2', 'ukras2'), (9.1, 24.1)),
        (('level2', 'ukras2'), (11.1, 24.1)),
        (('level2', 'ukras2'), (13.1, 24.1)),

        #desni zid donji dio
        (('level2', 'ukras2'), (17.9, 24.1)),
        (('level2', 'ukras2'), (19.9, 24.1)),
        (('level2', 'ukras2'), (21.9, 24.1)),
        (('level2', 'ukras2'), (23.9, 24.1)),
        (('level2', 'ukras2'), (25.9, 24.1)),
        (('level2', 'ukras2'), (27.9, 24.1)),


        #ARTIFICIJALNA VRATA
        #ulaz
        (('level2', 'ukras2'), (12.5, 26.9)),
        (('level2', 'ukras2'), (13.5, 26.9)),
        (('level2', 'ukras2'), (17.5, 26.9)),
        (('level2', 'ukras2'), (18.5, 26.9)),


        #HODNIK NAKON ARTIFICIJALNIH VRATA SLIJEPE ULICE
        #lijevo
        (('level2', 'ukras1'), (1.5, 27.5)),
        (('level2', 'ukras1'), (11.5, 27.5)),
        
        #desno
        (('level2', 'ukras1'), (19.5, 27.5)),
        (('level2', 'ukras1'), (30.5, 27.5)),


        #ZADNJI VEĆI ZID NA MAPI
        #gornji dio
        (('level2', 'ukras2'), (10.9, 30.9)),
        (('level2', 'ukras2'), (12.9, 30.9)),
        (('level2', 'ukras2'), (14.9, 30.9)),
        (('level2', 'ukras2'), (16.9, 30.9)),
        (('level2', 'ukras2'), (18.9, 30.9)),
        (('level2', 'ukras2'), (20.9, 30.9)),
        (('level2', 'ukras2'), (22.9, 30.9)),
        (('level2', 'ukras2'), (24.9, 30.9)),
        (('level2', 'ukras2'), (26.9, 30.9)),

        #donji dio
        (('level2', 'ukras2'), (10.9, 33.1)),
        (('level2', 'ukras2'), (12.9, 33.1)),
        (('level2', 'ukras2'), (14.9, 33.1)),
        (('level2', 'ukras2'), (16.9, 33.1)),
        (('level2', 'ukras2'), (18.9, 33.1)),
        (('level2', 'ukras2'), (20.9, 33.1)),
        (('level2', 'ukras2'), (22.9, 33.1)),
        (('level2', 'ukras2'), (24.9, 33.1)),
        (('level2', 'ukras2'), (26.9, 33.1)),


        #ZAVRŠNA VRATA
        (('level2', 'ukras2'), (30.9, 32.9)),
        (('level2', 'ukras2'), (30.9, 34.1))
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
            'pos': (30.8, 12.3),
            'dialogue_id': 'level2_puzzle',
            'path': 'resources/sprites/npc/dialogue_npc/0.png'
       }
    ]
    
    return level_data
