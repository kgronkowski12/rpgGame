import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from post import *
from random import choice
from weapon import Weapon
from ui import UI
from enemy import Enemy

class World:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.visable_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.current_attack = None
        self.create_map()
        self.ui = UI()

    def create_map(self):
        layouts = {
            'world_wall': csv_import('../map/map__Wall.csv'),
            'flowers': csv_import('../map/map__Flowers.csv'),
            'object': csv_import('../map/map__Objects.csv'),
            'entities': csv_import('../map/map__Characters.csv')

        }

        graphics = {
            'flowers': import_folder('../img/flowers'),
            'objects': import_folder('../img/objects')
        }

        #style = world_wall, layout = csv file
        for style,layout in layouts.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1': #ma rysować granice tylko w polach, które nie są puste (-1), tutaj wartość 395 oznacza granicę
                        #bez tego 'if' cała mapa zostaje uznana za granicę nie do przejścia i gracz automatycznie zostaje wyrzucony z niej
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'world_wall':
                            Tile((x,y),[self.obstacle_sprites],'invisible') #self.visable_sprites jako 1 argument sprawi ze granice będą widoczne jako czarne pola
                        if style == 'flowers':
                            random_flowers_image = choice(graphics['flowers'])
                            Tile((x,y),[self.visable_sprites,self.obstacle_sprites],'flowers',random_flowers_image)
                        if style == 'object':
                            #create an object tile
                            surf = graphics['objects'][int(col)]
                            Tile((x,y),[self.visable_sprites,self.obstacle_sprites],'object',surf)

                        if style == 'entities':#1 skeletor,2 grzybol, 3 pso niedzwiedz
                            if col == '0':
                                self.player = Player(
                                                    (x,y),
                                                     [self.visable_sprites],
                                                     self.obstacle_sprites,
                                                     self.create_attack,
                                                     self.destroy_attack,
                                                     self.create_magic) 
                            
                            else:
                                Enemy('monster',(x,y),[self.visable_sprites])
                                #create attack bez () bo nie -> call a pass function
                                #player idzie do visable sprites a potem dostaje info o obstacle sprites tylko do kolizji



    def create_attack(self):
        self.current_attack = Weapon(self.player,[self.visable_sprites])


    def create_magic(self,style,strength,cost):
        print(style)
        print(strength)
        print(cost)


    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def run(self):
        self.visable_sprites.custom_draw(self.player)
        self.visable_sprites.update()
        self.ui.display(self.player)

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0]//2 #1 atrybut surface czyli szerokosc dzielimy na pol zeby gracz byl zawsze w centrum kamery
        self.half_height = self.display_surface.get_size()[1]//2
        self.offset = pygame.math.Vector2()
        self.floor_surf = pygame.image.load('../img/tiles/map.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

    def custom_draw(self,player):
        self.offset.x = player.rect.centerx - self.half_width #jak bardzo gracz "oddalil" sie od centrum
        self.offset.y = player.rect.centery - self.half_height
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf,floor_offset_pos)
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery): #rysujemy według osi Y (więc najpierw rysujemy najwyższe i potem co raz niżej (im niżej tym "wyższa warstwa"))
            offset_pos = sprite.rect.topleft - self.offset #przesuniecie sprite'ow o wektor
            self.display_surface.blit(sprite.image,offset_pos) #rysowanie jednoczesnie w tej samej pozycji rectangle i obrazka