from screeninfo import get_monitors

from configLoader import *
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


verticalTileNumber=11
tile_size = 64
if firstTime:
    screenWidth = primaryMonitorSize()[0]
else:
    screenWidth=width
screenheight = verticalTileNumber*tile_size

level0={
    "background": "../levels/0/level_0_background.csv",
    "boxes":"../levels/0/level_0_boxes.csv",
    "coins":"../levels/0/level_0_coins.csv",
    "constraints":"../levels/0/level_0_constraints.csv",
    "constraints2":"../levels/0/level_0_constraints2.csv",
    "constraints3": "../levels/0/level_0_constraints3.csv",
    "enemys":"../levels/0/level_0_enemys.csv",
    "luckyblocks":"../levels/0/level_0_luckyblocks.csv",
    "decoration":"../levels/0/level_0_windows and doors.csv"
}




