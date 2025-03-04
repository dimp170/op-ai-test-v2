import pygame
from LVLDAT import Level
from PlatformOBJ import Platform
from PlayerCharacter import Player
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
TILE_SIZE = 64

# Image file names (Use a dictionary for easier management)
BLOCK_IMAGES = {
    "spawn": "spawnTile.PNG",
    "normal": "floorTile.PNG",
    "up": "moveUpTile.PNG",
    "down": "moveDownTile.PNG",
    "bouncy": "moveBounceTile.PNG",
    "pullup": "pullTile.PNG",
    "message": "setMessageTile.PNG",
    "enablemessages": "setEnableTile.PNG",
    "disablemessages": "setDisableTile.PNG",
    "flyingplatform": "FlyingPlatform.PNG",
    "lowerlimit": "lowerlimit.png", # Add image for this block if needed
    # Add more block types and their corresponding image names
}


class Level_05(Level):
    def __init__(self, player):
        Level.__init__(self, player)
        player.text = "OFF"
        self.level_limit = -250000
        self.level_data = self.load_level_data()
        self.create_platforms()

    def load_level_data(self):
        return [
            [6, 26, -6, -25, "normal"],
            [5, 1, 1, 0, "enablemessages"],
            [5, 1, 1, 0, "message", "This game is an absolute mess."],
            # ... rest of your level data ...
            [1, 1, 0, 0, "lowerlimit"],
            [1,1,5,-5,"flyingplatform"],
        ]


    def create_platforms(self):
        for platform_data in self.level_data:
            self.create_platform_group(*platform_data)

    def create_platform_group(self, width, height, x, y, block_type, *message):
        for row in range(height):
            for col in range(width):
                block = self.create_block(block_type, x + col, y + row, message)
                if block:
                    self.platform_list.add(block)

    def create_block(self, block_type, x, y, message):
        block = Platform(TILE_SIZE, TILE_SIZE)
        block.rect.x = x * TILE_SIZE
        block.rect.y = y * TILE_SIZE
        block.type = block_type

        image_path = os.path.join("blockimages/Tiles", BLOCK_IMAGES.get(block_type, "floorTile.PNG"))
        try:
            block.image = pygame.image.load(image_path).convert()
        except pygame.error as e:
            print(f"Error loading image {image_path}: {e}")
            return None

        if block_type == "message":
            block.message = message[0] if message else ""

        return block