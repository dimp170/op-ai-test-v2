#This needs the most work out of everything else - it's an absolute mess.
import math
import os
import pygame
import random
from pygame.locals import *
import statistics as st
idleimage = ["PL1"]
PL = ["PL0", "PL1", "PL3", "PL4", "PL3", "PL1", "PL0"]
PR = ["PR0", "PR1", "PR3", "PR4", "PR3", "PR1", "PR0"]
PI = ["PIL", "PIR"]
PS = ["PLSL", "PLSR"]
PF = ["PFALL", "PFALR", "PFALL2", "PFALR2", "PFALL3", "PFALR3", "PFALL4", "PFALR4"]
PSH= ["PSHL", "PSH"]
PH = ["Head1"]
#Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255,100,100)
PURPLE = (255,0,255)
GRAY = (100,100,100)
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.secondtimer = 0#Counts up to 60 and adds a second
        self.invalidMove = False
        self.goingUp = 0
        self.goingDown = 0
        self.bounces = 0
        self.framepause = 0
        self.state = "Idle"
        self.fails = 0
        self.pushing = 0
        self.Direction = 1
        self.message = ""
        self.currentcheckpoint = 0 #Needs to be implemented
        self.jumps = 0
        self.stage = 0
        self.stageM = 1
        self.timer = 0
        self.totalseconds = 0
        self.image = pygame.image.load(os.path.join('images', "PIR.gif")).convert()
        self.frame = 0                 #Current frame of animation.
        self.rect = self.image.get_rect()
        self.gstorage = []             #Testing neat visual effects here.
        #Visual triggers
        self.text = "OFF"
        self.down = 0
        self.up = 0
        self.pull = 0
        self.snappedtofloor = 0        #To prevent floor clipping when you fall too fast
        self.change_x = 0
        self.change_y = 0
        self.anim = 0.0
        self.falltime = 0
        self.fpEnabled = 0             #Controls if the flying platform can move or not.
        #Base values for player physics (Jumping and running)
        self.speedCap = 15             #How fast the player can run
        self.speedGain = 0.25          #How fast the player speeds up
        self.fallCap = 40              #How fast the player can fall
        self.fallGain = 0              #How fast the player goes down           (UNUSED, NOT IMPLEMENTED)
        self.pushSpeed = 0             #How fast the player can push tiles      (UNUSED, NOT IMPLEMENTED)
        self.pushGain = 0              #How fast the player speeds up (pushing) (UNUSED, NOT IMPLEMENTED)
        #Game states (Used by the debug mode)
        self.freeFly = 0               #Enables free fly mode
        self.speedMultiplier = 1       #The speed multiplier used in fly mode. The + and - keys control this.
        self.swimMode = 0              #Makes all blocks act like water         (UNUSED, NOT IMPLEMENTED)
        self.deleteMap = 0             #Clears out the current map's block list (UNUSED, NOT IMPLEMENTED)
        self.deleteWorld = 0           #Clears out all level data               (UNUSED, NOT IMPLEMENTED)
        self.resetGame = 0             #Resets the game                         (UNUSED, NOT IMPLEMENTED)
        self.toSpawn = 0               #Warps the player to spawn
        self.randomlyWarp = 0          #Warps the player to a random block
        self.noClip = 0                #Disables horizontal wall collision
        self.noPhysicsBlocks = 0       #Disables special block property checks
        self.noParticles = 0           #Disables particles (for low end systems)
        self.noText = 0                #Disables text entirely                  (UNUSED, NOT IMPLEMENTED)
        self.noSprites = 0             #Disables images (squares everywhere)
        self.noMomentum = 0            #Disables the speed buildup              (UNUSED, NOT IMPLEMENTED)
        self.noJumpCap = 0             #Disables the max jumps
        self.debug = 0                 #Debug mode
        self.justSet = 0               #For the graphics disable/enable button
        self.type = ""                 #Used in the block type check
        #Game data
        self.level = None              #Where the level gets loaded in
    def update(self):
        blockFalling = False
        """ Move the player. """
        # Gravity
        self.secondtimer += 1
        self.calc_grav()
        if self.rect.y >=480:
            for block in self.level.platform_list:
                if block.rect.x <= self.rect.x:
                    self.rect.y=block.rect.y-200
                    self.rect.x=block.rect.x
        pcH = [self.rect.top, self.rect.bottom]
        pcW = [self.rect.left, self.rect.right]
        midH = st.median(pcH)
        midW = st.median(pcW)
        pcH.clear()
        pcW.clear()
        #Movement states start here
        
        #Moving left
        if self.state == "WLeft":
            self.change_x = max(self.change_x - self.speedGain, -self.speedCap)
            if self.noSprites != 1:
                if self.change_y == 1:
                    self.framepause += 1
                    if self.framepause >= 2:
                        self.Direction = 0
                        self.frame = (self.frame + 1) % 4
                        self.framepause = 0
                    self.pushing = 0
                    for block in self.level.platform_list:
                        if self.rect.right == block.rect.left and self.change_x != 0 and block.rect.bottom == self.rect.bottom:
                            self.image = pygame.image.load(os.path.join('images', PSH[self.Direction]+".gif")).convert()
                            self.pushing = 1
                            break
                        if self.rect.left == block.rect.right and self.change_x != 0 and block.rect.bottom == self.rect.bottom:
                            self.image = pygame.image.load(os.path.join('images', PSH[self.Direction]+".gif")).convert()
                            self.pushing = 1
                            break
                    if self.pushing == 0:
                        self.image = pygame.image.load(os.path.join('images', PL[self.frame]+".gif")).convert()
                else:
                    self.frame %= 4
                    if self.change_y <= 0:
                        self.image = pygame.image.load(os.path.join('images', PF[self.Direction]+".gif")).convert()
                    elif self.change_y <= 10:
                        self.image = pygame.image.load(os.path.join('images', PF[self.Direction+4]+".gif")).convert()
                    else:
                        self.image = pygame.image.load(os.path.join('images', PF[self.Direction+2]+".gif")).convert()

        #Not moving at all (idle)
        if self.state == "Idle":
            if self.noSprites != 1:
                if self.frame >= 4:
                    self.frame = 0
                #(In case the player jumps while idle. "PF" is the falling sprite and this makes sure that plays when you're moving in the air.)
                if self.change_y <= -1:
                    self.image = pygame.image.load(os.path.join('images', PF[self.Direction]+".gif")).convert()
                    self.frame = 1
                if self.change_y >= 1 and self.change_y <= 5:
                    self.image = pygame.image.load(os.path.join('images', PF[self.Direction+4]+".gif")).convert()
                    self.frame = 2
                if self.change_y >= 6 and self.change_y <= 11:
                    self.image = pygame.image.load(os.path.join('images', PF[self.Direction+6]+".gif")).convert()
                    self.frame = 3
                elif self.change_y >= 11:
                    self.frame = 4
                    self.image = pygame.image.load(os.path.join('images', PF[self.Direction+2]+".gif")).convert()
                if self.change_y == 1:
                    self.frame = 0
                    self.image = pygame.image.load(os.path.join('images', PI[self.Direction]+".gif")).convert()
        
        #Debug feature (free fly)
        if self.state == "WUp":
            self.change_y -= self.speedGain
            if self.change_y <= -self.speedCap:
                self.change_y = -self.speedCap
                
        #Debug feature (free fly)
        if self.state == "WDown":
            self.change_y += self.speedGain
            if self.change_y >= self.speedCap:
                self.change_y = self.speedCap
                
        #Moving right
        if self.state == "WRight":
            self.change_x += self.speedGain
            if self.change_x >= self.speedCap:
                self.change_x = self.speedCap
                
            if self.noSprites != 1:
                if self.change_y == 1:
                    self.framepause += 1
                    if self.framepause >= 2:
                        self.Direction = 1
                        self.frame+=1
                        if self.frame == 4:
                            self.frame = 0
                        self.framepause = 0
                    for block in self.level.platform_list:
                        if self.rect.right == block.rect.left and self.change_x != 0 and block.rect.bottom == self.rect.bottom:
                            self.image = pygame.image.load(os.path.join('images', PSH[self.Direction]+".gif")).convert()
                            self.pushing = 1
                        if self.rect.left == block.rect.right and self.change_x != 0 and block.rect.bottom == self.rect.bottom:
                            self.image = pygame.image.load(os.path.join('images', PSH[self.Direction]+".gif")).convert()
                            self.pushing = 1
                    if self.pushing != 1:
                        if self.frame >= 4:
                            self.frame = 0
                        self.image = pygame.image.load(os.path.join('images', PR[self.frame]+".gif")).convert()
                else:
                    if self.frame == 4:
                        self.frame = 0
                    if self.change_y <= 0:
                        self.image = pygame.image.load(os.path.join('images', PF[self.Direction]+".gif")).convert()
                    if self.change_y >= 1 and self.change_y <= 10:
                        self.image = pygame.image.load(os.path.join('images', PF[self.Direction+4]+".gif")).convert()
                    elif self.change_y >= 11:
                        self.image = pygame.image.load(os.path.join('images', PF[self.Direction+2]+".gif")).convert()
        #When the disable sprites debug feature is turned off, load the graphics for the tiles back in
        if self.noSprites == 0 and self.justSet == 1:
            for block in self.level.platform_list:
                if block.type == "up":
                    block.image = pygame.image.load(os.path.join('blockimages/Tiles', "moveUpTile.PNG")).convert()
                if block.type == "down":
                    block.image = pygame.image.load(os.path.join('blockimages/Tiles', "moveDownTile.PNG")).convert()
                if block.type == "bouncy":
                    block.image = pygame.image.load(os.path.join('blockimages/Tiles', "moveBounceTile.PNG")).convert()
                if block.type == "" or block.type == "normal":
                    block.image = pygame.image.load(os.path.join('blockimages/Tiles', "floorTile.PNG")).convert()
                if block.type.startswith("pull"):
                    block.image = pygame.image.load(os.path.join('blockimages/Tiles', "pullTile.PNG")).convert()
                if block.type == "message":
                    block.image = pygame.image.load(os.path.join('blockimages/Tiles',"setMessageTile.PNG")).convert()
                if block.type == "enablemessages":
                    block.image = pygame.image.load(os.path.join('blockimages/Tiles',"setEnableTile.PNG")).convert()
                if block.type == "disablemessages":
                    block.image = pygame.image.load(os.path.join('blockimages/Tiles',"setDisableTile.PNG")).convert()
                if block.type == "developer":
                    block.image = pygame.image.load(os.path.join('images', "Dr RNG 3.PNG")).convert()
                if block.type == "flyingplatform":
                    block.image = pygame.image.load(os.path.join('blockimages', "FlyingPlatform.PNG")).convert()
                if block.type == "spawn":
                    block.image = pygame.image.load(os.path.join('blockimages/Tiles', "spawnTile.PNG")).convert()
                if block.type == "suffer":
                    block.image = pygame.image.load(os.path.join('blockimages/Tiles', "sufferTile.PNG")).convert()
            self.justSet = 0
        #When the disable sprites debug feature is turned on, make all of the major platforms specific colors to make it easier to tell them apart (ignore the ones that don't matter so much/aren't added yet)
        if self.noSprites == 1 and self.justSet == 1:
            self.image.fill(WHITE)
            for block in self.level.platform_list:
                block.image.fill(WHITE)
                if block.type == "up":
                    block.image.fill(GREEN)
                if block.type == "down":
                    block.image.fill(RED)
                if block.type == "bouncy":
                    block.image.fill(BLUE)
                if block.type == "" or block.type == "normal":
                    block.image.fill(WHITE)
                if block.type.startswith("pull"):
                    block.image.fill(GRAY)
                if block.type == "spawn":
                    block.image.fill(PURPLE)
            self.justSet = 0
            #Movement states end here

        if self.randomlyWarp != 0:
            toblock = random.randint(0, len(self.level.platform_list))
            tracker = 0
            for block in self.level.platform_list:
                if tracker == toblock:
                    self.rect.x = block.rect.x
                    self.rect.y = block.rect.y-128
                tracker+=1
            self.randomlyWarp = 0
        # Move left/right
        self.rect.x += self.change_x
        # See if we hit anything

        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        #Block type info
        if self.toSpawn == 1:
            for block in self.level.platform_list:
                if str(block.type).lower() == "spawn":
                    self.type = block.type
                    self.rect.x = block.rect.x
                    self.rect.y = block.rect.y-128
                    self.toSpawn = 0

        if self.noPhysicsBlocks != 1:
            #Pushable block check (NEEDS WORK!... Maybe. Depends on how it gets used. Might add gravity to the block eventually so it falls when it goes over an edge.)
            for block in self.level.platform_list:
                #Hitting the block from the left side
                if block.type == "push" and self.Direction == 1 and self.pushing == 1 and self.rect.right in range(block.rect.left-15, block.rect.left+5):
                    if self.rect.top <= block.rect.bottom:
                        block.rect.left +=self.change_x
                #Hitting the block from the right side
                if block.type == "push" and self.Direction == 0 and self.pushing == 1 and self.rect.left in range(block.rect.right-5, block.rect.right+15):
                    if self.rect.top <= block.rect.bottom:
                        block.rect.right+=self.change_x
            for block in self.level.platform_list:
                if midW in range(block.rect.left, block.rect.right):
                    
                    #"Down" block
                    if block.type == "down" and block.moves < 64:
                        if self.rect.bottom == block.rect.top and block.type == "down":
                            self.type = block.type
                            self.goingDown = 1
                            self.rect.y += 2
                        if block.rect.bottom <= self.rect.top:
                            self.goingDown = 0
                            block.rect.y-=2
                            block.moves-=1
                        block.rect.y += 2
                        block.moves += 1
                        
                    #"Up" block
                    if block.type == "up" and block.moves < 64:
                        if self.rect.bottom == block.rect.top and block.type == "up":
                            self.type = block.type
                            self.goingUp = 1
                            self.rect.y -= 2
                        if self.rect.top <= block.rect.bottom and self.rect.top > block.rect.top:
                            self.goingUp = 0
                            self.rect.y += 2
                        block.rect.y -= 2
                        block.moves += 1
                    #"Bouncy" block
                    if block.type == "bouncy" and self.rect.bottom == block.rect.top:
                        self.type = block.type
                        self.rect.y -= 10
                        self.jumps = 1
                        self.bounces += 1
                        if self.bounces == 10:
                            self.bounces -= 1
                        self.change_y -= 5*self.bounces
                    #Reset bounce counter
                    if block.type != "bouncy" and self.rect.bottom == block.rect.top:
                        self.type = block.type
                        self.bounces = 0
                
                #Gravitational/"pull" blocks
                if block.type.startswith("pull"):
                    direct = block.type[4:]
                    if self.rect.x in range(block.rect.left, block.rect.right):
                        if direct == "up":
                            self.type = block.type
                            if self.rect.y > block.rect.y:
                                self.change_y=-10
                                self.pull = 1
                        if direct == "down":
                            self.type = block.type
                            if self.rect.y < block.rect.y:
                                self.change_y=10
                                self.pull = 1
                    if self.rect.y in range(block.rect.top, block.rect.bottom):
                        if direct == "left":
                            self.type = block.type
                            self.change_x=-10
                            self.pull = 1
                        if direct == "right":
                            self.type = block.type
                            self.change_x=10
                            self.pull = 1
                    elif self.rect not in block.rect:
                        self.pull = 0
                
                #"Lowerlimit" block (warps player to spawn if they're below it)
                if block.type.startswith("lower"):
                    
                    if midH in range(block.rect.top+1, block.rect.bottom+2000):
                        self.type = block.type
                        die = pygame.mixer.Sound("SFX/Deathwarp.wav")
                        pygame.mixer.Sound.play(die)
                    if midH in range(block.rect.top+12000, block.rect.bottom+15000):
                        self.type = block.type
                        for obj in self.level.platform_list:
                            if obj.type.startswith("spawn"):
                                self.change_y=0
                                self.rect.bottom = obj.rect.top
                                self.rect.x = obj.rect.x
                #Flying platform enable/disable blocks
                if self.rect.x in range(block.rect.left, block.rect.right):
                    if block.type.startswith("fp"): #Enable/disable options for the flying block
                        if block.type == "fpenable":
                            self.fpEnabled = 1
                        if block.type == "fpdisable":
                            self.fpEnabled = 0
                #Text blocks
                if self.noText != 1:
                    if block.type.startswith("mess"):
                        if midW in range(block.rect.left, block.rect.right):
                            self.type = block.type
                            self.message = block.message
                    if block.type.startswith("enablem"):
                        if midW in range(block.rect.left, block.rect.right):
                            self.type = block.type
                            self.text = "ON"
                    if block.type.startswith("disablem"):
                        if midW in range(block.rect.left, block.rect.right):
                            self.type = block.type
                            self.text = "OFF"
                
                #"Developer" block
                if block.type.startswith("deve"):
                    
                    #Chase the player
                    if block.rect.bottom < self.rect.top:
                        block.rect.y += 1
                    if block.rect.top > self.rect.bottom:
                        block.rect.y -= 1
                    if self.rect.bottom != block.rect.top:
                        if block.rect.x < self.rect.x:
                            block.rect.x += 1
                        if block.rect.x > self.rect.x:
                            block.rect.x -= 1
                    if self.rect.bottom == block.rect.top:
                        self.type = block.type
                        self.goingUp = 1
                        self.rect.y -= 1
                        block.rect.y -= 1
                        block.rect.x += self.change_x
                #"Flying" block
                if block.type.startswith("flyingplatform"): #The block itself
                    #Go up/down when activated (maybe make this get controlled by the player?)
                    if self.fpEnabled == 1:
                        if block.rect.bottom < self.rect.top:
                            block.rect.y += 1
                        if block.rect.top > self.rect.bottom:
                            block.rect.y -= 1
                        if self.rect.bottom == block.rect.top:
                            self.type = block.type
                            self.goingUp = 1
                            self.rect.y -= 1
                            block.rect.y -= 1
                            block.rect.x += self.change_x
                #Move blocks back to their original positions when the player is away.
                if midW not in range(block.rect.left, block.rect.right):
                    if block.type == "down" and block.moves > 0:
                        block.rect.y -= 2
                        block.moves -= 1
                        self.goingDown = 0
                    if block.type == "up" and block.moves > 0:
                        block.rect.y += 2
                        block.moves -= 1
                        self.goingUp = 0

        else:
            self.type = "DISABLED"
        playersize = self.rect.bottom-self.rect.top
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in self.level.platform_list:
            if block.type == "push":
                block_backup = block
                for block in self.level.platform_list:
                    if block.rect.x in range(block_backup.rect.x-64, block_backup.rect.x+64) and block.rect.top == block_backup.rect.bottom:
                        blockFalling = False
                        break
                    else:
                        blockFalling = True
                if blockFalling == True:
                    block = block_backup
                    block.rect.y+=16
