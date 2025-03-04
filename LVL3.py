import pygame
from LVLDAT import Level
from PlatformOBJ import Platform
from PlatformImageOBJ import PlatformImage
from PlayerCharacter import Player
import random
import os

# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 100, 100)
PURPLE = (255, 0, 255)
GRAY = (100, 100, 100)
TILE_SIZE = 64  # Assuming 64x64 tiles


# Dictionary mapping block types to image filenames.  This is crucial for reducing duplication.
BLOCK_IMAGES = {
    "spawn": "spawnTile.PNG",
    "normal": "floorTile.PNG",
    "up": "moveUpTile.PNG",
    "down": "moveDownTile.PNG",
    "bouncy": "moveBounceTile.PNG",
    "pullup": "pullTile.PNG",
    "pulldown": "pullTile.PNG",
    "pullleft": "pullTile.PNG",
    "pullright": "pullTile.PNG",
    "message": "setMessageTile.PNG",
    "enablemessages": "setEnableTile.PNG",
    "disablemessages": "setDisableTile.PNG",
    "suffer": "sufferTile.PNG",
    "developer": "Dr RNG 3.PNG",
    # Add other block types and image names here as needed...
}


class Level_03(Level):
    def __init__(self, player):
        Level.__init__(self, player)
        self.level_limit = -5500
        self.level_data = self.load_level_data()
        self.create_platforms()

    def load_level_data(self):
        return [
            [1, 1, 0, 0, "spawn"],
            [8, 10, 1, 0, "normal"],
            [1, 10, 9, 0, "normal"],
            [25, 6, 5, 5, "normal"],
            [25, 1, 30, 5, "bouncy"],
            [4, 8, 55, 5, "down"],
            [11, 8, 59, 3, "up"],
            [1, 1, 255, 255, "lowerlimit"],  #Respawn zone
            [22, 2, 255, 255, "suffer"],
        ]


    def create_platforms(self):
        for platform_data in self.level_data:
            width, height, x, y, block_type = platform_data
            for row in range(height):
                for col in range(width):
                    block = self.create_block(block_type, x + col, y + row)
                    if block: #Check if block was created successfully
                        self.platform_list.add(block)

    def create_block(self, block_type, x, y):
        block = Platform(TILE_SIZE, TILE_SIZE)
        block.rect.x = x * TILE_SIZE
        block.rect.y = y * TILE_SIZE
        block.type = block_type
        image_path = os.path.join('blockimages/Tiles', BLOCK_IMAGES.get(block_type, "floorTile.PNG")) #default image
        try:
            block.image = pygame.image.load(image_path).convert()
        except pygame.error as e:
            print(f"Error loading image {image_path}: {e}")
            return None  # Return None if image loading fails

        return block