import pygame
from miscFunctions import scale

class UI:
    def __init__(self, surface):
        #setup
        self.displaySurface=surface
        pygame.font.init()
        #lives
        self.livesIcon=scale(pygame.image.load("../assets/sprites/UI/lives.png").convert_alpha(),64,64)
        #coins
        self.coinIcon=scale(pygame.image.load("../assets/sprites/objects/coins/gold/0.png").convert_alpha(),64,64)
        self.coinRect=self.coinIcon.get_rect(topleft=(50,61))
        self.font=pygame.font.Font("../assets/fonts/PressStart2P.ttf",32)
    def showLives(self, current, x,y):
        self.livesRect = self.livesIcon.get_rect(topleft=(x,y))
        self.displaySurface.blit(self.livesIcon,(self.livesRect))
        livesSurface=self.font.render("x"+str(current),False,(255,255,255))
        livesRect=livesSurface.get_rect(midleft=(self.livesRect.right+4,self.livesRect.centery))
        self.displaySurface.blit(livesSurface,livesRect)
    def showCoin(self, amount, x,y):
        self.coinRect = self.coinIcon.get_rect(topleft=(x, y))
        self.displaySurface.blit(self.coinIcon,(x,y))
        coinSurface=self.font.render(str(amount),False,(255,255,255))
        coinRect=coinSurface.get_rect(midleft=(self.coinRect.right+4,self.coinRect.centery))
        self.displaySurface.blit(coinSurface,coinRect)
