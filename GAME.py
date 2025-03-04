import pygame
from LoadDepends import *  #Import necessary modules


# Constants (Good practice to centralize these)
Music = ["Silence", "Silence", "loop0", "loop2"]
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 600
TILE_SIZE = 64 #Example tile size
FPS = 60
DEBUG_FONT_SIZE = 15


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Scriptopolis Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", DEBUG_FONT_SIZE)
        self.player = Player()
        self.levels = [Level_01(self.player), Level_02(self.player), Level_03(self.player), Level_04(self.player), Level_05(self.player)] #Create levels
        self.current_level_index = 0
        self.current_level = self.levels[self.current_level_index]
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.load_music()

    def load_music(self):
        pygame.mixer.music.load(f"music\\{Music[self.current_level_index]}.wav")
        pygame.mixer.music.play(loops=0, start=0.0, fade_ms=1999)

    def handle_input(self, event):
        #Handle input events
        pass


    def update(self, dt):
        #Update game logic
        pass


    def draw(self):
        self.screen.fill(BLACK)
        self.current_level.draw(self.screen)
        self.all_sprites.draw(self.screen)
        #draw debug info
        pass
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    self.handle_input(event)
                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
            if pygame.mixer.music.get_pos() == -1:
                self.load_music()  #Restart the music if it ends
            self.update(dt)
            self.draw()


if __name__ == "__main__":
    game = Game()
    game.run()