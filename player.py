import pygame
from settings import *
from math import sin

class Player(pygame.sprite.Sprite):
    def __init__(self,position,group,obstacle_sprites,create_attack,destroy_attack,create_magic):
        super().__init__(group)
        self.image = pygame.image.load('../img/player/down/down_0.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(-6,-26)
        self.import_player()
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.create_attack = create_attack
        self.obstacle_sprites = obstacle_sprites
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(info_weapons.keys())[self.weapon_index] #potrzebujemy listy by móc zdobywac index broni
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200 #cooldown wspomagajacy timer po to by 
        #podczas pojedynczego wcisniecia przycisku zmiany broni nie doszlo do wielu 
        #zmian broni jako ze fizycznie wcisniecie przyciska to np okolo 0,2s 
        #co dla komputera oznacza wiele klatek a wiec powtorzenie kodu zmiany broni 
        #wiele razy

        #magia
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(info_magic.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None

        #statystyki
        self.stats = {'hp':100,'mana':60,'attack':10,'magic':4,"speed":6}
        self.max_stats = {'hp':300,'mana':140,'attack':20,'magic':10,"speed":10}
        self.upgrade_cost = {'hp':100,'mana':100,'attack':100,'magic':100,"speed": 100}
        self.hp = self.stats['hp'] *0.5
        self.mana = self.stats['mana'] *0.8
        self.xp = 5000
        self.speed = self.stats['speed']


        #timer obrażeń
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500


        #importujemy dźwieki
        self.weapon_attack_sound = pygame.mixer.Sound('../sound/sword.wav')
        self.weapon_attack_sound.set_volume(0.4)

    def import_player(self):
        player_path = '../img/player/'
        self.animation_status = {'up': [],'down': [], 'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                           'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': []}
        for animation in self.animation_status.keys():
            full_path = player_path + animation
            self.animation_status[animation] = folder_import(full_path)



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


    def player_input(self):
        if not self.attacking: #by nie mozna bylo zmienic kierunku w trakcie ataku
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.direction.y =-1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0


            if keys[pygame.K_RIGHT]:
                self.direction.x =1
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0
            if keys[pygame.K_SPACE]: #and not self.attacking: #po to by gracz nie atakował trzymając przycisk ORAZ by nie mógł atakować i uzywac magii jednoczesnie ORAZ by nie mogl ich uzywac w bardzooo krotkich odstepach czasu
                self.attacking = True
                self.attack_time = pygame.time.get_ticks() #zapisuje czas tylko ostatniego ataku
                self.create_attack()
                self.weapon_attack_sound.play()
            if keys[pygame.K_w]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(info_magic.keys())[self.magic_index]
                strength = list(info_magic.values())[self.magic_index]['strength'] +self.stats['magic']
                mana_cost = list(info_magic.values())[self.magic_index]['mana_cost']
                self.create_magic(style,strength,mana_cost)

            if keys[pygame.K_a] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()

                if self.weapon_index < len(list(info_weapons.keys())) - 1: #-1 bo indeksy liczymy od 0, więc bronie
                    #mają 0,1,2; natomiast ilość broni to 3
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0
                self.weapon = list(info_weapons.keys())[self.weapon_index]


            if keys[pygame.K_d] and self.can_switch_magic:
                self.can_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()

                if self.magic_index < len(list(info_magic.keys())) - 1: #-1 bo indeksy liczymy od 0, więc bronie
                    #mają 0,1,2; natomiast ilość broni to 3
                    self.magic_index += 1
                else:
                    self.magic_index = 0
                self.magic = list(info_magic.keys())[self.magic_index]

    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0: #gracz się nie rusza
            if not 'idle' in self.status and not 'attack' in self.status: #sprawdzamy czy status nie posiada już idle w tytule bo inaczej ciągle będzie dodawać koncowke _idle do statusu wiec otrzymamy up_idle_idle_idle_idle
                self.status = self.status + '_idle'
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status: #inaczej beda tworzone kombosy rigt_idle_attack
                    self.status = self.status.replace('_idle','_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status: #po to by _attack zniknelo z statusu gdy zaatakujemy i przejdziemy w tryb idle
                self.status = self.status.replace('_attack','')


    def cooldowns(self):
        current_time = pygame.time.get_ticks() #cały czas liczy czas

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + info_weapons[self.weapon]['cooldown']: #to po plusie mozna usunac
                self.attacking = False
                self.destroy_attack()

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True


        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

    def create_animation(self):
        animation = self.animation_status[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)] #int bo animation speed to float a python oczekuje intów
        self.rect = self.image.get_rect(center = self.hitbox.center)
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_full_weapon_damage(self): #full obrazenia to staty bohatera + staty broni
        base_damage = self.stats['attack']
        weapon_damage = info_weapons[self.weapon]['damage'] #info_weapons w pliku settings
        return base_damage + weapon_damage


    def get_full_magic_damage(self):
        base_damage = self.stats['magic']
        spell_damage = info_magic[self.magic]['strength']
        return base_damage + spell_damage


    def get_value_by_index(self,index):
        return list(self.stats.values())[index]


    def get_cost_by_index(self,index):
        return list(self.upgrade_cost.values())[index]



    def mana_recovery(self):
        if self.mana < self.stats['mana']:
            self.mana += 0.01 * self.stats['magic']
        else:
            self.mana = self.stats['mana']

    def update(self):
        self.player_input()
        self.cooldowns()
        self.get_status()
        self.create_animation()
        self.move(self.stats['speed'])
        self.mana_recovery()
