import pygame
from settings import *
from post import import_folder
from entity import Entity

class Player(Entity):
    def __init__(self,pos,groups,obstacle_sprites,create_attack,destroy_attack,create_magic):
        super().__init__(groups)
        self.image = pygame.image.load('../img/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0,-26)

        self.import_player_assets()
        self.status = 'down'
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.create_attack = create_attack
        self.obstacle_sprites = obstacle_sprites

        #bron
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index] #potrzebujemy listy by móc zdobywac index broni
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
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None

        #statystyki
        self.stats = {'health':100,'energy':60,'attack':10,'magic':4,"speed":6}
        self.health = self.stats['health'] *0.5
        self.energy = self.stats['energy'] *0.8
        self.exp = 123
        self.speed = self.stats['speed']

    def import_player_assets(self):
        character_path = '../img/player/'
        self.animations = {'up': [],'down': [], 'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                           'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': []}
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
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

            if keys[pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[self.magic_index]
                strength = list(magic_data.values())[self.magic_index]['strength'] +self.stats['magic']
                cost = list(magic_data.values())[self.magic_index]['cost']


                self.create_magic(style,strength,cost)

            if keys[pygame.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()

                if self.weapon_index < len(list(weapon_data.keys())) - 1: #-1 bo indeksy liczymy od 0, więc bronie
                    #mają 0,1,2; natomiast ilość broni to 3
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0
                self.weapon = list(weapon_data.keys())[self.weapon_index]


            if keys[pygame.K_e] and self.can_switch_magic:
                self.can_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()

                if self.magic_index < len(list(magic_data.keys())) - 1: #-1 bo indeksy liczymy od 0, więc bronie
                    #mają 0,1,2; natomiast ilość broni to 3
                    self.magic_index += 1
                else:
                    self.magic_index = 0
                self.magic = list(magic_data.keys())[self.magic_index]

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
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_attack()

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True


        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animations_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)] #int bo animation speed to float a python oczekuje intów
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)