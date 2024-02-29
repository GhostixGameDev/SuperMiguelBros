import pygame
from pygame import transform
from screeninfo import get_monitors
from os import walk
from csv import reader

from levelEditor import tileSize


def posinega(numero):
    if numero > 0:
        return 1
    elif numero < 0:
        return -1
    else:
        return 0
def scale(imagen,scalex,scaley):
    return transform.scale(imagen,(scalex,scaley))
def scaleList(list,scalex,scaley):
    for i in range(0,len(list)):
        list[i] = scale(list[i],scalex,scaley)
    return list

def primaryMonitorSize():
    size=[0,0]
    primary=0
    if len(get_monitors())>1:
        for i in range(0,len(get_monitors())):
            if get_monitors()[i].is_primary:
                primary=i
    size[0]=get_monitors()[primary].width
    size[1]=get_monitors()[primary].height
    return size

def importFolderImages(path):
    spritesheet=[]
    for _,__,names in walk(path):
        for image in names:
            fullPath=path+"/"+image
            sprite=pygame.image.load(fullPath).convert_alpha()
            spritesheet.append(sprite)
    return spritesheet
def importCsvLayout(path):
    terrainMap=[]
    with open(path) as map:
        level=reader(map,delimiter=",")
        for row in level:
            terrainMap.append(list(row))
        return terrainMap

def importCutSpritesheet(path):
    surface=pygame.image.load(path).convert_alpha()
    tileNumX=int(surface.get_size()[0]/tileSize)
    tileNumY=int(surface.get_size()[1]/tileSize)
    cutTiles=[]
    for row in range(tileNumY):
        for col in range(tileNumX):
            x=col*tileSize
            y=row*tileSize
            newSurface=pygame.Surface((tileSize,tileSize),flags=pygame.SRCALPHA)
            newSurface.blit(surface,(0,0),pygame.Rect(x,y,tileSize,tileSize))
            cutTiles.append(newSurface)
    return cutTiles