##            if random.randint(0, 99) == 25:
##                A = block
##                randomMover1 = random.randint(-1, 1)*64
##                randomMover2 = random.randint(-1, 1)*64
##                for block in self.level.platform_list:
##                    if block.rect.x == randomMover1 and block.rect.y == randomMover2:
##                        self.invalidMove == True
##                        break
##                if self.invalidMove == False and block.rect.x > self.rect.x+200 and block.rect.y < self.rect.y+200 or block.rect.x < self.rect.x-200 and block.rect.y > self.rect.y-200:
##                    block = A
##                    block.rect.x+=randomMover1
##                    block.rect.y+=randomMover2
##                    print("HIT!!!!!")
##                self.invalidMove == False
        #Use math to calculate which side we are on and stop the player from clipping through the walls
        for block in block_hit_list:
            self.colliding = False
            MIDPOINT_X = [block.rect.left, midW, block.rect.right]
            MIDPOINT_Y = [block.rect.top, self.rect.bottom, block.rect.bottom]
            CENTERPOINT_X = st.median(MIDPOINT_X)
            CENTERPOINT_Y = st.median(MIDPOINT_Y)
            blockSides = [block.rect.left, block.rect.right]
            blockSides2 = [block.rect.top, block.rect.bottom]
            Side = min(blockSides, key=lambda x:abs(x-CENTERPOINT_X))
            Height = min(blockSides2, key=lambda x:abs(x-CENTERPOINT_Y))
            
            #Wall collision detection
            if self.noClip != 1:
                if Side == block.rect.left:
                    self.rect.right = block.rect.left
                    if self.Direction == 1:
                        #if block.type != "push":
                        self.change_x = 1
                        
                if Side == block.rect.right:
                    self.rect.left = block.rect.right
                    if self.Direction == 0:
                        #if block.type != "push":
                        self.change_x = -1
                #if Side != block.rect.left and Side != block.rect.right:
                #    self.colliding = False
        self.rect.y += self.change_y
 
        # Check and see if we hit anything
        floor = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        
        if self.freeFly != 1:
            self.speedCap = 15
            self.speedGain = 0.25
            if self.change_y >= self.fallCap:
                self.change_y = self.fallCap
        else:
            self.speedCap = 15*self.speedMultiplier
            self.speedGain = 0.25*self.speedMultiplier
        if self.freeFly != 1:
            for block in floor:
                MIDPOINT_X = [block.rect.left, midW, block.rect.right]
                MIDPOINT_Y = [block.rect.top, self.rect.bottom, block.rect.bottom]
                CENTERPOINT_X = st.median(MIDPOINT_X)
                CENTERPOINT_Y = st.median(MIDPOINT_Y)
                blockSides = [block.rect.left, block.rect.right]
                blockSides2 = [block.rect.top, block.rect.bottom]
                Side = min(blockSides, key=lambda x:abs(x-CENTERPOINT_X))
                Height = min(blockSides2, key=lambda x:abs(x-CENTERPOINT_Y))
                # Reset our position based on the top/bottom of the object.
                if Height == block.rect.top and self.change_y > 0:
                    self.rect.bottom = block.rect.top
                    self.jumps = 0
                if block.type != "push":
                    if self.noClip != 1:
                        if Height == block.rect.bottom and self.change_y <= 0 and self.rect.top <= block.rect.bottom:
                            self.rect.top = block.rect.bottom 
                if block.type == "pullup":
                    self.rect.bottom = block.rect.top
                # Stop our vertical movement
                self.change_y = 0
        
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.freeFly != 1:
            if self.change_y == 0:
                self.change_y = 1
                self.snappedtofloor = 0
            else:
                self.change_y += 1.1
                for block in self.level.platform_list:
                    if self.rect.x in range(block.rect.left, block.rect.right) and block.rect.top-self.rect.bottom in range(0, 12) and self.change_y >= 25:
                        self.change_y = 0
                        self.rect.bottom = block.rect.top
                        self.snappedtofloor = 1
                        print("Successfully prevented a floor clip")
 
    def jump(self):
        """ Called when user hits 'jump' button. """
        jumps = self.jumps
        self.last_x = self.rect.x
        self.last_y = self.rect.y
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        
        if self.freeFly != 1:
            if self.jumps != 2:
                
                platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
                self.rect.y -= 10
            # If it is ok to jump, set our speed upwards and check if the player has jumped twice yet
                if self.jumps == 1:
                    if len(platform_hit_list) > -20:
                        self.change_y = -20
                        if self.noJumpCap != 1:
                            self.jumps += 1
                if self.jumps == 0:
                    if len(platform_hit_list) > -20:
                        self.change_y = -25
                        if self.noJumpCap != 1:
                            self.jumps += 1
            for block in platform_hit_list:
                if self.freeFly != 1:
                    if self.rect.top <= block.rect.bottom and block.rect.top < self.rect.top:
                        self.change_y *= -1
                        self.jumps = 0
                
    # Player-controlled movement:
    def go_left(self):
        self.state = "WLeft"
        """ Called when the user hits the left arrow. """
        self.Direction = 0
    def go_right(self):
        self.state = "WRight"
        """ Called when the user hits the right arrow. """
        self.Direction = 1
    def go_up(self):
        self.state = "WUp"
        """ Called when the user hits the up arrow in free fly mode. """
    def go_down(self):
        self.state = "WDown"
        """ Called when the user hits the down arrow in free fly mode. """
    def stop(self):
        self.state = "Idle"
        """ Called when the user lets off the keyboard. """
        self.change_x = 0
        if self.freeFly == 1:
            self.change_y = 0

