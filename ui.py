import pygame
from settings import *

class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(FONT_UI,FONT_UI_SIZE)

        #paski i statystyki
        self.health_bar_rect = pygame.Rect(8,668,BAR_WIDTH,BAR_HEIGHT)
        self.mana_bar_rect = pygame.Rect(8,685,BAR_WIDTH,BAR_HEIGHT)

        #konwertowanie słownika z broniami
        self.weapon_graphics = []
        for weapon in info_weapons.values():
            path = weapon['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)

        self.magic_graphics = []
        for magic in info_magic.values():
            magic = pygame.image.load(magic['graphic']).convert_alpha()
            self.magic_graphics.append(magic)

    def show_bar(self,current,max_amount,bg_rect,colour):
        #tło dla paska
        pygame.draw.rect(self.display_surface,COLOUR_UI_BG,bg_rect)
        #konwertowanie statystyk do pikseli
        ratio = current / max_amount #np obecne zycie/max zycie 100/100 = 1
        current_width = bg_rect.width * ratio #pasek 200px*1 ratio =200px (wiec caly pasek jest wypelniony zyciem)
        current_rect = bg_rect.copy() #juz wiekszosc info jest w bg_rect wiec to kopiuje po prostu
        current_rect.width = current_width
        #rysujemy pasek
        pygame.draw.rect(self.display_surface,colour,current_rect)
        pygame.draw.rect(self.display_surface,COLOUR_UI_BORDER,bg_rect,4) #ostatni argument (4) sprawia że pozbywamy się wypełnienia i zostaje
        #tylko krawędź na tyle duża jaką liczbę podaliśmy

    def show_xp(self,xp):
        text_surf = self.font.render(str(int(xp)),False,COLOUR_TEXT) #false bo zadnego anty aliasingu nie chcemy bo mamy pixelart DOCH
        #xp zmieniamy w str bo to ma byc info ale wczesniej na inta zeby sie pozbyc ewentualnych dziwnych koncowek np 4.12341242 w xpie
        x = self.display_surface.get_size()[0] - 1262
        y = self.display_surface.get_size()[1] - 152
        text_rect = text_surf.get_rect(topleft = (x,y))
        
        pygame.draw.rect(self.display_surface,COLOUR_UI_BG,text_rect.inflate(20,20))
        self.display_surface.blit(text_surf,text_rect)
        pygame.draw.rect(self.display_surface,COLOUR_UI_BORDER,text_rect.inflate(20,20),3)

    def selection_box(self,left,top,has_switched):
        bg_rect = pygame.Rect(left,top,BOX,BOX)
        pygame.draw.rect(self.display_surface,COLOUR_UI_BG,bg_rect)
        return bg_rect

    def weapon_overlay(self,weapon_index,has_switched):
        bg_rect = self.selection_box(8,600,has_switched) # broń
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center = bg_rect.center)

        self.display_surface.blit(weapon_surf,weapon_rect)

    
    def magic_overlay(self,magic_index,has_switched):
        bg_rect = self.selection_box(73,600,has_switched) # magia
        magic_surf = self.magic_graphics[magic_index]
        magic_rect = magic_surf.get_rect(center = bg_rect.center)
        self.display_surface.blit(magic_surf,magic_rect)


    def display(self,player):
        self.show_bar(player.hp,player.stats['hp'],self.health_bar_rect,COLOUR_HEALTH)
        self.show_bar(player.mana,player.stats['mana'],self.mana_bar_rect,COLOUR_MANA)

        self.show_xp(player.xp)
        self.weapon_overlay(player.weapon_index,not player.can_switch_weapon)
        self.magic_overlay(player.magic_index, not player.can_switch_magic)
