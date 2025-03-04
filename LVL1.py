import pygame
from LVLDAT import Level
from Levels.Objects.ObjectList import *
import random
import os

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 100, 100)
PURPLE = (255, 0, 255)
GRAY = (100, 100, 100)

# Dictionary mapping block types to image filenames
BLOCK_IMAGES = {
    "spawn": "spawnTile.PNG",
    "up": "moveUpTile.PNG",
    "down": "moveDownTile.PNG",
    "bouncy": "moveBounceTile.PNG",
    "normal": "floorTile.PNG",
    "push": "moveDownTile.PNG", #Using the same image as down for now
    "pullup": "pullTile.PNG",
    "pulldown": "pullTile.PNG",
    "pullleft": "pullTile.PNG",
    "pullright": "pullTile.PNG",
    "message": "setMessageTile.PNG",
    "enablemessages": "setEnableTile.PNG",
    "disablemessages": "setDisableTile.PNG",
    "suffer":"sufferTile.PNG",
    "flyingplatform": "FlyingPlatform.PNG",
    "developer":"Dr RNG 3.PNG",
}


class Level_01(Level):
    def __init__(self, player):
        Level.__init__(self, player)
        self.level_limit = -2500
        self.level_data = [  #Level data as a list of lists
            [1, 11, -1, -22, "normal"],
            [1, 11, 4, -24, "normal"],
            [1, 1, -5, 0, "pullup"],
            # ... rest of your level data ...
        ]

    def create_blocks(self):
        """Creates the blocks for this level"""
        for platform in self.level_data:
            width, height, x_offset, y_offset, block_type = platform
            message = platform[5] if len(platform) > 5 else ""
            self.create_block_type(width,height,x_offset,y_offset,block_type,message)


    def create_block_type(self, width, height, x_offset, y_offset, block_type, message):
        for y in range(height):
            for x in range(width):
                block = Platform(TILE_SIZE, TILE_SIZE) #TILE_SIZE is assumed to be defined
                block.rect.x = (x_offset + x) * TILE_SIZE
                block.rect.y = (y_offset + y) * TILE_SIZE
                block.type = block_type
                if block_type in BLOCK_IMAGES:
                    try:
                        image_path = os.path.join('blockimages/Tiles', BLOCK_IMAGES[block_type])
                        block.image = pygame.image.load(image_path).convert()
                    except pygame.error as e:
                        print(f"Error loading image {image_path}: {e}")

                if block_type == "message":
                    block.message = message
                self.platform_list.add(block)

    def __init__(self, player):
        """ Create level 1. """
        Level.__init__(self, player)
        self.level_limit = -2500
        self.create_blocks()