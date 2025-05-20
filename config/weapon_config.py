# Pistol Configuration
# Role: Starting weapon that provides reliable, accurate damage against single targets
PISTOL_CONFIG = {
    'name': 'pistol',
    'path': 'resources/sprites/weapon/pistol/0.png',
    'scale': 0.22,
    'animation_time': 200,  # Lower = faster firing rate
    'damage': 30,  # Damage per shot (30 damage requires ~3-4 shots for standard 100 HP enemy)
    'accuracy': 0.95,  # High precision with minimal spread (not currently used but prepared for future implementation)
    'auto_fire': False,  # Whether the weapon can be fired automatically by holding the mouse button
    'sound': 'pistolj',  # Sound effect to play when firing
    'description': 'Standard issue sidearm. Reliable and accurate.'
}

# SMG (Submachine Gun) Configuration
# Role: Rapid-fire weapon for crowd control and high burst damage at close range
SMG_CONFIG = {
    'name': 'smg',
    'path': 'resources/sprites/weapon/smg/0.png',
    'scale': 1.2,
    'animation_time': 70,  # Lower = faster firing rate
    'damage': 15,  # Lower per-shot damage than pistol
    'accuracy': 0.75,  # Less accurate than pistol (not currently used but prepared for future implementation)
    'auto_fire': True,  # Can be fired automatically by holding the mouse button
    'auto_fire_delay': 70,  # Lower = faster auto-fire rate
    'sound': 'smg',  # Sound effect to play when firing
    'right_offset': 230,  # Horizontal offset for weapon positioning
    'description': 'Rapid-fire weapon ideal for close quarters combat.'
}

# Plasma Gun Configuration
# Role: Ultimate weapon with high damage and fast fire rate for the final level
PLASMA_GUN_CONFIG = {
    'name': 'plasmagun',
    'path': 'resources/sprites/weapon/plasmagun/0.png',
    'scale': 0.5,
    'animation_time': 325,  # Fastest fire rate of all weapons
    'damage': 50,  # Highest damage per shot
    'accuracy': 0.9,  # High accuracy
    'auto_fire': False,  # Can be fired automatically by holding the mouse button
    #'auto_fire_delay': 200,  # Delay between auto-fired shots in milliseconds
    'sound': 'plasmagun',  # Sound effect to play when firing
    'right_offset': 200,  # Horizontal offset for weapon positioning
    'description': 'Advanced plasma weapon with devastating firepower.'
}

# Dictionary mapping weapon names to their configurations
WEAPON_CONFIGS = {
    'pistol': PISTOL_CONFIG,
    'smg': SMG_CONFIG,
    'plasmagun': PLASMA_GUN_CONFIG,
}

def get_weapon_config(weapon_name):
    return WEAPON_CONFIGS.get(weapon_name.lower())
