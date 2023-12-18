from csv import reader
from os import walk
import pygame



WIDTH = 1280
HEIGHT = 720
FPS = 60
TILESIZE = 64

#ui
BAR_WIDTH = 200
BAR_HEIGHT = 16
BOX = 64
FONT_UI = '../img/font/Minecraft.ttf'
FONT_UI_SIZE = 18

#kolory!!!!!!!!!!!!!!!!!
COLOUR_BACKGROUND = '#4DA6FF'
COLOUR_TEXT = 'white'

COLOUR_UI_BG = '#303030'
COLOUR_UI_BORDER = 'black'

#kolory ui
COLOUR_HEALTH = '#800a01'
COLOUR_MANA = '#010a70'

# menu ulepszeń
COLOUR_UPGRADE_BG = 'white'
COLOUR_BAR = 'black'
COLOUR_TEXT_UPGRADE = 'black'

COLOUR_UPGRADE_BG_SELECTED = 'black'
COLOUR_BAR_SELECTED = 'white'
COLOUR_TEXT_SELECTED = 'white'


#pushback to odleglosc na jaka są odrzuceni gdy gracz ich zaatakuje
info_monster = {
	'bear_dog': {'hp': 100, 'damage':20, 'xp':200,'attack_type': 'bite', 'attack_sound':'../sound/attack/slash.wav', 'range_notice': 450, 'range_attack': 70, 'speed': 6, 'pushback': 300},
	'mushroom': {'hp': 100, 'damage':10, 'xp':150,'attack_type': 'cut', 'attack_sound':'../sound/attack/mushroom.wav', 'range_notice': 400 , 'range_attack': 90, 'speed': 4, 'pushback': 200},
	'skeletor': {'hp': 85, 'damage':6, 'xp':125,'attack_type': 'bone', 'attack_sound':'../sound/attack/slash.wav', 'range_notice': 360, 'range_attack': 85, 'speed': 5, 'pushback': 50}}


#bronie
info_weapons = {
	'sword': {'damage': 15,'cooldown': 300, 'graphic':'../img/weapons/sword/full.png'},
	'axe': {'damage': 25, 'cooldown': 650, 'graphic':'../img/weapons/axe/full.png'},
	'sable':{'damage': 5, 'cooldown': 100, 'graphic':'../img/weapons/sable/full.png'}}


#magia
info_magic = {
    'flame': {'strength': 25,'mana_cost': 25,'graphic':'../img/elements/ball/ball.png'},
    'heal': {'strength': 30,'mana_cost': 15,'graphic':'../img/elements/heal/heal.png'},
}

## funkcje do importowania:
def folder_import(path):
    surface_list = []
    for _,__,img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list

def csv_import(path):
    world_csv = []
    with open(path) as world_map:
        layout = reader(world_map,delimiter = ',')
        for row in layout:
            world_csv.append(list(row))
        return world_csv
