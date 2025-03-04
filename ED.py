import pygame
import os
import random
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 600
class EndIMG(pygame.sprite.Sprite):
    """ Object that tells you the stage is over (unused, needs to be removed or reworked) """
 
    def __init__(self, width, height):
        super().__init__()
 
        self.image = pygame.image.load(os.path.join('blockimages', "End.gif")).convert()
 
        self.rect = self.image.get_rect()
    
