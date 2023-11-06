import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self,position,group,obstacle_sprites):
        super().__init__(group)
        
        #grafika
        self.image = pygame.image.load('../img/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(0,-26)
        self.import_player()
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.15
        
        #ruch
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        #sprite'y
        self.obstacle_sprites = obstacle_sprites

    def import_player(self):
        player_path = '../img/player/'
        self.animation_status = {'up': [],'down': [], 'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                           'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': []}
        for animation in self.animation_status.keys():
            full_path = player_path + animation
            self.animation_status[animation] = import_folder(full_path)

    def player_input(self):
        if not self.attacking: #by nie mozna bylo zmienic kierunku w trakcie ataku
            keys = pygame.key.get_pressed()

            #góra/dół
            if keys[pygame.K_UP]:
                self.direction.y =-1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            #lewo/prawo
            if keys[pygame.K_RIGHT]:
                self.direction.x =1
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

        #atakowanie
            if keys[pygame.K_SPACE]: #i not self.attacking: #po to by gracz nie atakował trzymając przycisk ORAZ by nie mógł atakować i uzywac magii jednoczesnie ORAZ by nie mogl ich uzywac w bardzooo krotkich odstepach czasu
                self.attacking = True
                self.attack_time = pygame.time.get_ticks() #zapisuje czas tylko ostatniego ataku
                print('attack')

        #magia
            if keys[pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                print('magic')


    def get_status(self):
        #status bezczynności
        if self.direction.x == 0 and self.direction.y == 0: #gracz się nie rusza
            if not 'idle' in self.status and not 'attack' in self.status: #sprawdzamy czy status nie posiada już idle w tytule bo inaczej ciągle będzie dodawać koncowke _idle do statusu wiec otrzymamy up_idle_idle_idle_idle
                self.status = self.status + '_idle'

        #status ataku
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status: #inaczej beda tworzone kombosy rigt_idle_attack
                    #nadpisujemy bezczynność
                    self.status = self.status.replace('_idle','_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status: #po to by _attack zniknelo z statusu gdy zaatakujemy i przejdziemy w tryb idle
                self.status = self.status.replace('_attack','')


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

    def cooldowns(self):
        current_time = pygame.time.get_ticks() #cały czas liczy czas

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False


    def create_animation(self):
        animation = self.animation_status[self.status]

        #pętla przez indeksy klatek
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        #podstawienie grafiki
        self.image = animation[int(self.frame_index)] #int bo animation speed to float a python oczekuje intów
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def update(self):
        self.player_input()
        self.cooldowns()
        self.get_status()
        self.create_animation()
        self.move(self.speed)
