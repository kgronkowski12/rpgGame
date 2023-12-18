import pygame
from settings import *
from math import sin


class Enemy(pygame.sprite.Sprite):
    def __init__(self,monster_name,position,group,obstacle_sprites,damage_player,trigger_death_elements,add_xp):
        super().__init__(group)
        self.label_sprite = 'enemy'
        #grafika
        self.import_graphics(monster_name)
        self.status = 'idle'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animation_status[self.status][self.frame_index]


        #poruszanie sie
        self.rect = self.image.get_rect(topleft = position)
        self.hitbox = self.rect.inflate(0,-10)
        self.obstacle_sprites = obstacle_sprites
        self.direction = pygame.math.Vector2()


        #statystyki
        self.monster_name = monster_name
        monster_info = info_monster[self.monster_name]
        self.hp = monster_info['hp']
        self.xp= monster_info['xp']
        self.speed= monster_info['speed']
        self.attack_damage= monster_info['damage']
        self.pushback= monster_info['pushback']
        self.range_attack= monster_info['range_attack']
        self.range_notice= monster_info['range_notice']
        self.attack_type= monster_info['attack_type']

        #interakcje z graczem
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400
        self.damage_player = damage_player
        self.trigger_death_elements = trigger_death_elements
        self.add_xp = add_xp

        #timer niewidzialności
        #wrogowie bez tego umieraja po jednym ciosie poniewaz gra po prostu sprawdza
        #kolizje a wiec jeden atak trwa tak naprawde 60 klatek/s #czyli 60 ataków
        self.vulnerable = True
        self.hit_time = None
        self.invisibility_duration = 300

        #dźwięki
        self.death_sound = pygame.mixer.Sound('../sound/death.wav')
        self.hit_sound = pygame.mixer.Sound('../sound/hit.wav')
        self.attack_sound = pygame.mixer.Sound(monster_info['attack_sound'])
        self.death_sound.set_volume(0.6)
        self.hit_sound.set_volume(0.6)
        self.attack_sound.set_volume(0.3)

    def import_graphics(self,name):
        self.animation_status = {'idle':[],'move':[],'attack':[]}
        main_path = f'../img/enemies/{name}/'
        for animation in self.animation_status.keys():
            self.animation_status[animation] = folder_import(main_path + animation)
            #main path to ta sciezka wyzej, animation to idle/move/attack
            #laczymy je i dostajemy sciezke do konkretnego folderu
            #i potem funkcja import folder daje nam kazde zdjecie w danym folderze
            #i mozna walnac je do naszego słownika



    def move(self,speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize() #aby prędkość nie była podwójna przy trzymaniu dwóch kierunków
            #jednocześnie np. dół i prawo
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self,direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: #idziemy w prawo
                        self.hitbox.right = sprite.rect.left #skoro idziemy w prawo to ewentualna kolizja na 100% będzie po prawej stronie
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.rect.right
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: #idziemy w dół, w pygame center point (0,0) jest w gornym lewym rogu
                        self.hitbox.bottom = sprite.rect.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.rect.bottom

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0: return 255 #pelna przezroczystosc
        else: return 0



    def get_player_distance_direction(self,player): #może to rozbić te funkcje
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude() #(odejmujemy wektory gracza i wroga od poczatku ukladu wspolrzednych)
        # a dostajemy wektor miedzy wrogiem a graczem i potem za pomoca magnitude zmieniamy wektor w odleglosc
        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2() # jeśli gracz i wrog sa w tym samym miejscu to dajemy wrogowi po prostu wektor (0,0)
        return (distance,direction)



    def get_status(self,player):
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.range_attack and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        elif distance <= self.range_notice:
            self.status = 'move'
        else:
            self.status = 'idle'
    

    def actions(self,player):
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage,self.attack_type)
            self.attack_sound.play()
        elif self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2() #gdy gracz wyjdzie z zasiegu wzroku wroga, zatrzyma się on odrazu w miejscu

    def create_animation(self): # prawie to samo co funcja create_animation w graczu
        animation = self.animation_status[self.status]

        self.frame_index += self.animation_speed #bierzemy to z entity
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center) #ruszamy hitbox a nie rectangle,wiec 'wkladamy' rectangle w srodek hitboxa

        if not self.vulnerable: #gdy wrog jest atakowany
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255) #set alpha to przezroczystość (255 to pelna), czyli gdy nie jest atakowany to widac caly czas w 100%

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            current_time = pygame.time.get_ticks()
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invisibility_duration:
                self.vulnerable = True



    def get_damage(self,player,attack_type):
        if self.vulnerable:
            self.hit_sound.play()
            self.direction = self.get_player_distance_direction(player)[1] #przesuwamy wroga w inny kierunek
            if attack_type == 'weapon':
                self.hp -= player.get_full_weapon_damage() #getter funkcja
            else:
                self.hp -= player.get_full_magic_damage()
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

    def check_death(self):
        if self.hp <= 0:
            self.kill()
            self.trigger_death_elements(self.rect.center,self.monster_name) #sprawdzac rzeczy typu element type bo sie w wielu powtarza
            self.add_xp(self.xp)
            self.death_sound.play()


    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.pushback



    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.create_animation()
        self.cooldowns()
        self.check_death()
    def enemy_update(self,player):
        self.get_status(player)
        self.actions(player)
