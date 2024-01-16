import pygame
from settings import folder_import

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
