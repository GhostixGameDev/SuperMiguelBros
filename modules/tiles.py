import pygame
from levelEditor import tile_size
from miscFunctions import scale, importFolderImages


class Tile(pygame.sprite.Sprite):
    def __init__(self,size,x,y):
        super().__init__()
        self.image=pygame.Surface((size,size))
        self.rect=self.image.get_rect(topleft=(x,y))
    def update(self,x_shift):
        self.rect.x +=x_shift
class staticTile(Tile):
    def __init__(self,size,x,y,surface):
        super().__init__(size,x,y)
        self.image=surface
    def update(self,x_shift):
        self.rect.x +=x_shift

class animatedTile(Tile):
    def __init__(self,size,x,y,path):
        super().__init__(size,x,y)
        self.frames=importFolderImages(path)
        self.frameIndex=0
        self.image=self.frames[self.frameIndex]
    def animate(self):
        self.frameIndex+=0.15
        if self.frameIndex>=len(self.frames):
            self.frameIndex=0
        self.image=self.frames[int(self.frameIndex)]

    def update(self,x_shift):
        self.animate()
        self.rect.x += x_shift

class coin(animatedTile):
    def __init__(self,size,x,y,path,value):
        super().__init__(size,x,y,path)
        centerX=x+int(size/2)
        centerY=y+int(size/2)
        self.rect=self.image.get_rect(center=(centerX,centerY))
        self.value=value

class box(staticTile):
    def __init__(self,size,x,y):
        super().__init__(size,x,y,scale(pygame.image.load("../assets/sprites/objects/box.png").convert_alpha(),64,64))
class luckyblock(staticTile):
    def __init__(self, size, x, y, path, state):
        super().__init__(size, x, y,pygame.image.load(path).convert_alpha())
        self.state = state
    def updateState(self,state):
        self.state = state
class goal(staticTile):
    def __init__(self,size,x,y):
        super().__init__(size,x,y,pygame.image.load("../assets/sprites/objects/goal/goal.png").convert_alpha())