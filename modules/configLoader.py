#================================
import configparser

from screeninfo import get_monitors

#CONFIGURATION
config=configparser.ConfigParser()
config.read("../Config/gameConfig.ini")
firstTime=config.getint("GAME_CONFIG","firstTime")
width=config.getint("GAME_CONFIG", "screenWidth")
height=config.getint("GAME_CONFIG", "screenHeight")
fullscreen=config.getint("GAME_CONFIG","fullscreen")
language=config.get("GAME_CONFIG","language")
maxFPS=config.getint("GAME_CONFIG","maxFPS")
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

#width=1920
#height=1080
firstTime=True #Turn it false for screen size testing
if firstTime:
    width=primaryMonitorSize()[0]
    height=primaryMonitorSize()[1]
    scale=primaryMonitorSize()[0]/1366
else:
    scale = width / 1366
tileSize = 64
tileSizeScaled=round(64*scale)
print(tileSizeScaled)