import pygame
from miscFunctions import importFolderImages

class ParticleEffect(pygame.sprite.Sprite):

    def __init__(self,pos,type):
        super().__init__()
        self.frameIndex=0
        self.animationSpeed=0.5
        if type=="jump":
            self.frames = importFolderImages("../assets/sprites/particles/dust/jump")
        if type=="land":
            self.frames = importFolderImages("../assets/sprites/particles/dust/land")
        self.image=self.frames[self.frameIndex]
        self.rect=self.image.get_rect(center=pos)
    def animate(self):
        self.frameIndex+=self.animationSpeed
        if self.frameIndex>=len(self.frames):
            self.kill()
        else:
            self.image=self.frames[int(self.frameIndex)]
    def update(self,xShift):
        self.animate()
        self.rect.x+=xShift