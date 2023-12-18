import pygame
from settings import *

class Weapon(pygame.sprite.Sprite):
    def __init__(self,player,group):
        super().__init__(group)
        self.label_sprite = 'weapon'
        direction = player.status.split('_')[0] #chcemy się pozbyć stanów idle z listy stanów tak by dostać tylko kierunek
        full_path = f'../img/weapons/{player.weapon}/{direction}.png'
        self.image = pygame.image.load(full_path).convert_alpha()

        #położenie broni
        if direction == 'down':
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(-10,0)) #dodajemy shift by broń była bliżej dloni
        elif direction == 'up':
            self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(16,0))
        elif direction == 'left':
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(4,20))
        else:
           self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0,20))

class MagicPlayer:
    def __init__(self,animation_player):
        self.animation_player = animation_player
        self.sound_heal = pygame.mixer.Sound('../sound/heal.wav')
        self.sound_flame = pygame.mixer.Sound('../sound/Fire.wav')


    def heal(self,player,strength,mana_cost,group):
        if player.mana >= mana_cost:
            self.sound_heal.play()
            player.hp += strength
            player.mana -= mana_cost
            if player.hp >= player.stats['hp']:
                player.hp = player.stats['hp']
            self.animation_player.create_elements('heal',player.rect.center,group)


    def flame(self,player,mana_cost,group):
        if player.mana >= mana_cost:
            player.mana -= mana_cost
            self.sound_flame.play()
            #bierzemy listę stanow gracza i dzielimy je jesli jest right idle np, i patrzymy tylko na 1 rzecz (kierunek)
            if player.status.split('_')[0] == 'right':
                direction = pygame.math.Vector2(1,0)
            elif player.status.split('_')[0] == 'left':
                direction = pygame.math.Vector2(-1,0)
            elif player.status.split('_')[0] == 'up':
                direction = pygame.math.Vector2(0,-1)
            else:
                direction = pygame.math.Vector2(0,1)

            for i in range(1,6):
                if direction.x:
                    shift_x= (direction.x*i)* TILESIZE 
                    #rysujemy każdy kolejny sprite obok wczesniejszego (dlatego mnozymy kierunek z kolejnoscia)
                    #ale samo mnozenie tych 2 sprawiloby ze bylyby o 1px obok wiec mnozymy jeszcze przez wielkosc kafelka
                    x = player.rect.centerx +shift_x
                    y = player.rect.centery
                    self.animation_player.create_elements('flame',(x,y),group)
                else:
                    shift_y = (direction.y*i)* TILESIZE
                    x = player.rect.centerx
                    y = player.rect.centery + shift_y
                    self.animation_player.create_elements('flame',(x,y),group)
