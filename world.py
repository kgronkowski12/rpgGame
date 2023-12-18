import pygame
from settings import *
from player import Player
from random import choice
from combat import *
from ui import UI
from enemy import Enemy
from elements import AnimationMaker
from upgrade import Upgrade

class Tile(pygame.sprite.Sprite):
    def __init__(self,position,group,label_sprite,surface=pygame.Surface((TILESIZE,TILESIZE))):
        super().__init__(group)
        self.label_sprite = label_sprite
        self.image = surface
        if label_sprite == 'object':
            self.rect = self.image.get_rect(topleft= (position[0],position[1] - TILESIZE)) #odejmujemy tile bo duze obiekty maja 128x64 lub 64x128 wiec 'topleft' jest przesuwany na srodek
        else:
            self.rect = self.image.get_rect(topleft=position) #cały rozmiar

        self.hitbox = self.rect.inflate(0,-10) #stworzenie hitboxu

class World:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False
        self.visable_sprites = SortByY()
        self.obstacle_sprites = pygame.sprite.Group()
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group() #bronie i magia
        self.attackable_sprites = pygame.sprite.Group() # wrogowie
        self.create_world()
        self.ui = UI()
        self.upgrade = Upgrade(self.player)

        #elementy
        self.animation_player = AnimationMaker()
        self.magic_player = MagicPlayer(self.animation_player)

    def create_world(self):
        layouts = {
            'world_wall': csv_import('../map/map__Wall.csv'),
            'flowers': csv_import('../map/map__Flowers.csv'),
            'object': csv_import('../map/map__Objects.csv'),
            'entities': csv_import('../map/map__Characters.csv')

        }

        graphics = {
            'flowers': folder_import('../img/flowers'),
            'objects': folder_import('../img/objects')
        }

        #style = world_wall, layout = csv file
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
                            Tile((x,y),
                                 [self.visable_sprites,self.obstacle_sprites,self.attackable_sprites],
                                 'flowers',random_flowers_image)
                        if style == 'object':
                            #create an object tile
                            surf = graphics['objects'][int(column)]
                            Tile((x,y),[self.visable_sprites,self.obstacle_sprites],'object',surf)

                        if style == 'entities':#1 skeletor,2 grzybol, 3 pso niedzwiedz
                            if column == '0':
                                self.player = Player(
                                                    (x,y),
                                                     [self.visable_sprites],
                                                     self.obstacle_sprites,
                                                     self.create_attack,
                                                     self.destroy_attack,
                                                     self.create_magic) 
                            
                            else:
                                if column == '1': monster_name = 'skeletor'
                                elif column == '2': monster_name = 'mushroom'
                                elif column == '3': monster_name = 'bear_dog'
                                Enemy(monster_name,
                                      (x,y),
                                      [self.visable_sprites,self.attackable_sprites], #grupy 'sprite'ów' do jakich należą wrogowie
                                      self.obstacle_sprites,
                                      self.damage_player,
                                      self.trigger_death_elements,
                                      self.add_xp)
                                #create attack bez () bo nie -> call a pass function
                                #player idzie do visable sprites a potem dostaje info o obstacle sprites tylko do kolizji



    def create_attack(self):
        self.current_attack = Weapon(self.player,[self.visable_sprites,self.attack_sprites])


    def create_magic(self,style,strength,mana_cost):
        if style =='heal':
            self.magic_player.heal(self.player,strength,mana_cost,[self.visable_sprites])

        if style == 'flame':
            self.magic_player.flame(self.player,mana_cost,[self.visable_sprites,self.attack_sprites])


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
                        if target_sprite.label_sprite == 'flowers':
                            position = target_sprite.rect.midtop #elements ida tam gdzie wczesniej byly kwiaty
                            self.animation_player.create_flowers_elements(position,[self.visable_sprites])
                            target_sprite.kill() #niszczymy kwiaty
                        else:
                            target_sprite.get_damage(self.player,attack_sprite.label_sprite)



    def damage_player(self,amount,attack_type):
        if self.player.vulnerable:
            self.player.hp -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            #spawnujemy elementy
            self.animation_player.create_elements(attack_type,self.player.rect.center,[self.visable_sprites])


    def trigger_death_elements(self,position,element_type):
        self.animation_player.create_elements(element_type,position,self.visable_sprites)


    def add_xp(self,amount):
        self.player.xp += amount

    def toggle_menu(self):
        self.game_paused = not self.game_paused


    def run(self):
        self.visable_sprites.custom_draw(self.player) #zawsze rysujemy nasze widoczne sprite'y
        self.ui.display(self.player)
        if self.game_paused:
            self.upgrade.display()
        else:
            self.visable_sprites.update() #update'ujemy widoczne sprite tylko gdy gra NIE JEST zapauzowana
            self.visable_sprites.enemy_update(self.player)
            self.player_attack_logic()

class SortByY(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.width_center = self.display_surface.get_size()[0]//2 #1 atrybut surface czyli szerokosc dzielimy na pol zeby gracz byl zawsze w centrum kamery
        self.height_center = self.display_surface.get_size()[1]//2
        self.shift = pygame.math.Vector2()
        self.floor_surf = pygame.image.load('../img/tiles/map.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

    def custom_draw(self,player):
        self.shift.x = player.rect.centerx - self.width_center #jak bardzo gracz "oddalil" sie od centrum
        self.shift.y = player.rect.centery - self.height_center
        floor_shift_position = self.floor_rect.topleft - self.shift
        self.display_surface.blit(self.floor_surf,floor_shift_position)
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery): #rysujemy według osi Y (więc najpierw rysujemy najwyższe i potem co raz niżej (im niżej tym "wyższa warstwa"))
            shift_position = sprite.rect.topleft - self.shift #przesuniecie sprite'ow o wektor
            self.display_surface.blit(sprite.image,shift_position) #rysowanie jednoczesnie w tej samej pozycji rectangle i obrazka


    def enemy_update(self,player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'label_sprite') and sprite.label_sprite == 'enemy'] #hasattr sprawdza czy wystepuje atrybut label_sprite po to by nie wystepowal error dla kazdego ktory go nie ma
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
