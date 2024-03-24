import pygame
from settings import *
import random

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
            'mimic': folder_import('../img/enemies/mimic/idle'),
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

            
class Froga(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.font = pygame.font.Font(FONT, FONT_SIZE)
        WHITE = (255, 255, 255)
        self.UI = True
        self.froggo=None
        self.wait = 0
        self.say = "Hello"
        self.image = pygame.image.load("../img/froggo/frogga.png").convert_alpha()  # Load image with transparency
        self.rect = self.image.get_rect()  # Get the rectangle bounding the sprite
        self.graphic=self.image

    def update(self):
        if self.froggo.hitbox.x>self.rect.x-250 and self.froggo.hitbox.x<self.rect.x+270 and self.froggo.hitbox.y>self.rect.y-270 and self.froggo.hitbox.y<self.rect.y+250:
            self.wait+=1
            texter = ["Hello","How are you?","Nice day today.","Aren't you tired?","The mushrooms are restless.","I've planted these flowers myeself.","Are you gonna stay with me a while?", "I used to be an adventurer like you...","The island on the right seems scary.","It might rain tomorrow.","Is everything okay?","Good luck on your journey!","Take care.","You look well.","I'm always here for you.","I can hear the Wolves howling in the distance."]
            if self.wait>=110:
                self.say = texter[random.randint(0,len(texter)-1)]
                self.wait=0
            
            text_surface2 = self.font.render(self.say,False,COLOUR_TEXT)
            x= WIDTH/2 + self.rect.x - self.froggo.hitbox.x + 35
            y= HEIGHT/2 + self.rect.y - self.froggo.hitbox.y + 25
            text_rectangle2 = text_surface2.get_rect(topleft = (x,y+38))

            pygame.draw.rect(self.screen,COLOUR_UI_BG,text_rectangle2.inflate(30,25))
            self.screen.blit(text_surface2,text_rectangle2)
        pass  # You can implement sprite updates here if needed

            
class Shield(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.UI = True
        self.currentHealth = 0
        self.froggo=None
        self.wait = 0
        self.image = pygame.image.load("../img/weapons/shield.png").convert_alpha()  # Load image with transparency
        self.rect = self.image.get_rect()  # Get the rectangle bounding the sprite
        self.graphic=self.image

    def update(self):
        self.rect.topleft = [self.froggo.rect.topleft[0]+30,self.froggo.rect.topleft[1]+30]
        self.wait+=1
        self.froggo.hp = self.currentHealth
        if self.wait>160:
            if self.wait//5 % 2 == 0:
                self.image = pygame.image.load("../img/empty.png").convert_alpha() 
            else:
                self.image = pygame.image.load("../img/weapons/shield.png").convert_alpha() 
            self.graphic = self.image
            if self.wait>220:
                self.kill()
        pass  # You can implement sprite updates here if needed

class Drop(pygame.sprite.Sprite):
    def __init__(self,typer):
        super().__init__()
        WHITE = (255, 255, 255)
        self.UI = False
        self.froggo=None
        self.type=typer
        self.wait=0
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
        self.wait+=1
        if self.wait>=65:
            if self.wait//5 % 2 == 0:
                self.image = pygame.image.load("../img/empty.png").convert_alpha() 
            else:
                if self.type == "heart":
                    self.image = pygame.image.load("../img/other/heart.png").convert_alpha()  # Load image with transparency
                if self.type == "mana":
                    self.image = pygame.image.load("../img/other/manaREG.png").convert_alpha() 
                if self.type == "coin":
                    self.image = pygame.image.load("../img/other/coin.png").convert_alpha() 
            if self.wait>=130:
                self.kill()
            self.image = pygame.transform.scale(self.image, (40, 40)) 
            self.graphic = self.image
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

class Chest(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        WHITE = (255, 255, 255)
        self.UI = False
        self.froggo=None
        self.image = pygame.image.load("../img/enemies/mimic/idle/0.png").convert_alpha() 
        #self.image = pygame.transform.scale(self.image, (40, 40)) 
        self.rect = self.image.get_rect()  # Get the rectangle bounding the sprite
        self.graphic=self.image

    def update(self):
        if self.froggo.hitbox.x>self.rect.x-100 and self.froggo.hitbox.x<self.rect.x+120 and self.froggo.hitbox.y>self.rect.y-120 and self.froggo.hitbox.y<self.rect.y+100:
            player_image = pygame.image.load("../img/flowers/flower_3.png").convert_alpha()  # Load image with transparency
            player_sprite =     Drop("coin")
            player_sprite.rect.topleft=self.rect.topleft
            player_sprite.image = player_image
            all_sprites.add(player_sprite)

            player_sprite =     Drop("coin")
            player_sprite.rect.topleft=(self.rect.x+30,self.rect.y+20)
            player_sprite.image = player_image
            all_sprites.add(player_sprite)

            player_sprite =     Drop("coin")
            player_sprite.rect.topleft=(self.rect.x+60,self.rect.y-20)
            player_sprite.image = player_image
            all_sprites.add(player_sprite)
            self.kill()
        pass  # You can implement sprite updates here if needed
            
