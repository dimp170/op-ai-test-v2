import pygame
from LVLDAT import Level
from PlatformOBJ import Platform
from PlatformImageOBJ import PlatformImage
from PlayerCharacter import Player
import random

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 100, 100)
PURPLE = (255, 0, 255)
GRAY = (100, 100, 100)


class Level_02(Level):
    def __init__(self, player):
        Level.__init__(self, player)
        self.level_limit = -2500
        self.level_data = self.load_level_data()
        self.create_platforms()


    def load_level_data(self):
        return [
            [1, 1, 0, 0, "spawn"],
            [8, 1, 1, 0, "normal"],
            [1, 10, 9, 0, "normal"],
            [25, 1, 5, 5, "normal"],
            [25, 1, 30, 5, "bouncy"],
            [4, 8, 55, 5, "down"],
            [11, 8, 59, 3, "up"],
        ]

    def create_platforms(self):
        for platform_data in self.level_data:
            width, height, x, y, block_type = platform_data
            for row in range(height):
                for col in range(width):
                    block = self.create_block(block_type, x + col, y + row)
                    self.platform_list.add(block)

    def create_block(self, block_type, x, y):
        block = Platform(100, 100) #Adjust size as needed
        block.rect.x = x * 100 #Adjust size as needed
        block.rect.y = y * 100 #Adjust size as needed
        block.type = block_type
        # Set colors based on block type (This could be improved by using images instead of colors)
        if block_type == "up":
            block.image.fill(GREEN)
        elif block_type == "down":
            block.image.fill(RED)
        elif block_type == "bouncy":
            block.image.fill(BLUE)
        elif block_type == "" or block_type == "normal":
            block.image.fill(WHITE)
        elif block_type.startswith("pull"):
            block.image.fill(GRAY)
        elif block_type == "spawn":
            block.image.fill(PURPLE)
            # self.player.rect.bottom = block.rect.top  #Handle this differently, maybe in a global game function
        return block