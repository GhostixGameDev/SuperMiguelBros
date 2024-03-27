import sys

import pygame
import miscFunctions
from configLoader import *

class mainMenu:
    def __init__(self,surface, version):
        #Setup
        self.displaySurface=surface
        self.version=version
        self.background=pygame.image.load("../assets/menu/main/mainMenu.png")
        self.skibidi=pygame.image.load("../assets/menu/main/skibidi_miguel.png")
        self.mainText=pygame.font.Font("../assets/fonts/PressStart2P.ttf", 24)
        self.buttons=[pygame.image.load("../assets/menu/main/play0.png"),pygame.image.load("../assets/menu/main/play1.png"),pygame.image.load("../assets/menu/main/settings0.png"),pygame.image.load("../assets/menu/main/settings1.png")]
        self.playButton=self.buttons[0]
        self.settingsButton=self.buttons[2]

    def input(self):
        key=pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
           pygame.quit()
           sys.exit()

    def run(self):
        self.displaySurface.fill("#008c96")
        self.displaySurface.blit(miscFunctions.scale(self.background,width,height),(0,0))
        self.displaySurface.blit(miscFunctions.scale(self.skibidi, 500*scale, 500*scale), (width/20, height/4))
        self.input()