#================================================================
#Contexto para los que visiten mi perfil de Github y se encuentren esto:
#Context for the ones who visit my Github Profile.
#This is basically a simple game made based on my highschool master, for a Pygame homework.

#Libraries...

import pygame


#Other modules of the game
from level import *
from modules.overworld import Overworld
from textHandler import Text
from levelEditor import *
from miscFunctions import *
from configLoader import *

#Classes

class Game:
    def __init__(self,surface):
        self.maxLevel=0
        self.surface=surface
        self.overworld = Overworld(0,self.maxLevel,self.surface)
    def run(self):
        self.overworld.run()
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

    #levelMap = Level(level0, screen)
    while playing:

        #EVENTOS DE PANTALLA
        #================================================================

        screen.fill((0,0,0))
        game.run()
        #levelMap.run()

        pygame.display.flip()

        #Definimos los fps limite del juego
        clock.tick(MaxFPS)

        #Cierre del juego:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing=False


if __name__ == '__main__':
    main(gameVer)
