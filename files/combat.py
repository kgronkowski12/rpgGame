import pygame
from settings import *
from elements import *

class Weapon(pygame.sprite.Sprite):
    def __init__(self,label,froggo):
        super().__init__(label)
        self.category = 'weapon'
        self.UI = False
        attack_direction = froggo.status.split('_')[0] #chcemy się pozbyć stanów idle z listy stanów tak by dostać tylko kierunek
        folder = f'../img/weapons/{froggo.weapon}/{attack_direction}.png'
        self.graphic = pygame.image.load(folder)
        #położenie broni
        if attack_direction == 'down':
            self.rect = self.graphic.get_rect(midtop = froggo.rect.midbottom + pygame.math.Vector2(-16,0)) #dodajemy shift na oko by broń była bliżej dloni
        elif attack_direction == 'up':
            self.rect = self.graphic.get_rect(midbottom = froggo.rect.midtop + pygame.math.Vector2(16,0))
        elif attack_direction == 'left':
            self.rect = self.graphic.get_rect(midright = froggo.rect.midleft + pygame.math.Vector2(4,20))
        elif attack_direction == 'right':
           self.rect = self.graphic.get_rect(midleft = froggo.rect.midright + pygame.math.Vector2(0,20))

class Spells:
    def __init__(self,animation_maker):
        self.category = 'spells'
        self.animation_maker = animation_maker
        self.sound_energy_ball = pygame.mixer.Sound('../sound/ball.wav')
        self.sound_heal = pygame.mixer.Sound('../sound/heal.wav')
        self.sound_heal.set_volume(0.1)

    def energy_ball(self,mana_cost,froggo,label):
        if froggo.mana >= mana_cost:
            froggo.mana -= mana_cost
            for i in range(1,4):
                shift_plus= i*TILESIZE
                shift_minus= -i*TILESIZE
                #rysujemy każdy kolejny sprite obok wczesniejszego (dlatego mnozymy kierunek z kolejnoscia, tzn. 1 lub -1)
                #ale samo mnozenie tych 2 sprawiloby ze bylyby o 1px obok wiec mnozymy jeszcze przez wielkosc kafelka
                self.animation_maker.create_elements('energy_ball',(froggo.rect.centerx+shift_plus,froggo.rect.centery),label)
                self.animation_maker.create_elements('energy_ball',(froggo.rect.centerx+shift_minus,froggo.rect.centery),label)
                self.animation_maker.create_elements('energy_ball',(froggo.rect.centerx,froggo.rect.centery+shift_plus),label)
                self.animation_maker.create_elements('energy_ball',(froggo.rect.centerx,froggo.rect.centery+shift_minus),label)
                self.animation_maker.create_elements('energy_ball',(froggo.rect.centerx+shift_minus,froggo.rect.centery+shift_minus),label)
                self.animation_maker.create_elements('energy_ball',(froggo.rect.centerx+shift_plus,froggo.rect.centery+shift_plus),label)
                self.animation_maker.create_elements('energy_ball',(froggo.rect.centerx+shift_plus,froggo.rect.centery+shift_minus),label)
                self.animation_maker.create_elements('energy_ball',(froggo.rect.centerx+shift_minus,froggo.rect.centery+shift_plus),label)
            self.sound_energy_ball.play()




    def cast_heal(self, mana_cost, strength, froggo, label):
        if froggo.mana >= mana_cost:
            froggo.mana -= mana_cost
            froggo.hp = min(froggo.hp + strength,froggo.stats['hp'])
            self.animation_maker.create_elements('heal',froggo.rect.center,label)
            self.sound_heal.play()

    def shield(self, mana_cost, froggo):
        if(froggo.mana >= mana_cost):
            if(froggo.coins >= 1):
                froggo.coins -= 1
                shield = Shield()
                shield.froggo = froggo
                shield.currentHealth=froggo.hp
                all_sprites.add(shield)
