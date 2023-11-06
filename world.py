import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from post import *
from random import choice

class World:
    def __init__(self):
        #tło
        self.display_surface = pygame.display.get_surface()
        #grupy sprite'ów
        self.visable_sprites = SortByY()
        self.obstacle_sprites = pygame.sprite.Group()
        self.create_world()


    def create_world(self):
        layouts = {
            'world_wall': csv_import('../map/map__Wall.csv'),
            'flowers': csv_import('../map/map__Flowers.csv'),
            'object': csv_import('../map/map__Objects.csv')
        }
        graphics = {
            'flowers': import_folder('../img/flowers'),
            'objects': import_folder('../img/objects')
        }

        #style = world_wall, layout = plik csv
        for style,layout in layouts.items():
            for index_OF_row,row in enumerate(layout):
                for index_OF_column, column in enumerate(row):
                    if column != '-1': #ma rysować granice tylko w polach, które nie są puste (-1), tutaj wartość 395 oznacza granicę
                        #bez tego 'if' cała mapa zostaje uznana za granicę nie do przejścia i gracz automatycznie zostaje wyrzucony z niej
                        x = index_OF_column * TILESIZE
                        y = index_OF_row * TILESIZE
                        if style == 'world_wall':
                            Tile((x,y),[self.obstacle_sprites],'invisible') #self.visable_sprites jako 1 argument sprawi ze granice będą widoczne jako czarne pola
                        if style == 'flowers':
                            random_flowers_image = choice(graphics['flowers'])
                            Tile((x,y),[self.visable_sprites,self.obstacle_sprites],'flowers',random_flowers_image)
                        if style == 'object':
                            #tworzymy plytke typu obiekt
                            surf = graphics['objects'][int(column)]
                            Tile((x,y),[self.visable_sprites,self.obstacle_sprites],'object',surf)

        self.player = Player((2000,1430),[self.visable_sprites],self.obstacle_sprites)
#player idzie do visable sprites a potem dostaje info o obstacle sprites tylko do kolizji

    def run(self):
        #update'ujemy sprite'y co klatkę
        self.visable_sprites.custom_draw(self.player)
        self.visable_sprites.update()
        debug(self.player.status)

class SortByY(pygame.sprite.Group): #będziemy rysować według współrzędnych Y, więc najwyżej położone sprite'y będą na najniższej warstwie (jak w np. photoshopie)
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.width_center = self.display_surface.get_size()[0]//2 #1 atrybut surface czyli szerokosc dzielimy na pol zeby gracz byl zawsze w centrum kamery
        self.height_center = self.display_surface.get_size()[1]//2
        self.shift = pygame.math.Vector2() #vector2 = 2 floaty
        #tworzymy podłogę
        self.floor_surf = pygame.image.load('../img/tiles/map.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

    def custom_draw(self,player):
        self.shift.x = player.rect.centerx - self.width_center #jak bardzo gracz "oddalil" sie od centrum
        self.shift.y = player.rect.centery - self.height_center
        #rysujemy podloge
        floor_shift_position = self.floor_rect.topleft - self.shift
        self.display_surface.blit(self.floor_surf,floor_shift_position)

        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery): #rysujemy według osi Y (więc najpierw rysujemy najwyższe i potem co raz niżej (im niżej tym "wyższa warstwa"))
            shift_position = sprite.rect.topleft - self.shift #przesuniecie sprite'ow o wektor
            self.display_surface.blit(sprite.image,shift_position) #rysowanie jednoczesnie w tej samej pozycji rectangle i obrazka
