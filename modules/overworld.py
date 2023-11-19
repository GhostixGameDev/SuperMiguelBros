import pygame
from gameData import levels
from miscFunctions import importFolderImages, scale
class Node(pygame.sprite.Sprite):
    def __init__(self,pos,status,playerSpeed,path):
        super().__init__()
        self.path=path
        self.image=scale(pygame.image.load(self.path),150,130)
        if status:
            self.status=True
        else:
            self.status=False
        self.rect=self.image.get_rect(center=pos)
        self.checkPoint=pygame.Rect(self.rect.centerx-(playerSpeed/2),self.rect.centery-(playerSpeed/2),playerSpeed,playerSpeed)
    def update(self):
        if self.status:
            self.image=scale(pygame.image.load(self.path),150,130).convert_alpha()
        else:
            tintedSurface=self.image.copy()
            tintedSurface.fill("black",None,pygame.BLEND_RGBA_MULT)
            self.image.blit(tintedSurface,(0,0))
class overworldPlayer(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.pos=pos
        self.image= pygame.image.load("../assets/sprites/miguel/idle/p1_front.png").convert_alpha()
        self.rect= self.image.get_rect(center=pos)
    def update(self):
        self.rect.center=self.pos
class Overworld:
    def __init__(self,startLevel,maxLevel,surface,createLevel):

        #Setup
        self.displaySurface=surface
        self.maxLevel=maxLevel
        self.currentLevel=startLevel
        self.createLevel=createLevel

        #Player things
        self.moveDirection=pygame.math.Vector2(0,0)
        self.speed=6
        self.moving=False
        #Assets
        self.setupNodes()
        self.setupPlayer()

        #timers
        self.startTime=pygame.time.get_ticks()
        self.allowInput=True
        self.timerLength=500
    #Creation of new levels in the menu
    def setupNodes(self):
        self.nodes=pygame.sprite.Group()
        for index, nodeData in enumerate(levels.values()):
            if index<=self.maxLevel:
                nodeSprite=Node(nodeData["nodePos"],True,self.speed,nodeData["nodeAssets"])
            else:
                nodeSprite = Node(nodeData["nodePos"],False,self.speed,nodeData["nodeAssets"])
            self.nodes.add(nodeSprite)
    def setupPlayer(self):
        self.player=pygame.sprite.GroupSingle()
        playerSprite=overworldPlayer(self.nodes.sprites()[self.currentLevel].rect.center)
        self.player.add(playerSprite)
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
    def input(self):
        key=pygame.key.get_pressed()
        if not self.moving and self.allowInput:
            if key[pygame.K_d] and self.currentLevel!=self.maxLevel:
                self.moveDirection=self.getMovementData(1)
                self.currentLevel+=1
                self.moving=True
            elif key[pygame.K_a] and self.currentLevel!=0:
                self.moveDirection=self.getMovementData(-1)
                self.currentLevel -= 1
                self.moving=True
            elif key[pygame.K_SPACE]:
                self.createLevel(self.currentLevel)
    def getMovementData(self,direction):
        start=pygame.math.Vector2(self.nodes.sprites()[self.currentLevel].rect.center)
        end=pygame.math.Vector2(self.nodes.sprites()[self.currentLevel+(1*direction)].rect.center)
        return (end-start).normalize()
    def updatePlayerPos(self):
        if self.moving and self.moveDirection:
            self.player.sprite.pos+=self.moveDirection*self.speed
            targetNode=self.nodes.sprites()[self.currentLevel]
            if targetNode.checkPoint.collidepoint(self.player.sprite.pos):
                self.moving=False
                self.moveDirection=pygame.math.Vector2(0,0)
    def inputTimer(self):
        if not self.allowInput:
            currentTime=pygame.time.get_ticks()
            if currentTime-self.startTime>=self.timerLength:
                allowInput=True
    def run(self):
        self.displaySurface.fill("#008c96")
        self.input()
        self.nodes.update()
        self.player.update()
        self.updatePlayerPos()
        self.drawLines()
        self.inputTimer()
        self.nodes.draw(self.displaySurface)
        self.player.draw(self.displaySurface)