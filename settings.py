# geral
WIDTH    = 650
HEIGHT   = 450
FPS      = 60
TILESIZE = 32

# ui 
BAR_HEIGHT = 16
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
UI_FONT = './assets/font/joystix.ttf'
UI_FONT_SIZE = 16
MENU_FONT_SIZE = 24
ITEM_BOX_SIZE = 60

UI_BG_COLOR = '#603038'
UI_BORDER_COLOR = '#4B021E'
UI_FONT_COLOR = '#EEEEEE'
HEALTH_BAR_COLOR = '#F06464'
ENERGY_BAR_COLOR = '#64A9F0'
UI_BORDER_COLOR_ACTIVE = 'gold'

# weapon
weapon_data = {
    'sword': {'cooldown': 100, 'damage': 8}
}

# heal
magic_data = {
    'heal': {'strenght': 20, 'cost': 10}
}
# Enemies
monster_data = {
    'boss':{
            'health': 250, 
            'exp': 20,
            'damage':25, 
            'attack_type':'flame', 
            'attack_sound':'./assets/sound-effects/fireball.wav', 
            'speed':2, 
            'resistance':3,
            'attack_radius':60,
            'notice_radius':200},

    'slime':{
            'health': 80,
            'exp': 20,
            'damage': 10,
            'attack_type':'attack',
            'attack_sound': './assets/sound-effects/slime-attack.wav',
            'speed': 1,
            'resistance': 2,
            'attack_radius': 30,
            'notice_radius': 100}
}   