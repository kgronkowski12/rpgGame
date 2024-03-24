import pygame
from settings import *
from froggo import Froggo
from random import choice
from combat import *
from ui import UI
from monster import Monster
from elements import AnimationMaker
from upgrade import Upgrade

class Tile(pygame.sprite.Sprite):
    def __init__(self,position,label,category,surface=pygame.Surface((TILESIZE,TILESIZE))):
        self.UI = False
        super().__init__(label)
        self.category = category
        self.graphic = surface
        if category == 'object':
            self.rect = self.graphic.get_rect(topleft= (position[0],position[1] - TILESIZE)) #odejmujemy tile bo duze obiekty maja 128x64 lub 64x128 wiec 'topleft' jest przesuwany na srodek
        else:
            self.rect = self.graphic.get_rect(topleft=position) #cały rozmiar

        self.hitbox = self.rect.inflate(0,-10) #stworzenie hitboxu

class World:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.pause = False


        #przygotowanie grupy sprite'ow
        self.visable_sprites = SortByY()

        #sprite efektów mapy
        self.water_sprites = pygame.sprite.Group()
        self.lava_sprites = pygame.sprite.Group()
        self.swamp_sprites = pygame.sprite.Group()

        self.teleporter_1_sprite = pygame.sprite.Group()
        self.teleporter_2_sprite = pygame.sprite.Group()
        self.teleporter_3_sprite = pygame.sprite.Group()

        #sprite ataku
        self.current_attack_sprite = None
        self.obstacle_sprites = pygame.sprite.Group()
        self.combat_sprites = pygame.sprite.Group() #bronie i magia
        self.destroyable_sprites = pygame.sprite.Group() # wrogowie
        #sprawdzamy kolizje miedzy attack a atackable

        self.create_world()
        #elementy
        self.animation_froggo = AnimationMaker()
        self.spells_froggo = Spells(self.animation_froggo)
        #user interface
        self.ui = UI()
        self.upgrade = Upgrade(self.froggo)



    def create_world(self):
        layouts = {
            'world_wall': csv_import('../map/map__Wall.csv'),
            'flowers': csv_import('../map/map__Flowers.csv'),
            'object': csv_import('../map/map__Objects.csv'),
            'entities': csv_import('../map/map__Characters.csv'),
            'lava': csv_import('../map/map__Lava.csv'),
            'water': csv_import('../map/map__Water.csv'),
            'swamp': csv_import('../map/map__Swamp.csv'),
            'teleport_1': csv_import('../map/teleport/map__Teleport1.csv'),
            'teleport_2': csv_import('../map/teleport/map__Teleport2.csv'),
            'teleport_3': csv_import('../map/teleport/map__Teleport3.csv')
        }

        graphics = {
            'flowers': folder_import('../img/flowers'),
            'objects': folder_import('../img/objects'),
            'teleporter': folder_import('../img/teleport')
        }

        #type = world_wall, layout = csv file
        for type,layout in layouts.items():
            for index_OF_row,row in enumerate(layout):
                for index_OF_column, column in enumerate(row):
                    if column != '-1': #ma rysować granice tylko w polach, które nie są puste (-1), tutaj wartość 395 oznacza granicę
                        #bez tego 'if' cała mapa zostaje uznana za granicę nie do przejścia i gracz automatycznie zostaje wyrzucony z niej
                        x = index_OF_column * TILESIZE
                        y = index_OF_row * TILESIZE
                        if type == 'world_wall':
                            Tile((x,y),[self.obstacle_sprites],'invisible') #self.visable_sprites jako 1 argument sprawi ze granice będą widoczne jako czarne pola


                        if type == "lava":
                            Tile((x,y),[self.lava_sprites],'invisible')
                        if type == "water":
                            Tile((x,y),[self.water_sprites],'invisible')
                        if type == "swamp":
                            Tile((x,y),[self.swamp_sprites],'invisible')


                        if type == "teleport_1":
                            random_surface = choice(graphics['teleporter'])
                            Tile((x,y),[self.visable_sprites,self.teleporter_1_sprite], 'teleport_1',random_surface)
                        if type == "teleport_2":
                            random_surface = choice(graphics['teleporter'])
                            Tile((x,y),[self.visable_sprites,self.teleporter_2_sprite], 'teleport_2',random_surface)
                        if type == "teleport_3":
                            random_surface = choice(graphics['teleporter'])
                            Tile((x,y),[self.visable_sprites,self.teleporter_3_sprite], 'teleport_3',random_surface)                                              


                        if type == 'flowers':
                            randomize_flowers = choice(graphics['flowers'])
                            Tile((x,y), [self.visable_sprites,self.obstacle_sprites,self.destroyable_sprites], 'flowers',randomize_flowers)
                        if type == 'object':
                            surface = graphics['objects'][int(column)]
                            Tile((x,y),[self.visable_sprites,self.obstacle_sprites],'object',surface)
                        if type == 'entities':#1 skeletor,2 grzybol, 3 pso niedzwiedz
                            if column == '0':
                                self.froggo = Froggo((x,y), [self.visable_sprites], self.obstacle_sprites, self.water_sprites,self.lava_sprites,self.swamp_sprites,self.teleporter_1_sprite,self.teleporter_2_sprite,self.teleporter_3_sprite,self.attack, self.kill_weapon_sprite, self.create_spells)
                            else:
                                if column == '1': 
                                    monster_name = 'skeletor'
                                elif column == '2': 
                                    monster_name = 'mushroom'
                                elif column == '3': 
                                    monster_name = 'bear_dog'
                                elif column == '4': 
                                    monster_name = 'mimic'
                                    #grupy 'sprite'ów' do jakich należą wrogowie
                                Monster(monster_name,(x,y),[self.visable_sprites,self.destroyable_sprites], self.obstacle_sprites, self.lava_sprites,  self.water_sprites,self.damage_froggo, self.trigger_death_elements, self.add_score_xp)
                                #create attack bez () bo nie -> call a pass function
                                #froggo idzie do visable sprites a potem dostaje info o obstacle sprites tylko do kolizji



    def attack(self):
        self.current_attack_sprite = Weapon([self.visable_sprites,self.combat_sprites],self.froggo)

    def kill_weapon_sprite(self):
        if self.current_attack_sprite:
            self.current_attack_sprite.kill()
        self.current_attack_sprite = None


    def toggle_menu(self):
        self.pause = not self.pause
        
    def froggo_combat(self): #przejdziemy przez wszystkie sprite atakow i sprawdzimy czy jakis z nich koliduje z attackable sprite'm
        if self.combat_sprites:
            for item in self.combat_sprites:
                collide_img = pygame.sprite.spritecollide(item,self.destroyable_sprites,False)
                #sprawdzamy kolizje miedzy pierwszym argumentem a drugim i na drugim wykonujemy trzeci (DOKILL), nie chcemy zabijac wiec zostawiamy na false 
                if collide_img:
                    for item in collide_img:
                        if item.category == 'flowers':
                            position = item.rect.midtop #elements ida tam gdzie wczesniej byly kwiaty
                            self.animation_froggo.create_elements("flowers",position,[self.visable_sprites])
                            item.kill() #niszczymy kwiaty
                            self.destroy_sound = pygame.mixer.Sound('../sound/flower.wav')
                            self.destroy_sound.set_volume(0.6)
                            self.destroy_sound.play()
                        if item.category == 'monster':
                            item.get_damage(self.froggo,item.category)

    def create_spells(self,type,strength,mana_cost):
        if type == 'energy_ball':
            self.spells_froggo.energy_ball(mana_cost, self.froggo, [self.visable_sprites,self.combat_sprites])
        if type =='heal':
            self.spells_froggo.cast_heal(mana_cost, strength, self.froggo,[self.visable_sprites])
        if type =='shield':
            self.spells_froggo.shield(mana_cost, self.froggo)

    def add_score_xp(self,amount):

        self.froggo.xp += amount
        self.froggo.score += amount
        self.froggo.monster_count += 1
        if self.froggo.monster_count == 51:
            self.froggo.score += 3000




    def damage_froggo(self,amount,attack_type):
        if self.froggo.vulnerable:
            self.froggo.hp -= amount
            self.froggo.vulnerable = False
            self.froggo.hurt_time = pygame.time.get_ticks()
            #spawnujemy elementy
            self.animation_froggo.create_elements(attack_type,self.froggo.rect.center,[self.visable_sprites])


    def trigger_death_elements(self,position,element_type):
        self.animation_froggo.create_elements(element_type,position,self.visable_sprites)







    def run(self):
        #updatujemy i rysujemy gre
        self.visable_sprites.generate(self.froggo) #zawsze rysujemy nasze widoczne sprite'y
        self.ui.display(self.froggo)
        if self.pause:
            self.upgrade.show_upgrade()
        else:
            self.visable_sprites.update() #update'ujemy widoczne sprite tylko gdy gra NIE JEST zapauzowana
            self.visable_sprites.monster_update(self.froggo)
            self.froggo_combat()

