
import pygame
import statistics as st
import random
from LoadDepends import *  

# Global constants
LEVEL_COUNT = 3
MUSIC = ["Silence", "Silence", "loop0", "loop2"]

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Screen dimensions
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 600

def handle_input(player, event):
    """Handles player input events."""
    if event.type == pygame.KEYDOWN:
        if event.key == 32:
            player.text = "ON"
        elif event.key == pygame.K_LEFT:
            player.go_left()
        elif event.key == pygame.K_RIGHT:
            player.go_right()
        elif event.key == pygame.K_UP:
            if player.freeFly != 1:
                player.jump()
            else:
                player.go_up()
        elif event.key == pygame.K_DOWN:
            if player.freeFly == 1:
                player.go_down()
        elif event.key == pygame.K_KP0:
            player.debug = 1 - player.debug
        elif event.key == pygame.K_KP1:
            player.noParticles = 1 - player.noParticles
        elif event.key == pygame.K_KP2:
            player.noClip = 1 - player.noClip
        elif event.key == pygame.K_KP3:
            player.noPhysicsBlocks = 1 - player.noPhysicsBlocks
        elif event.key == pygame.K_KP4:
            player.noSprites = 1 - player.noSprites
            player.justSet = 1
        elif event.key == pygame.K_KP5:
            player.toSpawn = 1
        elif event.key == pygame.K_KP6:
            player.randomlyWarp = 1
        elif event.key == pygame.K_KP7:
            print(pygame.display.get_window_size())
        elif event.key == pygame.K_END:
            switch_level(player)
        elif event.key == pygame.K_KP8:
            player.noJumpCap = 1 - player.noJumpCap
        elif event.key == pygame.K_KP9:
            player.freeFly = 1 - player.freeFly
        elif event.key == pygame.K_KP_PLUS:
            player.speedMultiplier += 1
        elif event.key == pygame.K_KP_MINUS:
            player.speedMultiplier -= 1
    elif event.type == pygame.KEYUP:
        if (event.key == pygame.K_LEFT and player.change_x < 0) or \
           (event.key == pygame.K_RIGHT and player.change_x > 0) or \
           (event.key == pygame.K_UP and player.change_y < 0 and player.freeFly == 1) or \
           (event.key == pygame.K_DOWN and player.change_y > 0 and player.freeFly == 1):
            player.stop()

def switch_level(player):
    """Switches to the next level in the game."""
    global current_level_no, current_level

    pygame.mixer_music.fadeout(300)
    if current_level_no < len(level_list) - 1:
        current_level_no += 1
    else:
        current_level_no = 0
        pygame.mixer_music.fadeout(2000)

    current_level = level_list[current_level_no]
    player.level = current_level
    player.toSpawn = 1
    player.text = 0
    player.justSet = 1
    load_level_music()

def load_level_music():
    """Loads and plays the music for the current level."""
    pygame.mixer_music.load(f"music/{MUSIC[current_level_no]}.wav")
    pygame.mixer_music.play(loops=0, start=0.0, fade_ms=1999)

def shift_world(player, current_level, size):
    """Shifts the game world based on player position."""
    scale_corrector = int(size[0] / 4)
    scale_corrector2 = int(size[1] / 4)
    scale_corrector3 = int(scale_corrector * 3)
    scale_corrector23 = int(scale_corrector2 * 3)

    # Right side
    if player.rect.right >= int(scale_corrector3):
        diff = int(scale_corrector3) - player.rect.right
        player.rect.right = int(scale_corrector * 3)
        current_level.shift_world_x(diff)

    # Left side
    if player.rect.left <= scale_corrector:
        diff = scale_corrector - player.rect.left
        player.rect.left = scale_corrector
        current_level.shift_world_x(diff)

    # Top side
    if player.rect.top <= scale_corrector2:
        diff = player.rect.top - scale_corrector2
        player.rect.top = scale_corrector2
        current_level.shift_world_y(-diff)

    # Bottom side
    if player.rect.bottom >= int(scale_corrector23):
        diff = int(scale_corrector23) - player.rect.bottom
        player.rect.bottom = int(scale_corrector23)
        current_level.shift_world_y(diff)

