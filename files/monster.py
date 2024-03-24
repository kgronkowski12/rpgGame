import pygame
from settings import *
from math import sin
from elements import *
from world import *
import random

class Monster(pygame.sprite.Sprite):
    def __init__(self,monster_name,position,label,obstacle_sprites,lava_sprites,water_sprites,damage_froggo,trigger_death_elements,add_xp):
        super().__init__(label)
        self.UI = False
        self.category = 'monster' #typ jest po to
        #aby mialy rozne wartosci i reakcje, np gracz atakuje wroga (traci zdrowie a potem umiera)
        #gracz atakuje kwiatka (nie ma zycia ale od razu zostaje zniszczone) itp

        #grafika
        self.import_graphics(monster_name)
        self.status = 'idle'
        self.timer = 0
        self.frame_index = 0
        self.animation_speed = 0.15
        self.graphic = self.animation_status[self.status][self.frame_index]

        self.screen = pygame.display.get_surface()
        self.font = pygame.font.Font(FONT, FONT_SIZE)

        #poruszanie sie
        self.rect = self.graphic.get_rect(topleft = position)
        self.hitbox = self.rect.inflate(0,-10)
        self.obstacle_sprites = obstacle_sprites
        self.direction = pygame.math.Vector2()

        self.lava_sprites = lava_sprites
        self.water_sprites = water_sprites


        #statystyki
        self.monster_name = monster_name
        monster_info = INFO_MONSTER[self.monster_name]
        self.hp = monster_info['hp']
        self.xp= monster_info['xp']
        self.speed= monster_info['speed']
        self.attack_damage= monster_info['damage']
        self.pushback= monster_info['pushback']
        self.range_attack= monster_info['range_attack']
        self.range_notice= monster_info['range_notice']
        self.attack_type= monster_info['attack_type']


        self.additional_stats = {'swamp':1}
        self.swamp = self.additional_stats['swamp']

        #interakcje z graczem
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400
        self.damage_froggo = damage_froggo
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
        self.death_sound.set_volume(0.5)
        self.hit_sound.set_volume(0.5)
        self.attack_sound.set_volume(0.2)

    def import_graphics(self,name): #podobnie jak import froggo assets z self animations
        self.animation_status = {'idle':[],'move':[],'attack':[]}
        main_folder = f'../img/enemies/{name}/'
        for animation in self.animation_status.keys():
            self.animation_status[animation] = folder_import(main_folder + animation)
            #main folder to ta sciezka wyzej, animation to idle/move/attack
            #laczymy je i dostajemy sciezke do konkretnego folderu
            #i potem funkcja import folder daje nam kazde zdjecie w danym folderze
            #i mozna walnac je do naszego słownika



    def move(self,speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize() #aby prędkość nie była podwójna przy trzymaniu dwóch kierunków
            #jednocześnie np. dół i prawo
        self.hitbox.x += self.direction.x * (speed * self.swamp)
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * (speed * self.swamp)
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

        for sprite in self.lava_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                self.hp -= 0.1

        for sprite in self.water_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                self.swamp -= 0.006
            if self.swamp <= 0.1:
                self.swamp = 0.1
            if self.swamp >= 1:
                self.swamp = 1
            if self.swamp < 1:
                self.swamp += 0.0001

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0: return 255 #pelna przezroczystosc
        else: return 0
    
    def froggo_distance(self,froggo):
        vector = (pygame.math.Vector2(froggo.rect.center) - pygame.math.Vector2(self.rect.center)) #(odejmujemy wektory gracza i wroga od poczatku ukladu wspolrzednych)
        # a dostajemy wektor miedzy wrogiem a graczem i potem za pomoca magnitude zmieniamy wektor w odleglosc
        distance = vector.magnitude()
        return (distance)
    
    def froggo_direction(self,froggo):
        distance = self.froggo_distance(froggo)
        if distance > 0:
            direction = (pygame.math.Vector2(froggo.rect.center) - pygame.math.Vector2(self.rect.center)).normalize()
        else:
            direction = pygame.math.Vector2() # jeśli gracz i wrog sa w tym samym miejscu to dajemy wrogowi po prostu wektor (0,0)
        return (direction)




    def get_status(self,froggo):
        distance = self.froggo_distance(froggo)

        if distance <= self.range_attack and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        elif distance <= self.range_notice:
            self.status = 'move'
        else:
            self.status = 'idle'
        if self.status=='move':
            self.timer+=1
            if(self.timer<=45):
                say = ""
                if self.monster_name=="bear_dog":
                    say = "Woof Woof!"
                if self.monster_name=="mushroom":
                    say = "Fungi fury!"
                if self.monster_name=="skeletor":
                    say = "Bony barrage!"
                if self.monster_name=="mimic":
                    say = "Gotchya!"
                text_surface2 = self.font.render(say,False,COLOUR_TEXT)
                x= WIDTH/2 + self.hitbox.x - froggo.hitbox.x + 35
                y= HEIGHT/2 + self.hitbox.y - froggo.hitbox.y + 25
                text_rectangle2 = text_surface2.get_rect(topleft = (x,y+38))

                pygame.draw.rect(self.screen,COLOUR_UI_BG,text_rectangle2.inflate(30,25))
                self.screen.blit(text_surface2,text_rectangle2)
    

    def actions(self,froggo):
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            self.damage_froggo(self.attack_damage,self.attack_type)
            self.attack_sound.play()
        elif self.status == 'move':
            self.direction = self.froggo_direction(froggo)
        else:
            self.direction = pygame.math.Vector2() #gdy gracz wyjdzie z zasiegu wzroku wroga, zatrzyma się on odrazu w miejscu

    def create_animation(self):
        animation = self.animation_status[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0

        self.graphic = animation[int(self.frame_index)]
        self.rect = self.graphic.get_rect(center = self.hitbox.center) #ruszamy hitbox a nie rectangle,wiec 'wkladamy' rectangle w srodek hitboxa

        if not self.vulnerable: #gdy wrog jest atakowany
            alpha = self.wave_value()
            self.graphic.set_alpha(alpha)
        else:
            self.graphic.set_alpha(255) #set alpha to przezroczystość (255 to pelna), czyli gdy nie jest atakowany to widac caly czas w 100%

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            current_time = pygame.time.get_ticks()
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invisibility_duration:
                self.vulnerable = True



    def get_damage(self,froggo,attack_type):
        if self.vulnerable:
            self.hit_sound.play()
            self.direction = self.froggo_direction(froggo) #przesuwamy wroga w inny kierunek
            if attack_type == 'weapon':
                self.hp -= froggo.damage()[0] #getter funkcja
            else:
                self.hp -= froggo.damage()[1]
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

    def check_death(self):
        if self.hp <= 0:
            player_image = pygame.image.load("../img/flowers/flower_3.png").convert_alpha()  # Load image with transparency
            player_image = pygame.transform.scale(player_image, (50, 50)) 
            type="heart"
            rand = random.randint(0,100)
            if rand<=70:
                type="mana"
            if rand<=50:
                type="coin"


            player_sprite =     Drop(type)
            player_sprite.rect.topleft=self.rect.topleft
            player_sprite.image = player_image
            all_sprites.add(player_sprite)
            #visable_sprites.add(player_sprite)

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
    def monster_update(self,froggo):
        self.get_status(froggo)
        self.actions(froggo)
