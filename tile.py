import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self,position,group):
        super().__init__(group)
        self.image = pygame.image.load('../img/test/rock.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=position) #cały rozmiar
        self.hitbox = self.rect.inflate(0,-10) #hitbox będzie mniejszy niż postać (taki jakby mniejszy prostokąt w centrum, pierwsza wspolrzedna sie nie zmienia
        #wiec hitbox dotyka boków sprite'a aleee nie góry/dołu)
