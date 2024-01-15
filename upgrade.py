import pygame
from settings import *


class Upgrade:
    def __init__(self,froggo):

        self.screen = pygame.display.get_surface()
        self.froggo = froggo
        self.attribute_list = []
        self.max_values = list(froggo.max_stats.values())
        self.font = pygame.font.Font(FONT,FONT_SIZE)

        #system wyboru
        self.switch_attribute = True
        self.timer = None
        self.selected_index = 0

        #rozmiar itp
        self.height = self.screen.get_size()[1] *0.8 #cały ekran i 20%
        self.width = self.screen.get_size()[0] // 7 #5 statystyk postaci + 2 (to dwa to będzie dodatkowe miejsce dla pasków zeby nie byly scisniete)

        for item, index in enumerate(range(len(self.froggo.stats))):
            shift = self.screen.get_size()[0] // len(self.froggo.stats)
            #tworzymy obiekty i dodajemy do listy
            self.attribute_list.append(Attribute((item * shift) + .5*(shift-self.width),self.screen.get_size()[1]*0.1,self.width,self.height,index,self.font))


    def show_upgrade(self):
        for index, item in enumerate(self.attribute_list):
            item.show_attribute(self.screen, self.selected_index, list(self.froggo.stats.keys())[index],
                         list(self.froggo.stats.values())[index], self.max_values[index], list(self.froggo.upgrade_cost.values())[index])
        keys = pygame.key.get_pressed()

        if self.switch_attribute:
            if keys[pygame.K_UP]:
                self.timer = pygame.time.get_ticks()
                self.switch_attribute = False
                self.attribute_list[self.selected_index].trigger(self.froggo)
            if keys[pygame.K_RIGHT] and self.selected_index < len(self.froggo.stats) - 1:
                self.timer = pygame.time.get_ticks()
                self.selected_index += 1
                self.switch_attribute = False
            elif keys[pygame.K_LEFT] and self.selected_index > 0:
                self.timer = pygame.time.get_ticks()
                self.selected_index -= 1
                self.switch_attribute = False
        if not self.switch_attribute:
            current_time = pygame.time.get_ticks()
            if current_time - self.timer >= 400:
                self.switch_attribute = True



class Attribute:
    def __init__(self,left,top,width,height,index,font):
        self.rect = pygame.Rect(left,top,width,height)
        self.index = index
        self.font = font

    def show_bar(self,surface,value,max_value,selected):
        top = self.rect.midtop + pygame.math.Vector2(0,60)
        bottom = self.rect.midbottom - pygame.math.Vector2(0,60)
        colour = COLOUR_BAR_SELECTED if selected else COLOUR_BAR

        full_height = bottom[1] - top[1]
        present_level = (value/max_value) * full_height
        value_rect = pygame.Rect(top[0] - 15,bottom[1]-present_level,30,10) #left,top,width,height,15 bo polowa 30
        #present_level to ile od paska aktualnego ulepszenia jest w doł do spodu
        pygame.draw.line(surface,colour,top,bottom,5)
        pygame.draw.rect(surface,colour,value_rect)


    def trigger(self,froggo):
        upgrade_attribute = list(froggo.stats.keys())[self.index]

        if froggo.xp >= froggo.upgrade_cost[upgrade_attribute] and froggo.stats[upgrade_attribute] < froggo.max_stats[upgrade_attribute]:
            froggo.xp -= froggo.upgrade_cost[upgrade_attribute]
            froggo.stats[upgrade_attribute] *= 1.2
            froggo.upgrade_cost[upgrade_attribute] *= 1.4

        if froggo.stats[upgrade_attribute] > froggo.max_stats[upgrade_attribute]:
            froggo.stats[upgrade_attribute] = froggo.max_stats[upgrade_attribute]

    def show_attribute(self,surface,selection_num,name,value,max_value,cost):
        #kolor wybranego atrybutu
        colour_text = COLOUR_TEXT_SELECTED if self.index == selection_num else COLOUR_TEXT_UPGRADE
        colour_bar = COLOUR_BAR_SELECTED if self.index == selection_num else COLOUR_BAR
        #koszt
        cost_surface = self.font.render(f'{int(cost)}',False,colour_text) #int bo jest szansa ze koszt bedzie floatem a potem zmieniamy w f stringa
        cost_rect = cost_surface.get_rect(midbottom = self.rect.midbottom - pygame.math.Vector2(0,20))

        if self.index == selection_num:
            pygame.draw.rect(surface,COLOUR_UPGRADE_SELECTED,self.rect)
            pygame.draw.rect(surface,'white',self.rect,4)
        else:
            pygame.draw.rect(surface,COLOUR_UPGRADE,self.rect)
            pygame.draw.rect(surface,'black',self.rect,4)
            
        top = self.rect.midtop + pygame.math.Vector2(0,60)
        bottom = self.rect.midbottom - pygame.math.Vector2(0,60)
        full_height = bottom[1] - top[1]
        present_level = (value/max_value) * full_height
        value_rect = pygame.Rect(top[0] - 15,bottom[1]-present_level,30,10) #left,top,width,height,15 bo polowa 30
        #present_level to ile od paska aktualnego ulepszenia jest w doł do spodu

        #tytuły
        title_surface = self.font.render(name,False,colour_text)
        title_rect = title_surface.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0,20))
        #rysujemy
        surface.blit(title_surface,title_rect)
        surface.blit(cost_surface,cost_rect)

        #pokazywanie paskow
        pygame.draw.line(surface,colour_bar,top,bottom,5)
        pygame.draw.rect(surface,colour_bar,value_rect)
