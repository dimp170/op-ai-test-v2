import pygame
from LVLDAT import Level
from PlatformOBJ import Platform

class GameOverLevel(Level):  # More descriptive name
    def __init__(self, player):
        Level.__init__(self, player)
        self.level_limit = -250000
        self.platform_data = [
            [10, 1000, 0, 1000, ""],  # width, height, x, y, type
            [100, 100, 0, 380, ""],
            [100, 100, 100, 380, "up"],
            [100, 100, 200, 380, "down"],
            [100, 100, 300, 380, ""],
        ]
        self.create_platforms()

    def create_platforms(self):
        for platform_data in self.platform_data:
            width, height, x, y, block_type = platform_data
            block = Platform(width, height)
            block.rect.x = x
            block.rect.y = y
            block.type = block_type
            block.player = self.player # This line might need to be removed or handled differently
            self.platform_list.add(block)