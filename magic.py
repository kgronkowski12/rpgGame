import pygame
from settings import *

class MagicPlayer:
    def __init__(self,animation_player):
        self.animation_player = animation_player


    def heal(self,player,strength,cost,groups):
        if player.energy >= cost:
            player.health += strength
            player.energy -= cost
            if player.health >= player.stats['health']:
                player.health = player.stats['health']
            self.animation_player.create_particles('heal',player.rect.center,groups)


    def flame(self,player,cost,groups):
        if player.energy >= cost:
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
                    offset_x= (direction.x*i)* TILESIZE 
                    #rysujemy każdy kolejny sprite obok wczesniejszego (dlatego mnozymy kierunek z kolejnoscia)
                    #ale samo mnozenie tych 2 sprawiloby ze bylyby o 1px obok wiec mnozymy jeszcze przez wielkosc kafelka
                    x = player.rect.centerx +offset_x
                    y = player.rect.centery
                    self.animation_player.create_particles('flame',(x,y),groups)
                else:
                    offset_y = (direction.y*i)* TILESIZE
                    x = player.rect.centerx
                    y = player.rect.centery + offset_y
                    self.animation_player.create_particles('flame',(x,y),groups)
