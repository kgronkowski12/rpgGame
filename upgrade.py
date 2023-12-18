from math import cos
import pygame
from settings import *


class Upgrade:
    def __init__(self,player):

        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.attribute_nr = len(player.stats) #ilość statystyk gracza
        self.attribute_names = list(player.stats.keys())
        self.max_values = list(player.max_stats.values())
        self.font = pygame.font.Font(FONT_UI,FONT_UI_SIZE)

        #rozmiar itp
        self.height = self.display_surface.get_size()[1] *0.8 #cały ekran i 20%
        self.width = self.display_surface.get_size()[0] // 6 #5 statystyk postaci + 1 (to jeden to będzie dodatkowe miejsce dla pasków zeby nie byly scisniete)
        self.create_items()


        #system wyboru
        self.selection_index = 0
        self.selection_time = None
        self.can_move = True

    def player_input(self):
        keys = pygame.key.get_pressed()

        if self.can_move:
            if keys[pygame.K_RIGHT] and self.selection_index < self.attribute_nr - 1:
                self.selection_index += 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_LEFT] and self.selection_index > 0:
                self.selection_index -= 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
        
            if keys[pygame.K_UP]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                self.item_list[self.selection_index].trigger(self.player)

    def selection_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 300:
                self.can_move = True


    def create_items(self):
        self.item_list = []

        for item, index in enumerate(range(self.attribute_nr)):
            full_width = self.display_surface.get_size()[0]
            increment = full_width // self.attribute_nr
            left = (item * increment) + (increment-self.width) //2 #kazdy element obok bedzie mial delikatny shift
            top = self.display_surface.get_size()[1]*0.1
            #ustalilismy ze chcemy 80% ekranu, czyli 10% na dole i 10 na gorze to bedzie wolne miejsce
            #jako że potrzeba nam po prostu punktu na gorze od ktorego rysujemy
            #bierzemy 10% całego rozmiaru ekranu
            item = Item(left,top,self.width,self.height,index,self.font)
            self.item_list.append(item)


    def display(self):
        self.player_input()
        self.selection_cooldown()

        for index, item in enumerate(self.item_list):
            name = self.attribute_names[index]
            value = self.player.get_value_by_index(index)
            max_value = self.max_values[index]
            cost = self.player.get_cost_by_index(index)
            item.display(self.display_surface,self.selection_index,name,value,max_value,cost)


class Item:
    def __init__(self,left,top,width,height,index,font):
        self.rect = pygame.Rect(left,top,width,height)
        self.index = index
        self.font = font

    def display_names(self,surface,name,cost,selected):
        colour = COLOUR_TEXT_SELECTED if selected else COLOUR_TEXT_UPGRADE

        #tytuły
        title_surf = self.font.render(name,False,colour)
        title_rect = title_surf.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0,20))

        #koszt
        cost_surf = self.font.render(f'{int(cost)}',False,colour) #int bo jest szansa ze koszt bedzie floatem a potem zmieniamy w f stringa
        cost_rect = cost_surf.get_rect(midbottom = self.rect.midbottom - pygame.math.Vector2(0,20))

        #rysujemy
        surface.blit(title_surf,title_rect)
        surface.blit(cost_surf,cost_rect)

    def display_bar(self,surface,value,max_value,selected):
        top = self.rect.midtop + pygame.math.Vector2(0,60)
        bottom = self.rect.midbottom - pygame.math.Vector2(0,60)
        colour = COLOUR_BAR_SELECTED if selected else COLOUR_BAR

        full_height = bottom[1] - top[1]
        relative_number = (value/max_value) * full_height
        value_rect = pygame.Rect(top[0] - 15,bottom[1]-relative_number,30,10) #left,top,width,height,15 bo polowa 30
        #relative to ile od paska aktualnego ulepszenia jest w doł do spodu
        pygame.draw.line(surface,colour,top,bottom,5)
        pygame.draw.rect(surface,colour,value_rect)


    def trigger(self,player):
        upgrade_attribute = list(player.stats.keys())[self.index]

        if player.xp >= player.upgrade_cost[upgrade_attribute] and player.stats[upgrade_attribute] < player.max_stats[upgrade_attribute]:
            player.xp -= player.upgrade_cost[upgrade_attribute]
            player.stats[upgrade_attribute] *= 1.2
            player.upgrade_cost[upgrade_attribute] *= 1.4

        if player.stats[upgrade_attribute] > player.max_stats[upgrade_attribute]:
            player.stats[upgrade_attribute] = player.max_stats[upgrade_attribute]

    def display(self,surface,selection_num,name,value,max_value,cost):
        if self.index == selection_num:
            pygame.draw.rect(surface,COLOUR_UPGRADE_BG_SELECTED,self.rect)
            pygame.draw.rect(surface,'white',self.rect,4)
        else:
            pygame.draw.rect(surface,COLOUR_UPGRADE_BG,self.rect)
            pygame.draw.rect(surface,'black',self.rect,4)
        self.display_names(surface,name,cost,self.index == selection_num)
        self.display_bar(surface,value,max_value,self.index == selection_num)
