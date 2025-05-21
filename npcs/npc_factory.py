"""
NPC Factory for creating NPCs with appropriate configurations.
"""

from npcs.enemy_npcs import (
    KlonoviNPC,
    StakorNPC,
    TosterNPC,
    ParazitNPC,
    JazavacNPC,
    MadracNPC,
    BossNPC
)
from npcs.dialogue_npc import DialogueNPC


class NPCFactory:

    NPC_TYPES = {
        'klonovi': KlonoviNPC,
        'stakor': StakorNPC,
        'toster': TosterNPC,
        'parazit': ParazitNPC,
        'jazavac': JazavacNPC,
        'madrac': MadracNPC,
        'dialogue': DialogueNPC,
        'boss': BossNPC
    }

    @staticmethod
    def create_npc(game, npc_type, pos, **kwargs):
        if npc_type in NPCFactory.NPC_TYPES:
            npc_class = NPCFactory.NPC_TYPES[npc_type]
            return npc_class(game, pos=pos, **kwargs)
        return None

    @staticmethod
    def create_enemy_group(game, enemy_types, weights, count, valid_positions):
        from random import choices, shuffle

        if not enemy_types or not valid_positions:
            return []

        if len(enemy_types) != len(weights):
            weights = [1] * len(enemy_types)

        npc_classes = []
        for enemy_type in enemy_types:
            if enemy_type in NPCFactory.NPC_TYPES:
                npc_classes.append(NPCFactory.NPC_TYPES[enemy_type])

        if not npc_classes:
            return []

        shuffle(valid_positions)

        npcs = []
        for i in range(min(count, len(valid_positions))):
            x, y = valid_positions[i]
            npc_class = choices(npc_classes, weights[:len(npc_classes)])[0]
            npc = npc_class(game, pos=(x + 0.5, y + 0.5))
            npcs.append(npc)

        return npcs
