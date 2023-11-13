import pygame
from settings import *
from entity import Entity
from post import *

class Enemy(Entity):
    def __init__(self,monster_name,pos,groups):
        super().__init__(groups)
        self.sprite_type = 'enemy' #tak samo jak w tile a sam typ jest po to
        #aby mialy rozne wartosci i reakcje, np gracz atakuje wroga (traci zdrowie a potem umiera)
        #gracz atakuje kwiatka (nie ma zycia ale od razu zostaje zniszczone) itp

        self.import_graphics(monster_name)
        self.image = pygame.Surface((64,64))
        self.rect = self.image.get_rect(topleft = pos)

    def import_graphics(self,name): #podobnie jak import player assets z self animations
        self.animations = {'idle':[],'move':[],'attack':[]}
        main_path = f'../img/enemies/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)
            #main path to ta sciezka wyzej, animation to idle/move/attack
            #laczymy je i dostajemy sciezke do konkretnego folderu
            #i potem funkcja import folder daje nam kazde zdjecie w danym folderze
            #i mozna walnac je do naszego słownika