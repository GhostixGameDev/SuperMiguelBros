import pygame
from tiles import animatedTile
from random import randint
class enemy(animatedTile):
    def __init__(self,size,x,y):
        super().__init__(size,x,y,"../assets/sprites/west/animation")
        self.rect.y+=size-self.image.get_size()[1]
        self.speed=randint(3,5)
    def move(self):
        self.rect.x+=self.speed
    def flip(self):
        if self.speed>0:
            self.image= pygame.transform.flip(self.image,True,False)
    def reverse(self):
        self.speed*=-1
    def update(self,x_shift):
        self.rect.x += x_shift
        self.animate()
        self.move()