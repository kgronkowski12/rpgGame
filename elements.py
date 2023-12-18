import pygame
from settings import folder_import

class AnimationMaker:
    def __init__(self):
        self.frames = {
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
            'flame': folder_import('../img/elements/ball/frames'),
            'heal': folder_import('../img/elements/heal/frames')           
        }

    def create_elements(self,animation_type,position,group):
        animation_frames = self.frames[animation_type]
        ElementEffect(position,animation_frames,group)

    def create_flowers_elements(self,position,group):
        animation_frames = self.frames['flowers']
        ElementEffect(position,animation_frames,group)
        

class ElementEffect(pygame.sprite.Sprite):
    def __init__(self, position, animation_frames,group):
        super().__init__(group)
        self.label_sprite = 'magic'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = position)


    def create_animation(self): #zwiększamy indeks klatki, jeśli wyjdziemy poza długość listy klatek to 'zabijamy' naszego sprite'a
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.create_animation()
