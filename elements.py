import pygame
from post import import_folder
from random import choice

class AnimationPlayer:
    def __init__(self):
        self.frames = {
            #magia
            'flame': import_folder('../img/elements/ball/frames'),
            'heal': import_folder('../img/elements/heal/frames'),
            #ataki
            'bite': import_folder('../img/elements/bite'),
            'cut': import_folder('../img/elements/cut'),
            'bone': import_folder('../img/elements/bone'),
            #smierci wrogow
            'bear_dog': import_folder('../img/elements/bear_dog'),
            'mushroom': import_folder('../img/elements/mushroom'),
            'skeletor': import_folder('../img/elements/skeletor'),

            'leaf':(
                import_folder('../img/elements/leaf'),
                self.reflect_images(import_folder('../img/elements/leaf'))
            )
        }
    
    
    def reflect_images(self,frames):
        new_frames = []
        for frame in frames:
            flipped_frame = pygame.transform.flip(frame,True,False)
            new_frames.append(flipped_frame)
        return new_frames
    
    def create_grass_particles(self,pos,groups):
        animation_frames = choice(self.frames['leaf'])
        ParticleEffect(pos,animation_frames,groups)


    def create_particles(self,animation_type,pos,groups):
        animation_frames = self.frames[animation_type]
        ParticleEffect(pos,animation_frames,groups)
        


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames,groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)


    def animate(self): #zwiększamy indeks klatki, jeśli wyjdziemy poza długość listy
        #klatek to 'zabijamy' naszego sprite'a
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()