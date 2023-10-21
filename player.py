import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self,position,group,obstacle_sprites):
        super().__init__(group)
        
        #grafika
        self.image = pygame.image.load('../img/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(0,-26)

        #ruch
        self.direction = pygame.math.Vector2()
        self.speed = 5

        #sprite'y
        self.obstacle_sprites = obstacle_sprites

    def player_input(self):
        keys = pygame.key.get_pressed()

        #góra/dół
        if keys[pygame.K_UP]:
            self.direction.y =-1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        #lewo/prawo
        if keys[pygame.K_RIGHT]:
            self.direction.x =1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0


    def move(self,speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize() #aby prędkość nie była podwójna przy trzymaniu dwóch kierunków
            #jednocześnie np. dół i prawo
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center #hitbox jest w srodku

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


    def update(self):
        self.player_input()
        self.move(self.speed)
