import pygame

# Colors (These could be moved to a separate config file for better organization)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


class Level:  #Changed to class Level to prevent name conflict with LevelList import
    def __init__(self, player):
        self.player = player
        self.world_shift_x = 0
        self.world_shift_y = 0
        self.sprite_groups = {
            "platforms": pygame.sprite.Group(),
            "image_platforms": pygame.sprite.Group(),
            "enemies": pygame.sprite.Group(),
            "end_points": pygame.sprite.Group(),
            "push_blocks": pygame.sprite.Group(),
        }

    def update(self):
        for group in self.sprite_groups.values():
            group.update()

    def draw(self, screen):
        screen.fill(BLACK)  #Fill with background color
        for group in self.sprite_groups.values():
            group.draw(screen)

    def shift_world(self, dx, dy):
        self.world_shift_x += dx
        self.world_shift_y += dy
        for group_name, group in self.sprite_groups.items():
            for sprite in group:
                sprite.rect.x += dx
                sprite.rect.y += dy