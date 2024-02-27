import pygame
from settings import *

class UI:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.font = pygame.font.Font(FONT,FONT_SIZE)
        #konwertowanie słownika z czarami
        self.spells_graphics = []
        for spells in INFO_SPELLS.values():
            spells = pygame.image.load(spells['graphic'])
            self.spells_graphics.append(spells)
        #to samo ale bronie
        self.weapon_graphics = []
        for weapon in INFO_WEAPONS.values():
            folder = weapon['graphic']
            weapon = pygame.image.load(folder)
            self.weapon_graphics.append(weapon)
        #paski i statystyki
        bar_x = 8
        bar_y = 685
        self.health_bar = pygame.Rect(bar_x,bar_y-17,BAR_WIDTH,BAR_HEIGHT)
        self.mana_bar = pygame.Rect(bar_x,bar_y,BAR_WIDTH,BAR_HEIGHT)

    def controls(self):
        c = "Coins: "+str(coinCount)
        coin_surface = self.font.render(str(c),False,COLOUR_TEXT)
        text_surface = self.font.render(str('Sterowanie:                     '),False,COLOUR_TEXT)
        text_surface2 = self.font.render(str('poruszanie sie - strzalki    '),False,COLOUR_TEXT)
        text_surface3 = self.font.render(str('magia - w                        '),False,COLOUR_TEXT)        
        text_surface4 = self.font.render(str('zmiana broni/magii - a/d  '),False,COLOUR_TEXT)        
        text_surface5 = self.font.render(str('menu ulepszen - lewy shift'),False,COLOUR_TEXT)
        #na oko wyliczone                
        x=1045
        y=545
        text_rectangle6 = coin_surface.get_rect(topleft = (x+150,0))
        text_rectangle = text_surface.get_rect(topleft = (x,y))
        text_rectangle2 = text_surface2.get_rect(topleft = (x,y+38))
        text_rectangle3 = text_surface3.get_rect(topleft = (x,y+76))
        text_rectangle4 = text_surface4.get_rect(topleft = (x,y+114))
        text_rectangle5 = text_surface5.get_rect(topleft = (x,y+152))

        pygame.draw.rect(self.screen,COLOUR_UI_BG,text_rectangle.inflate(20,20))
        self.screen.blit(text_surface,text_rectangle)

        pygame.draw.rect(self.screen,COLOUR_UI_BG,text_rectangle2.inflate(20,20))
        self.screen.blit(text_surface2,text_rectangle2)

        pygame.draw.rect(self.screen,COLOUR_UI_BG,text_rectangle3.inflate(20,20))
        self.screen.blit(text_surface3,text_rectangle3)

        pygame.draw.rect(self.screen,COLOUR_UI_BG,text_rectangle4.inflate(20,20))
        self.screen.blit(text_surface4,text_rectangle4)

        pygame.draw.rect(self.screen,COLOUR_UI_BG,text_rectangle5.inflate(20,20))
        self.screen.blit(text_surface5,text_rectangle5)

        c = "Coins: "+str(coinCount)
        coin_surface = pygame.font.Font(FONT,FONT_SIZE).render(str(c),False,COLOUR_TEXT)
        text_rectangle6 = coin_surface.get_rect(topleft = (x+150,0))
        pygame.draw.rect(pygame.display.get_surface(),COLOUR_UI_BG,text_rectangle6.inflate(20,20))
        self.screen.blit(coin_surface,text_rectangle6)



    def xp(self,xp):
        surface = self.font.render(str(int(xp)),False,COLOUR_TEXT)
        rectangle = surface.get_rect(topleft = (18,568))
        pygame.draw.rect(self.screen,COLOUR_UI_BG,rectangle.inflate(20,20))
        self.screen.blit(surface,rectangle)


    def bar(self,froggo):

        #życie
        pygame.draw.rect(self.screen,COLOUR_UI_BG,self.health_bar)
        width1 = self.health_bar.width * (froggo.hp/froggo.stats['hp']) #pasek 200px*1 ratio =200px (wiec caly pasek jest wypelniony zyciem)
        rectangle1 = self.health_bar.copy() #juz wiekszosc info jest w health_bar wiec to kopiuje po prostu
        rectangle1.width = width1
        pygame.draw.rect(self.screen,COLOUR_HEALTH,rectangle1)
        pygame.draw.rect(self.screen,COLOUR_UI_BORDER,self.health_bar,4)

        #mana
        pygame.draw.rect(self.screen,COLOUR_UI_BG,self.mana_bar)
        current_width2 = self.mana_bar.width * (froggo.mana/froggo.stats['mana'])
        current_rectangle2 = self.mana_bar.copy()
        current_rectangle2.width = current_width2
        pygame.draw.rect(self.screen,COLOUR_MANA,current_rectangle2)
        pygame.draw.rect(self.screen,COLOUR_UI_BORDER,self.mana_bar,4)

    def combat_square(self,index_spell,index_weapon):
        square1 = pygame.Rect(8,600,BOX,BOX)
        pygame.draw.rect(self.screen,COLOUR_UI_BG,square1)
        surface1 = self.weapon_graphics[index_weapon]
        rectangle1 = surface1.get_rect(center = square1.center)
        self.screen.blit(surface1,rectangle1)

        square2 = pygame.Rect(73,600,BOX,BOX)
        pygame.draw.rect(self.screen,COLOUR_UI_BG,square2)
        surface2 = self.spells_graphics[index_spell]
        rectangle2 = surface2.get_rect(center = square2.center)
        self.screen.blit(surface2,rectangle2)
    


    def display(self,froggo):
        self.controls()
        self.xp(froggo.xp)
        self.bar(froggo)
        self.combat_square(froggo.spells_index,froggo.weapon_index)
