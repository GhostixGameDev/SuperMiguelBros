import pygame
from levelEditor import tile_size
from miscFunctions import scale
class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,size):
        super().__init__()
        self.image=scale(pygame.image.load("../assets/sprites/objects/box.png"),tile_size,tile_size)
        self.rect=self.image.get_rect(topleft=pos)
    def update(self,x_shift):
        self.rect.x +=x_shift