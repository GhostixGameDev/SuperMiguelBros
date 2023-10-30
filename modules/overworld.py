import pygame
from gameData import levels

class Node(pygame.sprite.Sprite):
    def __init__(self,pos,status):
        super().__init__()
        self.image=pygame.Surface((100,80))
        if status:
            self.image.fill("blue")
        else:
            self.image.fill("red")
        self.rect=self.image.get_rect(center=pos)

class Overworld:
    def __init__(self,startLevel,maxLevel,surface):

        #Setup
        self.displaySurface=surface
        self.maxLevel=maxLevel
        self.startLevel=startLevel

        #Assets
        self.setupNodes()
    #Creation of new levels in the menu
    def setupNodes(self):
        self.nodes=pygame.sprite.Group()
        for index, nodeData in enumerate(levels.values()):
            if index<=self.maxLevel:
                nodeSprite=Node(nodeData["nodePos"],True)
            else:
                nodeSprite = Node(nodeData["nodePos"],False)
            self.nodes.add(nodeSprite)
    def drawLines(self):
        points=[]
        # Also can be made with a comprehension like
        # points=[node["nodePos"] for index,node in enumerate(levels.values()) if index<=self.maxLevel]
        # But I think the comprehensions make code harder to read for someone costumed to other languages.
        for index, nodeData in enumerate(levels.values()):
            if index <= self.maxLevel:
                points.append(nodeData["nodePos"])
        if len(points) > 0:
            try:
                pygame.draw.lines(self.displaySurface,"red",False,points,6)
            except:
                pass
    def run(self):
        self.drawLines()
        self.nodes.draw(self.displaySurface)