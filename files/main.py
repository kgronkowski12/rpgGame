import pygame
import sys
from settings import *
from world import World

class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH,HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Froggo Adventure')
        self.world = World()

        #muzyka
        main_sound = pygame.mixer.Sound('../sound/song.wav')
        main_sound.play(loops = -1)
        main_sound.set_volume(0.35)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() #możliwość wyłączenia gry bez erroru
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LSHIFT:
                        self.world.toggle_menu()
                    if event.key == pygame.K_r:
                        pygame.mixer.quit()
                        game = Game()
                        game.run()
 
            self.window.fill(COLOUR_BACKGROUND)
            self.world.run()
            self.clock.tick(FPS)
            for x in all_sprites:
                x.froggo=self.world.froggo
                self.world.visable_sprites.add(x)
                all_sprites.remove(x)
            #all_sprites.draw(self.window)
            #all_sprites.update()
            pygame.display.update()
 
if __name__ == '__main__':
    game = Game()
    game.run()
