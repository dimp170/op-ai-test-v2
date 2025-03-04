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

# Image file names, use a dictionary for easy maintenance
BLOCK_IMAGES = {
    "spawn": "spawnTile.PNG",
    "normal": "floorTile.PNG",
    "up": "moveUpTile.PNG",
    "down": "moveDownTile.PNG",
    "bouncy": "moveBounceTile.PNG",
    "pullup": "pullTile.PNG",  # Assuming same image for all pull types
    "message": "setMessageTile.PNG",
    "enablemessages": "setEnableTile.PNG",
    "disablemessages": "setDisableTile.PNG",
    "developer": "Dr RNG 3.PNG",
    "lowerlimit": "lowerlimit.png", # Add an image for this block type if needed.
}


class Level_04(Level):
    def __init__(self, player):
        Level.__init__(self, player)
        player.text = "OFF"  # Initialize player text here
        self.level_limit = -10500
        self.level_data = self.load_level_data()
        self.create_platforms()


    def load_level_data(self):
        return [
            [5, 1, 0, 0, "spawn"],
            [1, 1, 5, 0, "enablemessages"],
            [10, 1, 6, 0, "message", "Hey, can you hear me?"],
            # ... rest of your level data ...
            [1, 1, 999, 25, "lowerlimit"],  # Lower limit
        ]

    def create_platforms(self):
        for platform_data in self.level_data:
            width, height, x, y, block_type, *message = platform_data
            self.create_block_group(width, height, x, y, block_type, message)


    def create_block_group(self, width, height, x, y, block_type, message):
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

        #Load image from BLOCK_IMAGES, default to normal block image if not found
        image_path = os.path.join("blockimages/Tiles", BLOCK_IMAGES.get(block_type, "floorTile.PNG"))
        try:
            block.image = pygame.image.load(image_path).convert()
        except pygame.error as e:
            print(f"Error loading image {image_path}: {e}")
            return None

        if block_type == "message":
            block.message = message[0] #Extract the message from the list

        return block