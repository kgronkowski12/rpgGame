import pygame
from settings import *
from entity import Entity
from post import *

class Enemy(Entity):
    def __init__(self,monster_name,pos,groups,obstacle_sprites,damage_player,trigger_death_particles,add_exp):
        super().__init__(groups)
        self.sprite_type = 'enemy'

        #grafika
        self.import_graphics(monster_name)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]


        #poruszanie sie
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-10)
        self.obstacle_sprites = obstacle_sprites


        #statystyki
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.exp= monster_info['exp']
        self.speed= monster_info['speed']
        self.attack_damage= monster_info['damage']
        self.resistance= monster_info['resistance']
        self.attack_radius= monster_info['attack_radius']
        self.notice_radius= monster_info['notice_radius']
        self.attack_type= monster_info['attack_type']

        #interakcje z graczem
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400
        self.damage_player = damage_player
        self.trigger_death_particles = trigger_death_particles
        self.add_exp = add_exp

        #timer niewidzialności
        #wrogowie bez tego umieraja po jednym ciosie poniewaz gra po prostu sprawdza
        #kolizje a wiec jeden atak trwa tak naprawde 60 klatek/s #czyli 60 ataków
        self.vulnerable = True
        self.hit_time = None
        self.invisibility_duration = 300

    def import_graphics(self,name): #podobnie jak import player assets z self animations
        self.animations = {'idle':[],'move':[],'attack':[]}
        main_path = f'../img/enemies/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)
            #main path to ta sciezka wyzej, animation to idle/move/attack
            #laczymy je i dostajemy sciezke do konkretnego folderu
            #i potem funkcja import folder daje nam kazde zdjecie w danym folderze
            #i mozna walnac je do naszego słownika



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

        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'
    

    def actions(self,player):
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage,self.attack_type)
        elif self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2() #gdy gracz wyjdzie z zasiegu wzroku wroga, zatrzyma się on odrazu w miejscu

    def animate(self): # prawie to samo co funcja animate w graczu
        animation = self.animations[self.status]

        self.frame_index += self.animations_speed #bierzemy to z entity
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
            self.direction = self.get_player_distance_direction(player)[1] #przesuwamy wroga w inny kierunek
            if attack_type == 'weapon':
                self.health -= player.get_full_weapon_damage() #getter funkcja
            else:
                self.health -= player.get_full_magic_damage()
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

    def check_death(self):
        if self.health <= 0:
            self.kill()
            self.trigger_death_particles(self.rect.center,self.monster_name) #sprawdzac rzeczy typu particle type bo sie w wielu powtarza
            self.add_exp(self.exp)


    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance #zmienic resistance w pushback



    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.cooldowns()
        self.check_death()
    def enemy_update(self,player):
        self.get_status(player)
        self.actions(player)
