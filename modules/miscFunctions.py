import pygame
from pygame import transform
from screeninfo import get_monitors
from os import walk
def posinega(numero):
    if numero > 0:
        return 1
    elif numero < 0:
        return -1
    else:
        return 0
def scale(imagen,scalex,scaley):
    return transform.scale(imagen,(scalex,scaley))
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