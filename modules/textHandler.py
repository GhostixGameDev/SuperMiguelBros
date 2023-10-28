import pygame
class Text:
    def __init__(self,text,font,posx,posy,r,g,b,size):
        self.posx=posx
        self.posy=posy
        self.textFont = pygame.font.SysFont(font, size)
        self.textImage = self.textFont.render(text, True, (r, g, b), (0, 0, 0))
        self.textRect = self.textImage.get_rect()
        self.textRect.centerx = posx
        self.textRect.centery = posy
    def update(self,text,r,g,b,posx,posy):
        self.textImage=self.textFont.render(text,True,(r,g,b),(0,0,0))
        self.textRect = self.textImage.get_rect()
        self.textRect.centerx = posx
        self.textRect.centery = posy