def generate_particles(screen, player, size):
    """Generates particle effects around the player."""
    if player.noParticles == 1:
        return

    draws = player.rect.top

    for g in range(player.rect.top, player.rect.bottom):
        draws += 1

        direction = -1 if player.Direction == 0 else 1

        try:
            if random.randint(0, 2) == 2:
                for i in range(player.rect.left, player.rect.right):
                    A = screen.get_at((i, draws))

                    A[0] = random.randint(1, 255)
                    A[1] = random.randint(1, 255)
                    A[2] = random.randint(1, 255) #Corrected index
                    A[3] = random.randint(1, 255)

                    if player.bounces != 0:
                        A[0] = random.randint(1, 100)
                        A[1] = random.randint(1, 250)
                        A[2] = random.randint(1, 255) #Corrected index
                        A[3] = random.randint(1, 255)

                    if player.goingUp != 0:
                        A[0] = random.randint(1, 100)
                        A[1] = random.randint(1, 200)
                        A[2] = random.randint(1, 255) #Corrected index
                        A[3] = random.randint(1, 255)

                    if player.goingDown != 0:
                        A[0] = random.randint(1, 255)
                        A[1] = random.randint(1, 200)
                        A[2] = random.randint(1, 100) #Corrected index
                        A[3] = random.randint(1, 100)

                    if A[0] != 0 and A[1] != 0 and A[2] != 0 and random.randint(0, 1) == 1:
                        screen.set_at((i - int(player.change_x), int(draws + player.change_y / 3 - 1)), A)
                        screen.set_at((i - int(player.change_x / 1.5), int(draws + player.change_y / 2 * -1)), A)
                        screen.set_at((i - int(player.change_x / 2), int(draws + player.change_y / 1 * -1)), A)
        except IndexError:
            pass  # Handle out-of-bounds errors silently


def draw_debug_info(screen, player, font):
    """Draws debug information on the screen."""
    y_offset = 65
    line_height = 15
    debug_data = [
        ("SBTYPE", player.type if player.type else "default"),
        ("X_SPEED", player.change_x),
        ("Y_SPEED", player.change_y),
        ("JUMPS", player.jumps),
        ("BOUNCE_COUNT", player.bounces),
        ("STATE", f"{player.frame} {player.bounces} {player.Direction} {player.pushing} {player.state} {player.image}"),
        ("FACING", player.Direction),
        ("STAGE", current_level_no),
        ("FALL_SPEED_CHECK", player.snappedtofloor),
        ("NO_COLLISION", player.noClip),
        ("INFINITE_JUMP", player.noJumpCap),
        ("NO_SPRITES", f"{player.noSprites} {player.noParticles}"),
        ("FLY_MODE", player.freeFly),
        ("NO_BLOCK_PROPERTIES", player.noPhysicsBlocks),
        ("FLYING_PLATFORM_ACTIVE", player.fpEnabled)
    ]

    for label, value in debug_data:
        text_surface = font.render(f"{label} {value}", 1, (150, 95, 255))
        screen.blit(text_surface, (50, y_offset))
        y_offset += line_height

# Main Program
def main():
    """Main Program"""
    global current_level_no, current_level, level_list

    pygame.init()
    font = pygame.font.SysFont("arial", 15)
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode((size), pygame.RESIZABLE)
    pygame.display.set_caption("Scriptopolis Game")

    # Setup game objects
    player = Player()
    level_list = [Level_01(player)]  # Add more levels as needed

    current_level_no = 0
    current_level = level_list[current_level_no]
    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    # Find spawn block and set player position
    for block in player.level.platform_list:
        if block.type == "spawn":
            blocksides = [block.rect.left, block.rect.right]
            startpos = st.median(blocksides)
            player.rect.bottom = block.rect.top
            player.rect.x = startpos
            break  # stop after the first spawn block is located.
    active_sprite_list.add(player)

    load_level_music() #Load starting stage music.

    # Game loop
    done = False
    clock = pygame.time.Clock()

    while not done:
        # Event processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            handle_input(player, event)

        # Music looping
        if pygame.mixer_music.get_busy() == False:
            load_level_music()

        # Update game logic
        active_sprite_list.update()
        current_level.update()
        size = pygame.display.get_window_size()
        shift_world(player, current_level, size)

        # Level completion check
        current_position = player.rect.x + current_level.world_shift
        current_height = player.rect.y + current_level.world_height

        if current_position < current_level.level_limit:
            switch_level(player)

        # Drawing
        screen.fill(BLACK)  # Clear the screen
        current_level.draw(screen)
        active_sprite_list.draw(screen)

        # Display debug text
        if player.text == "ON":
            pmes = font.render(player.message, 1, (100, 255, 0))
            screen.blit(pmes, (100, 50))

        #Draw X/Y position of the player
        posX = font.render(f"POS_X {current_position}", 1, (255, 255, 100))
        posY = font.render(f"POS_Y {current_height}", 1, (255, 255, 100))
        screen.blit(posX, (10,10))
        screen.blit(posY, (10,25))

        if player.debug == 1:
            draw_debug_info(screen, player, font)

        generate_particles(screen, player, size) #Draw particles.
        # Update the display
        pygame.display.flip()

        # Limit frame rate
        clock.tick(60)

        player.pushing = 0  #Reset pushing state.

    pygame.quit()


if __name__ == "__main__":
    main()
```

