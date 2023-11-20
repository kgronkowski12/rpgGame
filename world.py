import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from post import *
from random import choice, randint
from weapon import Weapon
from ui import UI
from enemy import Enemy
from elements import AnimationPlayer

class World:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.visable_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group() #bronie i magia
        self.attackable_sprites = pygame.sprite.Group() # wrogowie
        #sprawdzamy kolizje miedzy attack a atackable
        self.create_map()
        self.ui = UI()
        self.animation_player = AnimationPlayer()

    def create_map(self):
        layouts = {
            'world_wall': import_csv_layout('../map/map__Wall.csv'),
            'flowers': import_csv_layout('../map/map__Flowers.csv'),
            'object': import_csv_layout('../map/map__Objects.csv'),
            'entities': import_csv_layout('../map/map__Characters.csv')

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
                            Tile((x,y),
                                 [self.visable_sprites,self.obstacle_sprites,self.attackable_sprites],
                                 'flowers',random_flowers_image)
                        if style == 'object':
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
                                if col == '1': monster_name = 'skeletor'
                                elif col == '2': monster_name = 'mushroom'
                                elif col == '3': monster_name = 'bear_dog'
                                Enemy(monster_name,
                                      (x,y),
                                      [self.visable_sprites,self.attackable_sprites], #grupy 'sprite'ów' do jakich należą wrogowie
                                      self.obstacle_sprites,
                                      self.damage_player,
                                      self.trigger_death_particles)
                                #player idzie do visable sprites a potem dostaje info o obstacle sprites tylko do kolizji



    def create_attack(self):
        self.current_attack = Weapon(self.player,[self.visable_sprites,self.attack_sprites])


    def create_magic(self,style,strength,cost):
        print(style)
        print(strength)
        print(cost)


    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None


    def player_attack_logic(self): #przejdziemy przez wszystkie sprite atakow i sprawdzimy czy jakis z nich koliduje z attackable sprite'm
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite,self.attackable_sprites,False)
                #sprawdzamy kolizje miedzy pierwszym argumentem a drugim i na drugim wykonujemy trzeci (DOKILL), nie chcemy zabijac wiec zostawiamy na false 
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'flowers':
                            pos = target_sprite.rect.center #particles ida tam gdzie wczesniej byly kwiaty
                            offset = pygame.math.Vector2(0,75) #lekko przenosimy particles, czy usunac???
                            for leaf in range(randint(3,6)):
                                self.animation_player.create_grass_particles(pos-offset,[self.visable_sprites])
                            target_sprite.kill() #niszczymy kwiaty
                        else:
                            target_sprite.get_damage(self.player,attack_sprite.sprite_type)



    def damage_player(self,amount,attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_particles(attack_type,self.player.rect.center,[self.visable_sprites])


    def trigger_death_particles(self,pos,particle_type):
        self.animation_player.create_particles(particle_type,pos,self.visable_sprites)


    def run(self):
        self.visable_sprites.custom_draw(self.player)
        self.visable_sprites.update()
        self.visable_sprites.enemy_update(self.player)
        self.player_attack_logic()
        self.ui.display(self.player)

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0]//2 #1 atrybut surface czyli szerokosc dzielimy na pol zeby gracz byl zawsze w centrum kamery
        self.half_height = self.display_surface.get_size()[1]//2
        self.offset = pygame.math.Vector2()

        #creating the floor
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


    def enemy_update(self,player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy'] #hasattr sprawdza czy wystepuje atrybut sprite_type po to by nie wystepowal error dla kazdego ktory go nie ma
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
