import pygame
import sys
from settings import *
from world import World

class Game:
    def __init__(self):          
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption('TEST TITLE')
        self.clock = pygame.time.Clock()
    
        self.level = World()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() #możliwość wyłączenia gry bez erroru
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_u:
                        self.level.toggle_menu()
 
            self.screen.fill('black')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)
 
if __name__ == '__main__':
    game = Game()
    game.run()
