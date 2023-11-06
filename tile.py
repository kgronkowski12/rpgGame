import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self,position,group,sprite_type,surface=pygame.Surface((TILESIZE,TILESIZE))):
        super().__init__(group)
        self.sprite_type = sprite_type
        self.image = surface
        if sprite_type == 'object':
            self.rect = self.image.get_rect(topleft= (position[0],position[1] - TILESIZE)) #odejmujemy tile bo duze obiekty maja 128x64 lub 64x128 wiec 'topleft' jest przesuwany na srodek
        else:
            self.rect = self.image.get_rect(topleft=position) #cały rozmiar
        self.hitbox = self.rect.inflate(0,-10) #stworzenie hitboxu
