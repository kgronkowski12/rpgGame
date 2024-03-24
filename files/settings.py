import pygame
from csv import reader
from os import walk

all_sprites = pygame.sprite.Group()

WIDTH = 1280
HEIGHT = 720
TILESIZE = 64
FPS = 60
#kolory!!!!!!!!!!!!!!!!!
COLOUR_BACKGROUND = '#4DA6FF'
COLOUR_TEXT = 'white'
COLOUR_UI_BG = '#303030'
COLOUR_UI_BORDER = 'black'

# menu ulepszeń
COLOUR_UPGRADE = 'white'
COLOUR_BAR = 'black'
COLOUR_TEXT_UPGRADE = 'black'

COLOUR_UPGRADE_SELECTED = 'black'
COLOUR_BAR_SELECTED = 'white'
COLOUR_TEXT_SELECTED = 'white'

#kolory ui
COLOUR_HEALTH = '#800a01'
COLOUR_MANA = '#010a70'

#user interface
FONT = '../img/font/Minecraft.ttf'
FONT_SIZE = 18
BAR_WIDTH = 200
BAR_HEIGHT = 16
BOX = 64

coinCount = 0



FROGGO_MAX_LEVEL = {'hp':500,'mana':200,'attack':15,'spells':15,"speed":15}

#pushback to odleglosc na jaka są odrzuceni gdy gracz ich zaatakuje
INFO_MONSTER = {
	'bear_dog': {'hp': 100, 'damage':20, 'xp':200,'attack_type': 'bite', 'attack_sound':'../sound/attacks/bear_dog.wav', 'range_notice': 450, 'range_attack': 70, 'speed': 6, 'pushback': 300},
	'mushroom': {'hp': 100, 'damage':10, 'xp':150,'attack_type': 'cut', 'attack_sound':'../sound/attacks/mushroom.wav', 'range_notice': 400 , 'range_attack': 90, 'speed': 5, 'pushback': 200},
    'mimic': {'hp': 85, 'damage':6, 'xp':125,'attack_type': 'bite', 'attack_sound':'../sound/attacks/skeletor.wav', 'range_notice': 200, 'range_attack': 85, 'speed': 3, 'pushback': 50},
	'skeletor': {'hp': 85, 'damage':6, 'xp':125,'attack_type': 'bone', 'attack_sound':'../sound/attacks/skeletor.wav', 'range_notice': 350, 'range_attack': 85, 'speed': 5, 'pushback': 50}}


#bronie
INFO_WEAPONS = {
	'sword': {'damage': 15,'cooldown': 500, 'graphic':'../img/weapons/sword/full.png'},
	'axe': {'damage': 25, 'cooldown': 750, 'graphic':'../img/weapons/axe/full.png'},
	'sable':{'damage': 5, 'cooldown': 250, 'graphic':'../img/weapons/sable/full.png'}}


#magia
INFO_SPELLS = {
    'energy_ball': {'strength': 25,'mana_cost': 25,'graphic':'../img/elements/ball/ball.png'},
    'heal': {'strength': 30,'mana_cost': 15,'graphic':'../img/elements/heal/heal.png'},
    'shield': {'strength': 30,'mana_cost': 15,'graphic':'../img/weapons/shieldIcon.png'},
}

## funkcje do importowania:
def folder_import(location):
    list = []
    for _,__,files in walk(location):
        for item in files:
            folder = location + '/' + item
            img = pygame.image.load(folder)
            list.append(img)
    return list

def csv_import(location):
    world_csv = []
    with open(location) as world_map:
        layout = reader(world_map,delimiter = ',')
        for row in layout:
            world_csv.append(list(row))
        return world_csv
