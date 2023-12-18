import pygame
import sys
from settings import *
from world import World

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Froggo Adventure')
        self.world = World()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() #możliwość wyłączenia gry bez erroru
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LSHIFT:
                        self.world.toggle_menu()
 
            self.screen.fill(COLOUR_BACKGROUND)
            self.world.run()
            self.clock.tick(FPS)
            pygame.display.update()
 
if __name__ == '__main__':
    game = Game()
    game.run()
