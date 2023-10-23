import pygame
from settings import *
from tile import Tile
from player import Player

class World:
    def __init__(self):
        #tło
        self.display_surface = pygame.display.get_surface()
        #grupy sprite'ów
        self.visable_sprites = SortByY()
        self.obstacle_sprites = pygame.sprite.Group()

        self.create_world()

    def create_world(self):
        for index_OF_row,row in enumerate(WORLD):
            for index_OF_column, column in enumerate(row):
                x = index_OF_column * TILESIZE
                y = index_OF_row * TILESIZE
                if column == 'p':
                    self.player = Player((x,y),[self.visable_sprites],self.obstacle_sprites)
                    #player idzie do visable sprites a potem dostaje info o obstacle sprites tylko do kolizji
                if column == 'x': #w setting znak x w narysowanej mapie odpowiada przeszkodom
                    Tile((x,y),[self.visable_sprites,self.obstacle_sprites])


    def run(self):
        #update'ujemy sprite'y co klatkę
        self.visable_sprites.custom_draw(self.player)
        self.visable_sprites.update()


class SortByY(pygame.sprite.Group): #będziemy rysować według współrzędnych Y, więc najwyżej położone sprite'y będą na najniższej warstwie (jak w np. photoshopie)
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.width_center = self.display_surface.get_size()[0]//2 #1 atrybut surface czyli szerokosc dzielimy na pół zeby gracz byl zawsze w centrum kamery
        self.height_center = self.display_surface.get_size()[1]//2
        self.shift = pygame.math.Vector2() #vector2 = 2 floaty


    def custom_draw(self,player):
        self.shift.x = player.rect.centerx - self.width_center #jak bardzo gracz "oddalil" sie od centrum
        self.shift.y = player.rect.centery - self.height_center

        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            shift_position = sprite.rect.topleft - self.shift #przesuniecie sprite'ow o wektor
            self.display_surface.blit(sprite.image,shift_position) #rysowanie jednoczesnie w tej samej pozycji rectangle i obrazka