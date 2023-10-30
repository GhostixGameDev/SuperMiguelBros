#================================================================
#Contexto para los que visiten mi perfil de Github y se encuentren esto:
#Context for the ones who visit my Github Profile.
#This is basically a simple game made based on my highschool master, for a Pygame homework.

#Libraries...

import pygame


#Other modules of the game
from level import *
from tiles import Tile
from textHandler import Text
from levelEditor import *
from miscFunctions import *
from configLoader import *



#Global variables.
level=0
gameVer="Alpha 0.0.1"

#==========================================================


def main(gameVer):
    icono=pygame.image.load("../icon.ico")
    jugando = True
    if firstTime:
        pantalla=pygame.display.set_mode(primaryMonitorSize())
    else:
        pantalla = pygame.display.set_mode((width, height))
    MaxFPS = 60
    TargetFPS = 60
    pygame.init()
    pygame.display.set_caption("Super Miguel Bros v"+gameVer)
    pygame.display.set_icon(icono)
    clock=pygame.time.Clock()

    levelMap = Level(level0, pantalla)
    while jugando:

        #EVENTOS DE PANTALLA
        #================================================================
        pantalla.fill((0,0,0))
        levelMap.run()

        pygame.display.flip()

        #Definimos los fps limite del juego
        clock.tick(MaxFPS)

        #Cierre del juego:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jugando=False


if __name__ == '__main__':
    main(gameVer)
