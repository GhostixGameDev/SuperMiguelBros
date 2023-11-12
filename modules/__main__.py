#================================================================
#Contexto para los que visiten mi perfil de Github y se encuentren esto:
#Context for the ones who visit my Github Profile.
#This is basically a simple game made based on my highschool master, for a Pygame homework.

#Libraries...

import pygame


#Other modules of the game
from level import *
from overworld import Overworld
from textHandler import Text
from gameData import *
from miscFunctions import *
from configLoader import *

#Classes

class Game:
    def __init__(self,surface):
        self.maxLevel=1
        self.surface=surface
        self.status=0
        self.overworld = Overworld(0, self.maxLevel, self.surface, self.createLevel)
    def createLevel(self,currentLevel):
        self.levelMap = Level(currentLevel, self.surface,self.createOverworld)
        self.status=1
    def createOverworld(self,currentLevel,newMaxLevel):
        if newMaxLevel>self.maxLevel:
            self.maxLevel=newMaxLevel
        self.overworld = Overworld(currentLevel,self.maxLevel,self.surface,self.createLevel)
        self.status=0
    def run(self):
        if self.status==0:
            self.overworld.run()
        else:
            self.levelMap.run()
#==========================================================

#Global variables.
level=0
gameVer="Alpha 0.0.1"


def main(gameVer):
    icon=pygame.image.load("../icon.ico")
    playing = True
    if firstTime:
        screen=pygame.display.set_mode(primaryMonitorSize())
    else:
        screen = pygame.display.set_mode((width, height))
    MaxFPS = 60
    game = Game(screen)
    TargetFPS = 60
    pygame.init()
    pygame.display.set_caption("Super Miguel Bros v"+gameVer)
    pygame.display.set_icon(icon)
    clock=pygame.time.Clock()


    while playing:

        #EVENTOS DE PANTALLA
        #================================================================
        game.run()

        pygame.display.flip()

        #Definimos los fps limite del juego
        clock.tick(MaxFPS)

        #Cierre del juego:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing=False


if __name__ == '__main__':
    main(gameVer)
