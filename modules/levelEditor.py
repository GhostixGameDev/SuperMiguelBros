from configLoader import *
from modules.miscFunctions import primaryMonitorSize

level_map = [
                "X                        ",#Columns: Each character in the string
                "X                        ",#Rows: Each position in the array.
                "X                                         XX",
                "X XX      XXX        XX                       XX",
                "X XX  P                             XXXXXXXX",
                "X XXXXX         XX            XX",
                "X XXXXX       XX       XX        XX",
                "X XX      X  XXX                      ",
                "X         X  XXX    XX               XXX",
                "X      XXXX  XXXXX  XX XX      XXXX",
                "XXXXXXXXXXX  XXXXX  XX XXXXXXX",
                "DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD",

            ]
tile_size = 64
if firstTime:
    screenWidth = primaryMonitorSize()[0]
else:
    screenWidth=width
screenheight = len(level_map)*tile_size
