import pygame

from configLoader import tileSizeScaled
from tiles import animatedTile
from random import randint
from miscFunctions import importCutSpritesheet, importFolderImages, scaleList


class enemy(animatedTile):
    def __init__(self,size,x,y):
        super().__init__(size,x,y,"../assets/sprites/west/animation")
        self.frames=scaleList(importFolderImages("../assets/sprites/west/animation"),tileSizeScaled,tileSizeScaled)
        self.deadFrames = scaleList(importCutSpritesheet("../assets/sprites/west/death/west_atlas.png"),tileSizeScaled,tileSizeScaled)
        self.frameIndex=0
        self.image=self.frames[self.frameIndex]
        self.deadMoving = False
        self.rect.y+=size-self.image.get_size()[1]
        self.speed=randint(3,5)
        self.dead=False
    def move(self):
        self.rect.x+=self.speed
    def die(self):
        self.dead=True
        self.frameIndex=0
        self.image=self.deadFrames[self.frameIndex]
        self.dieAnimation()

    def dieAnimation(self):
        self.frameIndex += 0.15
        if self.frameIndex < 3:
            self.image = self.deadFrames[int(self.frameIndex)]


    def flip(self):
        if self.speed>0:
            self.image= pygame.transform.flip(self.image,True,False)
    def reverse(self):
        self.speed*=-1

    def animateDeath(self):
        self.frameIndex=3
        self.dieAnimation()
    def dieAnimation(self):
        self.frameIndex += 0.15
        if self.frameIndex > int(len(self.deadFrames)):
            self.frameIndex=3
        self.image = self.deadFrames[int(self.frameIndex)]
    def update(self,xShift,yShift):
        self.rect.x += xShift
        self.rect.y += yShift
        if self.dead and not self.deadMoving:
            self.animateDeath()
        else:
            if self.deadMoving:
                self.dieAnimation()
            else:
                self.animate()
            self.move()


