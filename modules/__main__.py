#================================================================
#Contexto para los que visiten mi perfil de Github y se encuentren esto:
#Context for the ones who visit my Github Profile.
#This is basically a simple game made based on my highschool master, for a Pygame homework.

#Libraries...

import pygame

#Game Music credits:
#Fast Feel Banana Peel by Alexander Nakarada | https://creatorchords.com
#Music promoted on https://www.chosic.com/free-music/all/
#Creative Commons Attribution 4.0 International (CC BY 4.0)
#https://creativecommons.org/licenses/by/4.0/



#Other modules of the game
from level import *
from overworld import Overworld
from gameData import *
from miscFunctions import *
from configLoader import *
from UI import UI
from menu import mainMenu

#Classes

class Game:
    def __init__(self,surface,version):
        self.surface=surface
        #audio
        pygame.mixer.init()
        self.gameMusic=pygame.mixer.Sound("../assets/music/game.ogg")
        self.winSound=pygame.mixer.Sound("../assets/sounds/victory.ogg")
        #player things
        self.maxLevel=5
        self.lives=3
        self.coins=0
        #Menu things
        self.version=version
        self.menu=mainMenu(self.surface,self.version)
        #overworld things
        self.status=0
        self.gameMusic.play(-1)
        self.UI=UI(self.surface)
        self.overworld = Overworld(0, self.maxLevel, self.surface, self.createLevel)

    def createLevel(self,currentLevel):
        self.levelMap = Level(currentLevel, self.surface,self.createOverworld,self.updateCoins,self.coins,self.updateLives,self.createLevel)
        self.status=2
    def createOverworld(self,currentLevel,newMaxLevel,win=False):
        if newMaxLevel>self.maxLevel:
            self.maxLevel=newMaxLevel
        if win:
            self.winSound.play()

        self.overworld = Overworld(currentLevel,self.maxLevel,self.surface,self.createLevel)
        self.status=1
    def updateCoins(self,amount):
        self.coins=amount
    def updateLives(self,amount):
        self.lives+=amount
    def run(self):
        if self.status==1:
            self.overworld.run()
            self.UI.showCoin(self.coins, 20, 10)
        elif self.status==2:
            self.levelMap.run()
            self.UI.showLives(self.lives, 20, 10)
            self.UI.showCoin(self.coins, 20, 90)
            if self.lives<1:
                self.status=0
                self.lives=3
                self.coins=0
                self.maxLevel=0
                self.overworld = Overworld(0, self.maxLevel, self.surface, self.createLevel)
        else:
            self.menu.run()
#==========================================================

gameVer="Alpha 1.0.1"


def main(gameVer):
    icon=pygame.image.load("../icon.ico")
    playing = True
    if firstTime:
        screen=pygame.display.set_mode(primaryMonitorSize())
    else:
        screen = pygame.display.set_mode((width, height))
    MaxFPS = 60
    game = Game(screen,gameVer)
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
