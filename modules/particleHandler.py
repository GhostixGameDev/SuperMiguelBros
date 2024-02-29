import pygame
from miscFunctions import importFolderImages
import random
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
    def update(self,xShift, yShift):
        self.animate()
        self.rect.x+=xShift
        self.rect.y+=yShift

class JoJoLikeText(pygame.font.Font):
    def __init__(self,font,size,surface):
        super().__init__(font,size)
        self.x=0
        self.y=0
        self.surface=surface
        self.jojoOutline=pygame.font.Font(font,size+1)
        self.pastTime = 0
        self.xShake=0
        self.yShake=0

    def shake(self):
        self.xShake=random.random()*2.5
        self.xShake-=random.random()*1.5
        self.yShake+=random.random()*2.5
        self.yShake=random.random()*1.5
        #print(self.xShake)
    def draw(self,text,color,x,y):
        self.x=x+self.xShake
        self.y=y+self.yShake
        self.jojoOutlineR=self.jojoOutline.render(text,False,(67, 35, 88))
        self.jojo = self.render(text,False,color).convert_alpha()
        self.surface.blit(self.jojo,(self.x,self.y))
        self.surface.blit(self.jojoOutlineR, (self.x, self.y))

    def textTimer(self):
        #print("past:"+str(self.pastTime))
        currentTime=pygame.time.get_ticks()
        if currentTime-self.pastTime>=2000:
            stop=True
            #print("Current; "+str(currentTime))
            return stop
    def update(self,xshift,yShift):
        self.x += xshift
        self.y += yShift
        self.shake()