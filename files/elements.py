import pygame
from settings import *

class AnimationMaker:
    def __init__(self):
        self.frame_sequence = {
            #ataki
            'bite': folder_import('../img/elements/bite'),
            'cut': folder_import('../img/elements/cut'),
            'bone': folder_import('../img/elements/bone'),
            #śmierci
            'bear_dog': folder_import('../img/elements/bear_dog'),
            'mushroom': folder_import('../img/elements/mushroom'),
            'skeletor': folder_import('../img/elements/skeletor'),
            'flowers': folder_import('../img/elements/leaf'),
            #magia
            'energy_ball': folder_import('../img/elements/ball/frames'),
            'heal': folder_import('../img/elements/heal/frames')           
        }

    def create_elements(self,animation_type,position,label):
        Elements(label, self.frame_sequence[animation_type], position)
        if animation_type == "flowers":
            Elements(label,self.frame_sequence['flowers'], position)        

class Elements(pygame.sprite.Sprite):
    def __init__(self, label, frame_sequence, position):
        super().__init__(label)
        self.UI = False
        self.current_index = 0
        self.category = 'spells'
        self.frame_sequence = frame_sequence
        self.graphic = self.frame_sequence[self.current_index]
        self.rect = self.graphic.get_rect(center = position)

    def update(self):
        self.current_index += .2 #.2 to nasz frame_rate
        if self.current_index >= len(self.frame_sequence): #zwiększamy indeks klatki, jeśli wyjdziemy poza długość listy klatek to 'zabijamy' naszego sprite'a
            self.kill()
        else:
            self.graphic = self.frame_sequence[int(self.current_index)]
            
from settings import *
class Drop(pygame.sprite.Sprite):
    def __init__(self,typer):
        super().__init__()
        WHITE = (255, 255, 255)
        self.UI = False
        self.froggo=None
        self.type=typer
        if self.type == "heart":
            self.image = pygame.image.load("../img/other/heart.png").convert_alpha()  # Load image with transparency
        if self.type == "mana":
            self.image = pygame.image.load("../img/other/manaREG.png").convert_alpha() 
        if self.type == "coin":
            self.image = pygame.image.load("../img/other/coin.png").convert_alpha() 
        self.image = pygame.transform.scale(self.image, (40, 40)) 
        self.rect = self.image.get_rect()  # Get the rectangle bounding the sprite
        self.graphic=self.image

    def update(self):
        if self.froggo.hitbox.x>self.rect.x-50 and self.froggo.hitbox.x<self.rect.x+70 and self.froggo.hitbox.y>self.rect.y-70 and self.froggo.hitbox.y<self.rect.y+50:
            if self.type == "heart":
                self.froggo.hp+=25
                if self.froggo.hp>self.froggo.stats['hp']:
                    self.froggo.hp = self.froggo.stats['hp']
            if self.type == "mana":
                self.froggo.mana+=25
                if self.froggo.mana>self.froggo.stats['mana']:
                    self.froggo.mana = self.froggo.stats['mana']
            if self.type == "coin":
                self.froggo.coins+=1
            self.kill()
        pass  # You can implement sprite updates here if needed

class Talk(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.font = pygame.font.Font(FONT, FONT_SIZE+6)
        WHITE = (255, 255, 255)
        self.UI = True
        self.froggo=None
        self.image = pygame.image.load("../img/other/dialog.jpg").convert_alpha()  # Load image with transparency

        self.image = pygame.transform.scale(self.image, (1330, 1000))
        self.rect = self.image.get_rect()  # Get the rectangle bounding the sprite
        self.graphic=self.image

    def update(self):
        self.rect.x = self.froggo.hitbox.x - 800
        self.rect.y = self.froggo.hitbox.y - 1150
        if self.froggo.talking==0:
            self.kill()

        text_surface2 = self.font.render(str('Woof Woof    '),False,COLOUR_TEXT)
        #na oko wyliczone
        x=350
        y=-25
        text_rectangle2 = text_surface2.get_rect(topleft = (x,y+38))

        pygame.draw.rect(self.screen,COLOUR_UI_BG,text_rectangle2.inflate(300,200))
        self.screen.blit(text_surface2,text_rectangle2)
        pass  # You can implement sprite updates here if needed

            
