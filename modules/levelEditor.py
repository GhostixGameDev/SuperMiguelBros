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

if firstTime:
    screenWidth = primaryMonitorSize()[0]
else:
    screenWidth=width
screenheight = verticalTileNumber * tileSizeScaled

Level0={
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
Level1={
    "background": "../levels/1/level_1_background.csv",
    "boxes":"../levels/1/level_1_boxes.csv",
    "coins":"../levels/1/level_1_coins.csv",
    "constraints":"../levels/1/level_1_constraints.csv",
    "constraints2":"../levels/1/level_1_constraints2.csv",
    "constraints3": "../levels/1/level_1_constraints3.csv",
    "enemys":"../levels/1/level_1_enemys.csv",
    "luckyblocks":"../levels/1/level_1_luckyblocks.csv",
    "decoration":"../levels/1/level_1_windows and doors.csv"
}
Level2={
    "background": "../levels/2/level_2_background.csv",
    "boxes":"../levels/2/level_2_boxes.csv",
    "coins":"../levels/2/level_2_coins.csv",
    "constraints":"../levels/2/level_2_constraints.csv",
    "constraints2":"../levels/2/level_2_constraints2.csv",
    "constraints3": "../levels/2/level_2_constraints3.csv",
    "enemys":"../levels/2/level_2_enemys.csv",
    "luckyblocks":"../levels/2/level_2_luckyblocks.csv",
    "decoration":"../levels/2/level_2_windows and doors.csv"
}
Level3={
    "background": "../levels/3/level_3_background.csv",
    "boxes":"../levels/3/level_3_boxes.csv",
    "coins":"../levels/3/level_3_coins.csv",
    "constraints":"../levels/3/level_3_constraints.csv",
    "constraints2":"../levels/3/level_3_constraints2.csv",
    "constraints3": "../levels/3/level_3_constraints3.csv",
    "enemys":"../levels/3/level_3_enemys.csv",
    "luckyblocks":"../levels/3/level_3_luckyblocks.csv",
    "decoration":"../levels/3/level_3_windows and doors.csv"
}
Level4={
    "background": "../levels/4/level_4_background.csv",
    "boxes":"../levels/4/level_4_boxes.csv",
    "coins":"../levels/4/level_4_coins.csv",
    "constraints":"../levels/4/level_4_constraints.csv",
    "constraints2":"../levels/4/level_4_constraints2.csv",
    "constraints3": "../levels/4/level_4_constraints3.csv",
    "enemys":"../levels/4/level_4_enemys.csv",
    "luckyblocks":"../levels/4/level_4_luckyblocks.csv",
    "decoration":"../levels/4/level_4_windows and doors.csv"
}




