WIDTH = 1280
HEIGHT = 720
FPS = 60
TILESIZE = 64

#ui
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = '../img/font/Minecraft.ttf'
UI_FONT_SIZE = 18

#kolory
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

#kolory ui
HEALTH_COLOR = '#800a01'
ENERGY_COLOR = '#010a70'
UI_BORDER_COLOR_ACTIVE = 'gold'


#bronie
weapon_data = {
	'sword': {'cooldown': 100, 'damage': 15,'graphic':'../img/weapons/sword/full.png'},
	'axe': {'cooldown': 300, 'damage': 20, 'graphic':'../img/weapons/axe/full.png'},
	'sable':{'cooldown': 50, 'damage': 8, 'graphic':'../img/weapons/sable/full.png'}}


#magia
magic_data = {
    'flame': {'strength': 5,'cost': 20,'graphic':'../img/elements/ball/ball.png'},
    'heal': {'strength': 20,'cost': 10,'graphic':'../img/elements/heal/heal.png'},
}


#wrogowie;  resistence to odleglosc na jaka są odrzuceni gdy gracz ich zaatakuje
monster_data = {
	'bear_dog': {'health': 100,'exp':100,'damage':20,'attack_type': 'bite', 'attack_sound':'../sound/attack/bite.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
	'mushroom': {'health': 100,'exp':110,'damage':8,'attack_type': 'cut', 'attack_sound':'../sound/attack/mushroom.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350},
	'skeletor': {'health': 70,'exp':120,'damage':6,'attack_type': 'bone', 'attack_sound':'../sound/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300}}
