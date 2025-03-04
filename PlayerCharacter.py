import pygame
import os
import random
import statistics as st

# Constants (Good practice to centralize these)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 100, 100)
PURPLE = (255, 0, 255)
GRAY = (100, 100, 100)
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRAVITY = 1.1
JUMP_STRENGTH = -25
TILE_SIZE = 32

# Animation data (replace with your actual image loading)
ANIMATION_FRAMERATE = 0.1 # seconds per frame
ANIMATION_DATA = {
    "idle": ["PL0", "PL1", "PL3", "PL4", "PL3", "PL1", "PL0"],
    "walk_left": ["PL0", "PL1", "PL3", "PL4", "PL3", "PL1", "PL0"],
    "walk_right": ["PR0", "PR1", "PR3", "PR4", "PR3", "PR1", "PR0"],
    "jump": ["PFALL", "PFALR", "PFALL2", "PFALR2", "PFALL3", "PFALR3", "PFALL4", "PFALR4"],
    "push": ["PSHL", "PSHR"],
}

def load_images(image_names):
    """Loads images from the specified directory"""
    return [pygame.image.load(os.path.join('images', f"{img}.gif")).convert() for img in image_names]

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = {}
        for animation_name, image_names in ANIMATION_DATA.items():
            self.images[animation_name] = load_images(image_names)
        self.image = self.images["idle"][0]  # Start with idle image
        self.rect = self.image.get_rect()
        self.position = pygame.math.Vector2(0, 0)
        self.velocity = pygame.math.Vector2(0, 0)
        self.on_ground = False
        self.jumps = 0
        self.max_jumps = 2
        self.debug = False
        self.free_fly = False
        self.speed_multiplier = 1
        self.message = ""
        self.text_enabled = False
        self.current_animation = "idle"
        self.animation_frame = 0
        self.animation_timer = 0
        self.direction = 1 # 1 for right, 0 for left

    def update(self, dt, level):
        self.animate(dt)
        self.apply_gravity(dt)
        self.move(dt)
        self.handle_collisions(level)
        self.interact_with_blocks(level) #handle block types

    def animate(self, dt):
        self.animation_timer += dt
        if self.animation_timer > ANIMATION_FRAMERATE:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % len(self.images[self.current_animation])
            self.image = self.images[self.current_animation][self.animation_frame]


    def apply_gravity(self, dt):
        if not self.free_fly:
            self.velocity.y += GRAVITY * dt


    def move(self, dt):
        #This needs to be updated to reflect current movement logic
        pass

    def handle_collisions(self, level):
        self.on_ground = False
        for block in level.platform_list:
            if self.rect.colliderect(block.rect):
                # ...More efficient collision detection and response...
                pass


    def interact_with_blocks(self, level):
        #Handle Interactions with blocks of different types
        pass

    def jump(self):
        if self.jumps < self.max_jumps:
            self.velocity.y = JUMP_STRENGTH
            self.jumps += 1
            self.current_animation = "jump"

    def go_left(self):
        self.velocity.x = -self.speed_multiplier * 5
        self.direction = 0
        self.current_animation = "walk_left"

    def go_right(self):
        self.velocity.x = self.speed_multiplier * 5
        self.direction = 1
        self.current_animation = "walk_right"

    def stop(self):
        self.velocity.x = 0
        self.current_animation = "idle"
