import pygame
class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height):
        """ You can do stuff on it. """
        self.message = ""
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.type = "blank"
        self.moves = 0
        self.rect = self.image.get_rect()
        