class SortByY(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.terrain = pygame.image.load('../img/tiles/map.png')
        self.terrain_rectangle = self.terrain.get_rect(topleft = (0,0))
        self.width_center = self.screen.get_size()[0]//2 #1 atrybut surface czyli szerokosc dzielimy na pol zeby gracz byl zawsze w centrum kamery
        self.height_center = self.screen.get_size()[1]//2
        self.shift = pygame.math.Vector2()

    def generate(self,froggo):
        #liczymy przesunięcie
        self.shift.x = froggo.rect.centerx - self.width_center #jak bardzo gracz "oddalil" sie od centrum
        self.shift.y = froggo.rect.centery - self.height_center

        #rysowanie mapy
        terrain_shift_position = self.terrain_rectangle.topleft - self.shift
        self.screen.blit(self.terrain,terrain_shift_position)


        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery): #rysujemy według osi Y (więc najpierw rysujemy najwyższe i potem co raz niżej (im niżej tym "wyższa warstwa"))
            shift_position = sprite.rect.topleft - self.shift #przesuniecie sprite'ow o wektor
            self.screen.blit(sprite.graphic,shift_position) #rysowanie jednoczesnie w tej samej pozycji rectangle i obrazka
        for sprite in self.sprites():
            if sprite.UI:
                shift_position = sprite.rect.topleft - self.shift  # przesuniecie sprite'ow o wektor
                self.screen.blit(sprite.graphic,shift_position)  # rysowanie jednoczesnie w tej samej pozycji rectangle i obrazka



    def monster_update(self,froggo):
        monster_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'category') and sprite.category == 'monster'] #hasattr sprawdza czy wystepuje atrybut category po to by nie wystepowal error dla kazdego ktory go nie ma
        for monster in monster_sprites:
            monster.monster_update(froggo)
